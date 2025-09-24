"""
Restaurants MCP Server - Restaurant discovery, menu browsing, and reservation booking.

To run this server:
    uv run mcp dev main.py

Provides restaurant information, menu details with nutritional data, and booking capabilities
for restaurants in London and Paris.
"""

from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

from restaurant_service import (
    get_restaurants_by_location,
    get_restaurant_by_id,
    search_restaurants,
    get_restaurant_menu,
    search_menu_items,
    book_reservation,
    get_reservation,
    cancel_reservation,
    get_restaurant_availability
)

mcp = FastMCP("Restaurants", port=8014)

# Restaurant discovery tools
@mcp.tool()
def get_restaurants(location: Optional[str] = None) -> Dict[str, Any]:
    """Get restaurants by location (London or Paris)

    Args:
        location: City name - "London", "Paris", or None for all

    Returns:
        List of restaurants with basic information
    """
    restaurants = get_restaurants_by_location(location) if location else get_restaurants_by_location("all")

    return {
        "restaurants": [
            {
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "cuisine_type": r.cuisine_type,
                "location": r.location,
                "address": r.address,
                "phone": r.phone,
                "rating": r.rating,
                "price_range": r.price_range,
                "special_features": r.special_features
            }
            for r in restaurants
        ],
        "total_count": len(restaurants)
    }

@mcp.tool()
def search_restaurants_tool(
    location: Optional[str] = None,
    cuisine_type: Optional[str] = None,
    price_range: Optional[str] = None,
    rating_min: Optional[float] = None
) -> Dict[str, Any]:
    """Search restaurants with filters

    Args:
        location: City name (London, Paris)
        cuisine_type: Type of cuisine (British, French, Indian, etc.)
        price_range: Price range ($, $$, $$$, $$$$)
        rating_min: Minimum rating (1.0-5.0)

    Returns:
        Filtered list of restaurants
    """
    restaurants = search_restaurants(location, cuisine_type, price_range, rating_min)

    return {
        "restaurants": [
            {
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "cuisine_type": r.cuisine_type,
                "location": r.location,
                "rating": r.rating,
                "price_range": r.price_range,
                "special_features": r.special_features
            }
            for r in restaurants
        ],
        "total_count": len(restaurants),
        "filters_applied": {
            "location": location,
            "cuisine_type": cuisine_type,
            "price_range": price_range,
            "rating_min": rating_min
        }
    }

@mcp.tool()
def get_restaurant_details(restaurant_id: str) -> Dict[str, Any]:
    """Get detailed information about a specific restaurant

    Args:
        restaurant_id: Unique ID of the restaurant

    Returns:
        Detailed restaurant information including menu and booking details
    """
    restaurant = get_restaurant_by_id(restaurant_id)
    if not restaurant:
        return {"error": f"Restaurant with ID {restaurant_id} not found"}

    return {
        "id": restaurant.id,
        "name": restaurant.name,
        "description": restaurant.description,
        "cuisine_type": restaurant.cuisine_type,
        "location": restaurant.location,
        "address": restaurant.address,
        "phone": restaurant.phone,
        "email": restaurant.email,
        "rating": restaurant.rating,
        "price_range": restaurant.price_range,
        "opening_hours": restaurant.opening_hours,
        "capacity": restaurant.capacity,
        "booking_advance_days": restaurant.booking_advance_days,
        "special_features": restaurant.special_features,
        "coordinates": restaurant.coordinates,
        "menu_item_count": len(restaurant.menu)
    }

# Menu and nutrition tools
@mcp.tool()
def get_restaurant_menu_tool(restaurant_id: str) -> Dict[str, Any]:
    """Get menu for a specific restaurant

    Args:
        restaurant_id: Unique ID of the restaurant

    Returns:
        Complete menu with nutritional information
    """
    menu = get_restaurant_menu(restaurant_id)
    if not menu:
        return {"error": f"Restaurant with ID {restaurant_id} not found or has no menu"}

    return {
        "restaurant_id": restaurant_id,
        "menu_items": [
            {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "price": item.price,
                "currency": item.currency,
                "category": item.category,
                "total_calories": item.total_calories,
                "total_protein": item.total_protein,
                "total_carbs": item.total_carbs,
                "total_fat": item.total_fat,
                "total_fiber": item.total_fiber,
                "allergens": item.allergens,
                "dietary_tags": item.dietary_tags,
                "preparation_time": item.preparation_time,
                "spice_level": item.spice_level,
                "ingredients": [
                    {
                        "name": ing.name,
                        "quantity": ing.quantity,
                        "calories_per_unit": ing.calories_per_unit,
                        "protein": ing.protein,
                        "carbs": ing.carbs,
                        "fat": ing.fat,
                        "fiber": ing.fiber,
                        "allergens": ing.allergens
                    }
                    for ing in item.ingredients
                ]
            }
            for item in menu
        ],
        "total_items": len(menu)
    }

@mcp.tool()
def search_menu_items_tool(
    restaurant_id: Optional[str] = None,
    category: Optional[str] = None,
    max_calories: Optional[float] = None,
    dietary_tags: Optional[List[str]] = None,
    allergen_free: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Search menu items with nutritional and dietary filters

    Args:
        restaurant_id: Specific restaurant ID (optional)
        category: Menu category (appetizer, main, dessert, beverage)
        max_calories: Maximum calories per item
        dietary_tags: Dietary requirements (vegetarian, vegan, gluten-free)
        allergen_free: Allergens to avoid

    Returns:
        Filtered menu items with nutritional data
    """
    items = search_menu_items(restaurant_id, category, max_calories, dietary_tags, allergen_free)

    return {
        "menu_items": [
            {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "price": item.price,
                "currency": item.currency,
                "category": item.category,
                "total_calories": item.total_calories,
                "total_protein": item.total_protein,
                "total_carbs": item.total_carbs,
                "total_fat": item.total_fat,
                "total_fiber": item.total_fiber,
                "allergens": item.allergens,
                "dietary_tags": item.dietary_tags,
                "spice_level": item.spice_level
            }
            for item in items
        ],
        "total_count": len(items),
        "filters_applied": {
            "restaurant_id": restaurant_id,
            "category": category,
            "max_calories": max_calories,
            "dietary_tags": dietary_tags,
            "allergen_free": allergen_free
        }
    }

# Booking tools
@mcp.tool()
def book_restaurant_reservation(
    restaurant_id: str,
    customer_name: str,
    customer_email: str,
    customer_phone: str,
    reservation_date: str,
    reservation_time: str,
    party_size: int,
    special_requests: Optional[str] = None
) -> Dict[str, Any]:
    """Book a restaurant reservation

    Args:
        restaurant_id: ID of the restaurant
        customer_name: Name of the customer
        customer_email: Email address for confirmation
        customer_phone: Phone number
        reservation_date: Date in YYYY-MM-DD format
        reservation_time: Time in HH:MM format
        party_size: Number of people (1-20)
        special_requests: Optional special requests

    Returns:
        Booking confirmation details
    """
    result = book_reservation(
        restaurant_id, customer_name, customer_email, customer_phone,
        reservation_date, reservation_time, party_size, special_requests
    )

    return {
        "success": result.success,
        "reservation_id": result.reservation_id,
        "message": result.message,
        "confirmation_details": result.confirmation_details
    }

@mcp.tool()
def get_reservation_details(reservation_id: str) -> Dict[str, Any]:
    """Get details of a specific reservation

    Args:
        reservation_id: Unique reservation ID

    Returns:
        Reservation details
    """
    reservation = get_reservation(reservation_id)
    if not reservation:
        return {"error": f"Reservation {reservation_id} not found"}

    return {
        "id": reservation.id,
        "restaurant_id": reservation.restaurant_id,
        "customer_name": reservation.customer_name,
        "customer_email": reservation.customer_email,
        "customer_phone": reservation.customer_phone,
        "reservation_date": reservation.reservation_date.isoformat(),
        "reservation_time": reservation.reservation_time.isoformat(),
        "party_size": reservation.party_size,
        "special_requests": reservation.special_requests,
        "status": reservation.status,
        "created_at": reservation.created_at.isoformat() if reservation.created_at else None
    }

@mcp.tool()
def cancel_restaurant_reservation(reservation_id: str) -> Dict[str, Any]:
    """Cancel a restaurant reservation

    Args:
        reservation_id: Unique reservation ID

    Returns:
        Cancellation confirmation
    """
    result = cancel_reservation(reservation_id)
    return {
        "success": result.success,
        "message": result.message
    }

@mcp.tool()
def get_restaurant_availability_tool(restaurant_id: str, date: str) -> Dict[str, Any]:
    """Get available time slots for a restaurant on a specific date

    Args:
        restaurant_id: ID of the restaurant
        date: Date in YYYY-MM-DD format

    Returns:
        Available time slots and capacity information
    """
    return get_restaurant_availability(restaurant_id, date)

# Resources
@mcp.resource("restaurants://{restaurant_id}")
def get_restaurant_resource(restaurant_id: str) -> str:
    """Get restaurant information as a formatted resource"""
    restaurant = get_restaurant_by_id(restaurant_id)
    if not restaurant:
        return f"Restaurant {restaurant_id} not found"

    result = f"🍽️ **{restaurant.name}**\n\n"
    result += f"**Cuisine:** {restaurant.cuisine_type}\n"
    result += f"**Location:** {restaurant.location}\n"
    result += f"**Address:** {restaurant.address}\n"
    result += f"**Phone:** {restaurant.phone}\n"
    result += f"**Rating:** {restaurant.rating}/5.0\n"
    result += f"**Price Range:** {restaurant.price_range}\n"
    result += f"**Capacity:** {restaurant.capacity} people\n\n"

    result += "**Opening Hours:**\n"
    for day, hours in restaurant.opening_hours.items():
        result += f"• {day}: {hours}\n"

    if restaurant.special_features:
        result += f"\n**Special Features:** {', '.join(restaurant.special_features)}\n"

    return result

@mcp.resource("restaurants://menu/{restaurant_id}")
def get_restaurant_menu_resource(restaurant_id: str) -> str:
    """Get restaurant menu as a formatted resource"""
    menu = get_restaurant_menu(restaurant_id)
    if not menu:
        return f"Menu not found for restaurant {restaurant_id}"

    result = f"🍽️ **Menu for Restaurant {restaurant_id}**\n\n"

    for item in menu:
        result += f"**{item.name}** - {item.price} {item.currency}\n"
        result += f"_{item.description}_\n"
        result += f"📊 **Nutrition:** {item.total_calories} cal, {item.total_protein}g protein, {item.total_carbs}g carbs, {item.total_fat}g fat\n"
        if item.allergens:
            result += f"⚠️ **Allergens:** {', '.join(item.allergens)}\n"
        if item.dietary_tags:
            result += f"🏷️ **Dietary:** {', '.join(item.dietary_tags)}\n"
        result += f"⏱️ **Prep Time:** {item.preparation_time} min | 🌶️ **Spice:** {item.spice_level}/5\n\n"

    return result

# Prompts
@mcp.prompt()
def restaurant_booking_prompt(location: str, cuisine_type: Optional[str] = None) -> str:
    """Generate a prompt for restaurant booking assistance"""
    base_prompt = f"""Please help with restaurant booking in {location}"""
    if cuisine_type:
        base_prompt += f" specializing in {cuisine_type} cuisine"

    return base_prompt + """, including:
1. Restaurant recommendations based on preferences
2. Menu analysis with nutritional information
3. Dietary restrictions and allergen considerations
4. Booking availability and reservation process
5. Special requests and accommodations
6. Price range and budget considerations
7. Location and accessibility information
8. Integration with nutrition planning and macro tracking

Focus on providing comprehensive restaurant guidance that integrates with nutrition and health goals."""

@mcp.prompt()
def nutrition_restaurant_prompt(restaurant_id: str, dietary_goals: Optional[str] = None) -> str:
    """Generate a prompt for nutrition-focused restaurant guidance"""
    base_prompt = f"""Please provide nutrition-focused guidance for restaurant {restaurant_id}"""
    if dietary_goals:
        base_prompt += f" with the goal of {dietary_goals}"

    return base_prompt + """, including:
1. Menu item analysis with detailed nutritional breakdown
2. Macro and micronutrient optimization
3. Calorie counting and portion control
4. Allergen and dietary restriction management
5. Integration with fitness and health goals
6. Meal planning and preparation timing
7. Supplement and nutrition timing considerations
8. Integration with other nutrition tracking services

Focus on providing actionable nutrition advice that helps achieve specific health and fitness goals."""

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
