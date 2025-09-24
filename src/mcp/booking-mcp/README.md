# Booking MCP Server

Mock booking service for the DeepseekTravels packing list agent.

## Phase 1: Offline/Mock Mode Only

This server provides **mock data only** and makes no external HTTP calls. All responses are deterministic fixtures designed for development and testing.

## Available Tools

- `search_flights(departure_airport, arrival_airport, departure_date, ...)` - Search for flights
- `search_hotels(city, country, check_in_date, check_out_date, ...)` - Search for hotels  
- `search_activities(location, activity_date, categories, ...)` - Search for activities and tours
- `hold_booking(booking_type, item_id, passenger_details)` - Place temporary hold on booking
- `confirm_booking(hold_id, payment_info)` - Confirm held booking with payment

## Running the Server

```bash
cd src/mcp/booking-mcp
uv run main.py
```

Server will start on `http://localhost:8011/mcp/`

## Environment Variables

- `DEEPSEEKTRAVELS_OFFLINE=true` (enforced in Phase 1)
- `DEEPSEEKTRAVELS_USE_MOCKS=true` (enforced in Phase 1)

## Booking Flow

1. Search for flights/hotels/activities using respective search tools
2. Call `hold_booking` with an item ID from search results (15-minute hold)
3. Present hold details to user for confirmation
4. Call `confirm_booking` with hold ID and payment info to complete booking

## Mock Data Features

- Realistic flight schedules and pricing
- Hotel ratings and amenities
- Activity categories and descriptions
- Hold/confirm workflow with expiration
- Booking confirmation numbers

**⚠️ Important**: This is mock data for development only. No real bookings are made. All confirmations are fake.