"""Booking MCP server with mocked travel deals."""

from typing import Dict, Any, Optional

from mcp.server.fastmcp import FastMCP

from booking_service import booking_router


mcp = FastMCP("Booking", port=8011)


@mcp.tool()
def search_flights(
    origin: str,
    destination: str,
    depart_date: str,
    return_date: Optional[str] = None,
    passengers: int = 1,
    cabin_class: str = "economy",
) -> Dict[str, Any]:
    """Return mocked flight options."""

    return booking_router.search_flights(
        origin,
        destination,
        depart_date,
        return_date,
        passengers,
        cabin_class,
    )


@mcp.tool()
def search_hotels(
    destination: str,
    check_in: str,
    check_out: str,
    guests: int = 1,
    budget: Optional[float] = None,
) -> Dict[str, Any]:
    """Return mocked hotel options."""

    return booking_router.search_hotels(destination, check_in, check_out, guests, budget)


@mcp.tool()
def search_activities(
    destination: str,
    start_date: str,
    end_date: Optional[str] = None,
    interests: Optional[str] = None,
    budget: Optional[float] = None,
) -> Dict[str, Any]:
    """Return mocked attraction/activity suggestions."""

    return booking_router.search_activities(destination, start_date, end_date, interests, budget)


@mcp.tool()
def hold_booking(booking_type: str, booking_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Create a hold for a booking (mocked)."""

    return booking_router.hold_booking(booking_type, booking_payload)


@mcp.tool()
def confirm_booking(hold_id: str, confirm: bool = False) -> Dict[str, Any]:
    """Confirm or cancel a booking hold."""

    return booking_router.confirm_booking(hold_id, confirm)


@mcp.resource("booking://summary/{destination}")
def get_booking_summary(destination: str) -> str:
    return booking_router.format_summary(destination)


@mcp.prompt()
def booking_pitch_prompt(destination: str) -> str:
    return booking_router.get_booking_prompt(destination)


if __name__ == "__main__":
    mcp.run("streamable-http")

