"""
DeepseekTravels API Server - Simplified Version

FastAPI backend that provides a simple chat interface while 
MCP servers are being set up. This can be extended later 
with full LangChain integration.
"""

import os
import json
from typing import Dict, Any, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import httpx

# Create FastAPI app
app = FastAPI(
    title="DeepseekTravels API",
    description="Intelligent travel packing assistant API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: datetime

class HealthResponse(BaseModel):
    status: str
    agent_ready: bool
    mcp_servers: Dict[str, str]
    tools_count: int

class ServerStatusResponse(BaseModel):
    servers: Dict[str, Dict[str, Any]]

# Simple in-memory session storage
sessions: Dict[str, list] = {}

def get_or_create_session(session_id: str) -> list:
    """Get or create a conversation session"""
    if session_id not in sessions:
        sessions[session_id] = []
    return sessions[session_id]

def generate_mock_response(message: str) -> str:
    """Generate a mock response based on the user's message"""
    lowerMessage = message.lower()
    
    # Check for packing list requests
    if any(word in lowerMessage for word in ['pack', 'list', 'bring', 'trip']):
        return generate_packing_response(message)
    
    # Check for weather requests
    if any(word in lowerMessage for word in ['weather', 'temperature', 'climate']):
        return generate_weather_response(message)
    
    # Check for travel requirements
    if any(word in lowerMessage for word in ['visa', 'requirement', 'document']):
        return generate_requirements_response(message)
    
    # Check for booking requests
    if any(word in lowerMessage for word in ['flight', 'hotel', 'book', 'accommodation']):
        return generate_booking_response(message)
    
    # General response
    return generate_general_response(message)

def generate_packing_response(message: str) -> str:
    """Generate a mock packing list response"""
    return """🧳 **Packing List for Your Trip**

I'd love to help you create a personalized packing list! Based on your message, here's a starter list:

**👔 Essential Clothing:**
• 3-4 shirts/tops (mix of casual and smart)
• 2 pairs of pants/bottoms
• 5-6 underwear
• 5-6 pairs of socks
• 1 light jacket or sweater
• Sleepwear

**🧴 Toiletries & Personal:**
• Toothbrush & toothpaste
• Shampoo/soap (travel size)
• Deodorant
• Sunscreen
• Personal medications

**📱 Electronics:**
• Phone charger
• Universal adapter
• Power bank
• Headphones

**📄 Important Documents:**
• Passport/ID
• Travel insurance
• Flight/hotel confirmations
• Emergency contact info

**🎯 Smart Tips:**
• Roll clothes to save 30% space
• Wear your heaviest items while traveling
• Pack for laundry every 5-7 days
• Leave 20% space for souvenirs

💡 *For a more detailed and personalized list, please make sure the MCP servers are running so I can check weather, travel requirements, and airline restrictions for your specific destination!*

What's your destination and how long is your trip? I can provide more specific recommendations! 🌍"""

def generate_weather_response(message: str) -> str:
    """Generate a mock weather response"""
    return """🌤️ **Weather Information**

I'd like to help you with weather information, but I need the weather service to be running to provide accurate forecasts.

**What I can help with when connected:**
• 7-day weather forecast for your destination
• Temperature ranges (min/max)
• Precipitation probability
• Wind conditions
• Humidity levels
• Weather-specific packing recommendations

**For now, here are some general tips:**
• Check the weather forecast before you travel
• Pack layers for temperature changes
• Bring a light rain jacket for unexpected showers
• Consider the season and climate of your destination

💡 *To get real weather data, please start the MCP servers using `./start-servers.sh` and I'll provide detailed forecasts for any destination!*

What destination are you traveling to? 🌍"""

def generate_requirements_response(message: str) -> str:
    """Generate a mock travel requirements response"""
    return """📋 **Travel Requirements**

I can help you check travel requirements, but I need the travel requirements service to be running for accurate, up-to-date information.

**What I can check when connected:**
• Visa requirements for your nationality and destination
• Required vaccinations and health certificates
• Security restrictions and prohibited items
• Airport and airline-specific baggage rules
• Documentation needed for entry/exit

**General reminders:**
• Ensure your passport is valid for at least 6 months
• Check if you need any vaccinations
• Review your airline's baggage restrictions
• Make copies of important documents

💡 *For specific requirements, please start the MCP servers and I'll check the latest requirements for your destination and nationality!*

Where are you traveling to and from? 🛂"""

def generate_booking_response(message: str) -> str:
    """Generate a mock booking response"""
    return """🔍 **Booking Assistance**

I can help you find flights, hotels, and activities, but I need the booking service to be running for real search results.

**What I can help with when connected:**
• Flight searches with multiple airlines
• Hotel recommendations and pricing
• Activity and tour suggestions
• Booking comparisons and reviews
• Price alerts and booking confirmation

**In the meantime:**
• Compare prices on multiple booking sites
• Book directly with airlines for better flexibility
• Read recent reviews for hotels and activities
• Consider booking cancellation policies

💡 *For live search results and booking assistance, please start the MCP servers and I'll help you find the best deals!*

What type of booking are you looking for? ✈️🏨"""

def generate_general_response(message: str) -> str:
    """Generate a general response"""
    return f"""🧳 **DeepseekTravels Assistant**

Hello! I'm your intelligent travel packing assistant. I can help you with:

🌦️ **Weather-based packing** - I'll check forecasts and recommend appropriate clothing
📋 **Smart packing lists** - Optimized for your bag size, weight limits, and activities  
✈️ **Airline restrictions** - Baggage rules and security restrictions
🏨 **Travel requirements** - Visa info, documents, and country-specific rules
🎯 **Activity planning** - Business, hiking, beach, formal events, and more

**To get started, try asking:**
• "What should I pack for a week in Tokyo in November?"
• "Beach weekend in Lisbon - keep it simple!"
• "Business trip to Singapore, 28L backpack"
• "What's the weather like in Paris next week?"
• "Do I need a visa for Japan?"

**Your message:** "{message}"

💡 *For full functionality including real-time weather, travel requirements, and booking searches, please start the MCP servers using `./start-servers.sh`*

How can I help you plan your next adventure? 🚀"""

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    # Check MCP server status
    mcp_status = {}
    server_configs = {
        "weather": "http://127.0.0.1:8009",
        "attractions": "http://127.0.0.1:8008", 
        "travel_requirements": "http://127.0.0.1:8010",
        "booking": "http://127.0.0.1:8011"
    }
    
    async with httpx.AsyncClient(timeout=2.0) as client:
        for name, url in server_configs.items():
            try:
                response = await client.get(f"{url}/health")
                mcp_status[name] = "connected" if response.status_code == 200 else "error"
            except:
                mcp_status[name] = "disconnected"
    
    return HealthResponse(
        status="healthy",
        agent_ready=True,  # Simplified version is always ready
        mcp_servers=mcp_status,
        tools_count=4  # Mock tool count
    )

@app.get("/servers/status", response_model=ServerStatusResponse)
async def server_status():
    """Get detailed server status"""
    servers = {
        "weather": {"url": "http://127.0.0.1:8009", "name": "Weather"},
        "attractions": {"url": "http://127.0.0.1:8008", "name": "Attractions"},
        "travel_requirements": {"url": "http://127.0.0.1:8010", "name": "Travel Requirements"},
        "booking": {"url": "http://127.0.0.1:8011", "name": "Booking"}
    }
    
    status_results = {}
    
    async with httpx.AsyncClient(timeout=3.0) as client:
        for key, info in servers.items():
            try:
                response = await client.get(f"{info['url']}/health")
                if response.status_code == 200:
                    status_results[key] = {
                        "status": "connected",
                        "name": info["name"],
                        "url": info["url"]
                    }
                else:
                    status_results[key] = {
                        "status": "error",
                        "name": info["name"],
                        "url": info["url"],
                        "error": f"HTTP {response.status_code}"
                    }
            except Exception as e:
                status_results[key] = {
                    "status": "disconnected",
                    "name": info["name"],
                    "url": info["url"],
                    "error": str(e)
                }
    
    return ServerStatusResponse(servers=status_results)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    """Main chat endpoint that processes user messages"""
    try:
        # Get or create session
        session_history = get_or_create_session(chat_message.session_id)
        
        # Add user message to history
        session_history.append({
            "role": "user",
            "content": chat_message.message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Generate response (simplified version)
        response_text = generate_mock_response(chat_message.message)
        
        # Add assistant response to history
        session_history.append({
            "role": "assistant", 
            "content": response_text,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 20 messages to prevent memory issues
        if len(session_history) > 20:
            session_history = session_history[-20:]
            sessions[chat_message.session_id] = session_history
        
        return ChatResponse(
            response=response_text,
            session_id=chat_message.session_id,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        print(f"❌ Error processing chat message: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing your request: {str(e)}"
        )

@app.delete("/sessions/{session_id}")
async def clear_session(session_id: str):
    """Clear a conversation session"""
    if session_id in sessions:
        del sessions[session_id]
        return {"message": f"Session {session_id} cleared"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")

@app.get("/sessions")
async def list_sessions():
    """List all active sessions"""
    return {"sessions": list(sessions.keys()), "count": len(sessions)}

if __name__ == "__main__":
    print("🚀 Starting DeepseekTravels API Server (Simplified Mode)...")
    print("   This version provides mock responses while MCP servers are being set up.")
    print("   For full functionality, implement LangChain integration.")
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )