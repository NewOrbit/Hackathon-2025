"""
Restaurant service with business logic for reservations and menu operations.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, date, time, timedelta
import random
import string

from models import Restaurant, MenuItem, Reservation, BookingResponse
from restaurant_data import LONDON_RESTAURANTS, PARIS_RESTAURANTS, ROME_RESTAURANTS

# In-memory storage for reservations (in production, this would be a database)
reservations_db: List[Reservation] = []


def get_restaurants_by_location(location: str) -> List[Restaurant]:
    """Get restaurants by location (London, Paris, or Rome)."""
    if location.lower() == "london":
        return LONDON_RESTAURANTS
    elif location.lower() == "paris":
        return PARIS_RESTAURANTS
    elif location.lower() == "rome":
        return ROME_RESTAURANTS
    else:
        return LONDON_RESTAURANTS + PARIS_RESTAURANTS + ROME_RESTAURANTS


def get_restaurant_by_id(restaurant_id: str) -> Optional[Restaurant]:
    """Get a specific restaurant by ID."""
    all_restaurants = LONDON_RESTAURANTS + PARIS_RESTAURANTS + ROME_RESTAURANTS
    for restaurant in all_restaurants:
        if restaurant.id == restaurant_id:
            return restaurant
    return None


def search_restaurants(
    location: Optional[str] = None,
    cuisine_type: Optional[str] = None,
    price_range: Optional[str] = None,
    rating_min: Optional[float] = None
) -> List[Restaurant]:
    """Search restaurants with filters."""
    restaurants = get_restaurants_by_location(location) if location else LONDON_RESTAURANTS + PARIS_RESTAURANTS + ROME_RESTAURANTS

    filtered = restaurants

    if cuisine_type:
        filtered = [r for r in filtered if cuisine_type.lower() in r.cuisine_type.lower()]

    if price_range:
        filtered = [r for r in filtered if r.price_range == price_range]

    if rating_min:
        filtered = [r for r in filtered if r.rating >= rating_min]

    return filtered


def get_restaurant_menu(restaurant_id: str) -> Optional[List[MenuItem]]:
    """Get menu for a specific restaurant."""
    restaurant = get_restaurant_by_id(restaurant_id)
    return restaurant.menu if restaurant else None


def search_menu_items(
    restaurant_id: Optional[str] = None,
    category: Optional[str] = None,
    max_calories: Optional[float] = None,
    dietary_tags: Optional[List[str]] = None,
    allergen_free: Optional[List[str]] = None
) -> List[MenuItem]:
    """Search menu items with filters."""
    all_items = []

    if restaurant_id:
        menu = get_restaurant_menu(restaurant_id)
        if menu:
            all_items = menu
    else:
        # Search all restaurants
        for restaurant in LONDON_RESTAURANTS + PARIS_RESTAURANTS + ROME_RESTAURANTS:
            all_items.extend(restaurant.menu)

    filtered = all_items

    if category:
        filtered = [item for item in filtered if item.category.lower() == category.lower()]

    if max_calories:
        filtered = [item for item in filtered if item.total_calories <= max_calories]

    if dietary_tags:
        filtered = [item for item in filtered if any(tag in item.dietary_tags for tag in dietary_tags)]

    if allergen_free:
        filtered = [item for item in filtered if not any(allergen in item.allergens for allergen in allergen_free)]

    return filtered


def book_reservation(
    restaurant_id: str,
    customer_name: str,
    customer_email: str,
    customer_phone: str,
    reservation_date: str,
    reservation_time: str,
    party_size: int,
    special_requests: Optional[str] = None
) -> BookingResponse:
    """Book a restaurant reservation."""
    restaurant = get_restaurant_by_id(restaurant_id)
    if not restaurant:
        return BookingResponse(
            success=False,
            message=f"Restaurant with ID {restaurant_id} not found"
        )

    # Check if restaurant is open on that day
    try:
        date_obj = datetime.strptime(reservation_date, "%Y-%m-%d").date()
        day_name = date_obj.strftime("%A")
        if day_name not in restaurant.opening_hours or restaurant.opening_hours[day_name] == "Closed":
            return BookingResponse(
                success=False,
                message=f"Restaurant is closed on {day_name}"
            )
    except ValueError:
        return BookingResponse(
            success=False,
            message="Invalid date format. Please use YYYY-MM-DD"
        )

    # Check advance booking limit
    today = date.today()
    if date_obj > today + timedelta(days=restaurant.booking_advance_days):
        return BookingResponse(
            success=False,
            message=f"Can only book up to {restaurant.booking_advance_days} days in advance"
        )

    if date_obj < today:
        return BookingResponse(
            success=False,
            message="Cannot book for past dates"
        )

    # Generate reservation ID
    reservation_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    # Create reservation
    try:
        time_obj = datetime.strptime(reservation_time, "%H:%M").time()
    except ValueError:
        return BookingResponse(
            success=False,
            message="Invalid time format. Please use HH:MM"
        )

    reservation = Reservation(
        id=reservation_id,
        restaurant_id=restaurant_id,
        customer_name=customer_name,
        customer_email=customer_email,
        customer_phone=customer_phone,
        reservation_date=date_obj,
        reservation_time=time_obj,
        party_size=party_size,
        special_requests=special_requests
    )

    # Store reservation
    reservations_db.append(reservation)

    return BookingResponse(
        success=True,
        reservation_id=reservation_id,
        message="Reservation confirmed successfully",
        confirmation_details={
            "restaurant_name": restaurant.name,
            "restaurant_address": restaurant.address,
            "restaurant_phone": restaurant.phone,
            "reservation_date": reservation_date,
            "reservation_time": reservation_time,
            "party_size": party_size,
            "special_requests": special_requests
        }
    )


def get_reservation(reservation_id: str) -> Optional[Reservation]:
    """Get reservation details by ID."""
    for reservation in reservations_db:
        if reservation.id == reservation_id:
            return reservation
    return None


def cancel_reservation(reservation_id: str) -> BookingResponse:
    """Cancel a reservation."""
    reservation = get_reservation(reservation_id)
    if not reservation:
        return BookingResponse(
            success=False,
            message=f"Reservation {reservation_id} not found"
        )

    reservation.status = "cancelled"
    return BookingResponse(
        success=True,
        message="Reservation cancelled successfully"
    )


def get_restaurant_availability(restaurant_id: str, date_str: str) -> Dict[str, Any]:
    """Get available time slots for a restaurant on a specific date."""
    restaurant = get_restaurant_by_id(restaurant_id)
    if not restaurant:
        return {"error": f"Restaurant {restaurant_id} not found"}

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        day_name = date_obj.strftime("%A")

        if day_name not in restaurant.opening_hours or restaurant.opening_hours[day_name] == "Closed":
            return {"error": f"Restaurant is closed on {day_name}"}

        # Simple availability check (in production, this would check actual bookings)
        hours = restaurant.opening_hours[day_name]
        if "12:00" in hours:
            return {
                "date": date_str,
                "available_slots": [
                    "12:00", "12:30", "13:00", "13:30", "14:00",
                    "19:00", "19:30", "20:00", "20:30", "21:00"
                ],
                "restaurant_capacity": restaurant.capacity
            }
        else:
            return {
                "date": date_str,
                "available_slots": [
                    "19:00", "19:30", "20:00", "20:30", "21:00", "21:30"
                ],
                "restaurant_capacity": restaurant.capacity
            }
    except ValueError:
        return {"error": "Invalid date format. Please use YYYY-MM-DD"}