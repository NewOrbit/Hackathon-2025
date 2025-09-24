"""Booking MCP mocked service layer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Optional

from fixtures import BOOKING_FIXTURES


@dataclass
class BookingRouter:
    fixtures: Dict[str, Dict[str, Any]]

    def search_flights(
        self,
        origin: str,
        destination: str,
        depart_date: str,
        return_date: Optional[str],
        passengers: int,
        cabin_class: str,
    ) -> Dict[str, Any]:
        key = destination.lower()
        data = self.fixtures.get(key, self.fixtures["default"]).copy()
        return {
            "origin": origin,
            "destination": destination,
            "depart_date": depart_date,
            "return_date": return_date,
            "passengers": passengers,
            "cabin_class": cabin_class,
            "flights": data.get("flights", []),
        }

    def search_hotels(
        self,
        destination: str,
        check_in: str,
        check_out: str,
        guests: int,
        budget: Optional[float],
    ) -> Dict[str, Any]:
        key = destination.lower()
        data = self.fixtures.get(key, self.fixtures["default"]).copy()
        return {
            "destination": destination,
            "check_in": check_in,
            "check_out": check_out,
            "guests": guests,
            "budget": budget,
            "hotels": data.get("hotels", []),
        }

    def search_activities(
        self,
        destination: str,
        start_date: str,
        end_date: Optional[str],
        interests: Optional[str],
        budget: Optional[float],
    ) -> Dict[str, Any]:
        key = destination.lower()
        data = self.fixtures.get(key, self.fixtures["default"]).copy()
        return {
            "destination": destination,
            "start_date": start_date,
            "end_date": end_date,
            "interests": interests,
            "budget": budget,
            "activities": data.get("activities", []),
        }

    def hold_booking(self, booking_type: str, booking_payload: Dict[str, Any]) -> Dict[str, Any]:
        hold_id = f"HOLD-{booking_type.upper()}-{booking_payload.get('destination', 'UNKNOWN').upper()}"
        return {
            "hold_id": hold_id,
            "booking_type": booking_type,
            "payload": booking_payload,
            "expires_in_minutes": 30,
        }

    def confirm_booking(self, hold_id: str, confirm: bool) -> Dict[str, Any]:
        status = "confirmed" if confirm else "cancelled"
        return {
            "hold_id": hold_id,
            "status": status,
        }

    def format_summary(self, destination: str) -> str:
        data = self.fixtures.get(destination.lower(), self.fixtures["default"])
        flights = len(data.get("flights", []))
        hotels = len(data.get("hotels", []))
        activities = len(data.get("activities", []))
        return (
            f"Mock booking summary for {destination}: "
            f"{flights} flights, {hotels} hotels, {activities} activities available."
        )

    def get_booking_prompt(self, destination: str) -> str:
        return (
            f"Compose a concise booking pitch for {destination} covering one flight, one hotel,"
            " and an activity, highlighting total estimated budget."
        )


booking_router = BookingRouter(BOOKING_FIXTURES)

