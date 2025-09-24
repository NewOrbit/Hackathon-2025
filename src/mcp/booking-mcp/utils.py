"""Booking MCP Server utilities"""

from typing import Dict, Any, List
from datetime import datetime

def format_flight_summary(flights: List[Dict[str, Any]]) -> str:
    """Format flight results into a readable summary"""
    if not flights:
        return "No flights found for the specified criteria."
    
    summary = f"Found {len(flights)} flights:\n\n"
    
    for i, flight in enumerate(flights[:3], 1):  # Show top 3
        dep_time = datetime.fromisoformat(flight['departure_time']).strftime("%H:%M")
        arr_time = datetime.fromisoformat(flight['arrival_time']).strftime("%H:%M")
        duration = f"{flight['duration_minutes'] // 60}h {flight['duration_minutes'] % 60}m"
        
        summary += f"{i}. {flight['airline']} {flight['flight_number']}\n"
        summary += f"   {flight['departure_airport']} {dep_time} → {flight['arrival_airport']} {arr_time} ({duration})\n"
        summary += f"   ${flight['price_usd']:.0f} • {flight['seats_available']} seats available\n\n"
    
    return summary

def format_hotel_summary(hotels: List[Dict[str, Any]]) -> str:
    """Format hotel results into a readable summary"""
    if not hotels:
        return "No hotels found for the specified criteria."
    
    summary = f"Found {len(hotels)} hotels:\n\n"
    
    for i, hotel in enumerate(hotels, 1):
        stars = "⭐" * int(hotel['rating_stars'])
        
        summary += f"{i}. {hotel['name']} {stars}\n"
        summary += f"   {hotel['address']}, {hotel['city']}\n"
        summary += f"   ${hotel['price_per_night_usd']:.0f}/night • Total: ${hotel['total_price_usd']:.0f}\n"
        summary += f"   Amenities: {', '.join(hotel['amenities'][:3])}\n\n"
    
    return summary

def format_activity_summary(activities: List[Dict[str, Any]]) -> str:
    """Format activity results into a readable summary"""
    if not activities:
        return "No activities found for the specified criteria."
    
    summary = f"Found {len(activities)} activities:\n\n"
    
    for i, activity in enumerate(activities, 1):
        summary += f"{i}. {activity['name']}\n"
        summary += f"   {activity['description']}\n"
        summary += f"   Duration: {activity['duration_hours']}h • ${activity['price_per_person_usd']:.0f} per person\n"
        summary += f"   Categories: {', '.join(activity['categories'])}\n\n"
    
    return summary

def format_booking_confirmation(confirmation: Dict[str, Any]) -> str:
    """Format booking confirmation into a readable summary"""
    conf = confirmation.get('confirmation', {})
    
    summary = f"🎉 Booking Confirmed!\n\n"
    summary += f"Confirmation: {conf.get('confirmation_id', 'N/A')}\n"
    summary += f"Type: {conf.get('booking_type', 'N/A').title()}\n"
    summary += f"Total: ${conf.get('total_price_usd', 0):.2f}\n"
    summary += f"Status: {conf.get('status', 'N/A').title()}\n\n"
    
    if conf.get('contact_info'):
        summary += f"Contact: {conf['contact_info'].get('email', 'N/A')}\n"
    
    if confirmation.get('important_note'):
        summary += f"\n⚠️ {confirmation['important_note']}\n"
    
    return summary