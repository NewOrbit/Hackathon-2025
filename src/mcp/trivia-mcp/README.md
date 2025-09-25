# Trivia MCP Server

Local secrets and insider information about attractions and locations.

## Features

- **Local Secrets**: Hidden information about attractions that only locals know
- **Celebrity Sightings**: Famous people spotted at locations with juicy details
- **Insider Tips**: Best times to visit, secret spots, and local customs
- **In-Memory Database**: Fast access to curated secrets and tips

## Available Attractions

- `space_needle` - Seattle's iconic tower
- `pike_place` - Seattle's famous market
- `golden_gate_bridge` - San Francisco's landmark
- `central_park` - New York's urban oasis
- `times_square` - New York's bustling square

## Tools

### `get_attraction_secret(attraction_id)`

Get a random secret, celebrity sighting, or insider tip for an attraction.

### `get_insider_tip(attraction_id, tip_type?)`

Get insider tips, optionally filtered by category (photo, food, timing, access, local).

### `get_celebrity_drama(location)`

Get celebrity sightings and drama for a location.

### `get_all_attraction_secrets(attraction_id)`

Get all secrets, celebrity sightings, and insider tips for an attraction.

### `get_available_attractions()`

Get list of all attractions with secrets available.

## Resources

- `trivia://attraction/{attraction_id}` - All secrets for an attraction
- `trivia://attractions` - List of available attractions

## Prompts

- `attraction_secrets_prompt(attraction_id)` - Discover attraction secrets
- `travel_secrets_prompt(location)` - Uncover location secrets
- `celebrity_hunting_prompt(location)` - Find celebrity drama

## Running the Server

```bash
uv run mcp dev main.py
```

The server will run on port 8012 by default.
