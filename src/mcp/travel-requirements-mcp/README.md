# Travel Requirements MCP Server

Mock travel requirements service for the DeepseekTravels packing list agent.

## Phase 1: Offline/Mock Mode Only

This server provides **mock data only** and makes no external HTTP calls. All responses are deterministic fixtures designed for development and testing.

## Available Tools

- `check_baggage_rules(airline, cabin_class, route)` - Get baggage allowances and restrictions
- `check_security_restrictions(departure_country, arrival_country, items)` - Check airport security rules
- `check_visa_requirements(passport_country, destination_country, trip_duration_days, purpose)` - Check visa requirements  
- `check_travel_documents(destination_country, passport_country, departure_date, return_date)` - Check required documents

## Running the Server

```bash
cd src/mcp/travel-requirements-mcp
uv run main.py
```

Server will start on `http://localhost:8010/mcp/`

## Environment Variables

- `DEEPSEEKTRAVELS_OFFLINE=true` (enforced in Phase 1)
- `DEEPSEEKTRAVELS_USE_MOCKS=true` (enforced in Phase 1)

## Mock Data Sources

All data references mock versions of:
- TSA "What Can I Bring?" guidelines
- IATA Travel Centre information  
- Embassy and consulate websites
- Airline baggage policies

**⚠️ Important**: This is mock data for development only. Always verify requirements with official sources before travel.