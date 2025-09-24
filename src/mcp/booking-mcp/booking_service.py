"""Booking Service - Mock data provider for Phase 1"""

from typing import Dict, Any, List
from datetime import datetime, timedelta, date
import uuid
from config import ensure_offline_mode, MOCK_SOURCES, BOOKING_SESSIONS
from models import Flight, Hotel, Activity, BookingHold, BookingConfirmation, FlightClass, BookingStatus

def search_flights_mock(departure_airport: str, arrival_airport: str, departure_date: date, 
                       return_date: date = None, passengers: int = 1, flight_class: str = "economy") -> Dict[str, Any]:
    """Get mock flight search results"""
    ensure_offline_mode()
    
    # Mock flight data
    base_flights = [
        {
            "airline": "American Airlines", "flight_number": "AA123",
            "departure_time": "08:00", "arrival_time": "14:30", "duration": 390,
            "price_economy": 450, "price_business": 1200, "price_first": 2800
        },
        {
            "airline": "Delta", "flight_number": "DL456", 
            "departure_time": "12:15", "arrival_time": "18:45", "duration": 390,
            "price_economy": 425, "price_business": 1150, "price_first": 2650
        },
        {
            "airline": "United", "flight_number": "UA789",
            "departure_time": "16:30", "arrival_time": "22:55", "duration": 385,
            "price_economy": 475, "price_business": 1300, "price_first": 3000
        }
    ]
    
    flights = []
    for i, base_flight in enumerate(base_flights):
        departure_dt = datetime.combine(departure_date, datetime.strptime(base_flight["departure_time"], "%H:%M").time())
        arrival_dt = datetime.combine(departure_date, datetime.strptime(base_flight["arrival_time"], "%H:%M").time())
        
        price_key = f"price_{flight_class.lower()}"
        price = base_flight.get(price_key, base_flight["price_economy"])
        
        flight = Flight(
            flight_id=f"flight_{i+1}_{departure_airport}_{arrival_airport}",
            airline=base_flight["airline"],
            flight_number=base_flight["flight_number"],
            departure_airport=departure_airport,
            arrival_airport=arrival_airport,
            departure_time=departure_dt,
            arrival_time=arrival_dt,
            duration_minutes=base_flight["duration"],
            flight_class=FlightClass(flight_class.lower()),
            price_usd=price * passengers,
            seats_available=15,
            baggage_included={"carry_on": "1 piece", "checked": "1 piece (23kg)"},
            cancellation_policy="Free cancellation within 24 hours"
        )
        flights.append(flight.dict())
    
    return {
        "departure_airport": departure_airport,
        "arrival_airport": arrival_airport,
        "departure_date": departure_date.isoformat(),
        "return_date": return_date.isoformat() if return_date else None,
        "passengers": passengers,
        "flight_class": flight_class,
        "flights": flights,
        "source": MOCK_SOURCES["flights"],
        "mock_data": True
    }

def search_hotels_mock(city: str, country: str, check_in_date: date, check_out_date: date, 
                      guests: int = 1, rooms: int = 1) -> Dict[str, Any]:
    """Get mock hotel search results"""
    ensure_offline_mode()
    
    nights = (check_out_date - check_in_date).days
    
    # Mock hotel data
    base_hotels = [
        {
            "name": f"Grand {city} Hotel", "rating": 4.5, "price_per_night": 180,
            "amenities": ["WiFi", "Pool", "Gym", "Restaurant", "Concierge"]
        },
        {
            "name": f"{city} Business Inn", "rating": 4.0, "price_per_night": 125,
            "amenities": ["WiFi", "Business Center", "Restaurant", "Parking"]
        },
        {
            "name": f"Budget Stay {city}", "rating": 3.5, "price_per_night": 85,
            "amenities": ["WiFi", "24h Front Desk"]
        }
    ]
    
    hotels = []
    for i, base_hotel in enumerate(base_hotels):
        total_price = base_hotel["price_per_night"] * nights * rooms
        
        hotel = Hotel(
            hotel_id=f"hotel_{i+1}_{city.lower().replace(' ', '_')}",
            name=base_hotel["name"],
            address=f"{100 + i*50} Main Street",
            city=city,
            country=country,
            rating_stars=base_hotel["rating"],
            price_per_night_usd=base_hotel["price_per_night"],
            total_price_usd=total_price,
            amenities=base_hotel["amenities"],
            cancellation_policy="Free cancellation until 6 PM on arrival day",
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            room_type="Standard Room"
        )
        hotels.append(hotel.dict())
    
    return {
        "city": city,
        "country": country, 
        "check_in_date": check_in_date.isoformat(),
        "check_out_date": check_out_date.isoformat(),
        "guests": guests,
        "rooms": rooms,
        "nights": nights,
        "hotels": hotels,
        "source": MOCK_SOURCES["hotels"],
        "mock_data": True
    }

def search_activities_mock(location: str, activity_date: date, categories: List[str] = None, 
                          max_price_usd: float = None) -> Dict[str, Any]:
    """Get mock activity search results"""
    ensure_offline_mode()
    
    # Mock activity data
    base_activities = [
        {
            "name": f"{location} City Walking Tour", "description": "3-hour guided walking tour",
            "duration": 3, "price": 35, "categories": ["cultural", "walking", "historic"]
        },
        {
            "name": f"{location} Museum Pass", "description": "Full day access to top museums",
            "duration": 8, "price": 45, "categories": ["museum", "cultural", "art"]
        },
        {
            "name": f"{location} Food Tour", "description": "Taste local cuisine with a guide",
            "duration": 4, "price": 75, "categories": ["food", "cultural", "walking"]
        },
        {
            "name": f"{location} Bike Tour", "description": "Explore the city by bicycle",
            "duration": 2.5, "price": 40, "categories": ["outdoor", "cycling", "sightseeing"]
        }
    ]
    
    activities = []
    for i, base_activity in enumerate(base_activities):
        # Filter by categories if specified
        if categories and not any(cat in base_activity["categories"] for cat in categories):
            continue
        
        # Filter by price if specified
        if max_price_usd and base_activity["price"] > max_price_usd:
            continue
        
        activity = Activity(
            activity_id=f"activity_{i+1}_{location.lower().replace(' ', '_')}",
            name=base_activity["name"],
            description=base_activity["description"],
            location=location,
            duration_hours=base_activity["duration"],
            price_per_person_usd=base_activity["price"],
            max_participants=20,
            available_slots=12,
            categories=base_activity["categories"],
            cancellation_policy="Free cancellation up to 2 hours before start",
            booking_date=activity_date,
            start_time="10:00"
        )
        activities.append(activity.dict())
    
    return {
        "location": location,
        "date": activity_date.isoformat(),
        "categories_filter": categories or [],
        "max_price_filter": max_price_usd,
        "activities": activities,
        "source": MOCK_SOURCES["activities"],
        "mock_data": True
    }

def hold_booking_mock(booking_type: str, item_id: str, passenger_details: Dict[str, Any] = None) -> Dict[str, Any]:
    """Create a mock booking hold"""
    ensure_offline_mode()
    
    hold_id = str(uuid.uuid4())
    hold_expires_at = datetime.now() + timedelta(minutes=15)  # 15 minute hold
    
    # Mock prices by booking type
    mock_prices = {
        "flight": 450.0,
        "hotel": 540.0,  # 3 nights * 180
        "activity": 35.0
    }
    
    hold = BookingHold(
        hold_id=hold_id,
        booking_type=booking_type,
        item_id=item_id,
        hold_expires_at=hold_expires_at,
        total_price_usd=mock_prices.get(booking_type, 100.0),
        cancellation_policy="Free cancellation within hold period",
        special_terms="Hold expires in 15 minutes. Payment required to confirm."
    )
    
    # Store in mock session storage
    BOOKING_SESSIONS[hold_id] = hold.dict()
    
    return {
        "hold_details": hold.dict(),
        "hold_expires_in_minutes": 15,
        "next_step": "Call confirm_booking with this hold_id to complete booking",
        "mock_data": True
    }

def confirm_booking_mock(hold_id: str, payment_info: Dict[str, str]) -> Dict[str, Any]:
    """Confirm a mock booking"""
    ensure_offline_mode()
    
    # Check if hold exists
    if hold_id not in BOOKING_SESSIONS:
        return {
            "error": "Hold not found or expired",
            "hold_id": hold_id,
            "mock_data": True
        }
    
    hold_data = BOOKING_SESSIONS[hold_id]
    
    # Check if hold expired
    if datetime.now() > datetime.fromisoformat(hold_data["hold_expires_at"]):
        del BOOKING_SESSIONS[hold_id]
        return {
            "error": "Hold has expired",
            "hold_id": hold_id,
            "mock_data": True
        }
    
    # Create confirmation
    confirmation_id = f"CONF_{str(uuid.uuid4())[:8].upper()}"
    
    confirmation = BookingConfirmation(
        confirmation_id=confirmation_id,
        booking_type=hold_data["booking_type"],
        item_id=hold_data["item_id"],
        status=BookingStatus.CONFIRMED,
        total_price_usd=hold_data["total_price_usd"],
        booking_date=datetime.now(),
        contact_info={
            "email": "booking-confirmations@deepseektravels.com",
            "phone": "+1-800-TRAVEL"
        },
        special_instructions="This is a mock booking confirmation for development purposes"
    )
    
    # Remove from holds, add to confirmed bookings
    del BOOKING_SESSIONS[hold_id]
    BOOKING_SESSIONS[confirmation_id] = confirmation.dict()
    
    return {
        "confirmation": confirmation.dict(),
        "payment_processed": True,
        "payment_method": payment_info.get("method", "credit_card"),
        "mock_data": True,
        "important_note": "This is a MOCK booking. No real reservation was made."
    }