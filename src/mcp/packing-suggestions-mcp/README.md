# Packing Lists MCP Server

MCP server for generating comprehensive packing lists for various activities with weather-based recommendations.

## Features

- Generate packing lists for 20+ activities including hiking, camping, beach trips, business travel, and more
- Weather-based recommendations with cold weather and rain addons
- Customizable temperature thresholds
- Activity-specific base items with optional weather enhancements

## Activities Supported

- Outdoor: day_hike, multi_day_hike, camping, beach_trip, skiing, cycling
- Travel: business_travel, city_break, backpacking, road_trip
- Adventure: rock_climbing, kayaking, surfing, photography
- Indoor: conference, wedding, gym_workout, yoga
- And many more...

## Usage

To run this server:
```bash
uv run mcp dev main.py
```

The server will run on port 8010 by default.

## Tools

### get_packing_list
Generate a comprehensive packing list for a specific activity with weather considerations.

**Parameters:**
- `activity` (str): The activity type (e.g., "day_hike", "beach_trip", "business_travel")
- `cold_threshold_c` (int, optional): Temperature threshold in Celsius below which cold items are added (default: 10°C)
- `expect_rain` (bool, optional): Whether to include rain items regardless of temperature (default: false)

**Returns:**
A packing list object with:
- Activity name
- Base items (always included)
- Cold weather threshold and items
- Rain protection items

### list_activities
Get a list of all supported activities with descriptions.

**Returns:**
A list of supported activities with brief descriptions of each.

## Example Response

```json
{
  "activity": "day_hike",
  "base_items": ["daypack", "water bottle", "snacks", "first aid kit", "map/GPS", "headlamp"],
  "cold_threshold_c": 10,
  "cold_items": ["insulated jacket", "beanie", "gloves", "warm layers"],
  "rain_items": ["rain shell", "pack cover", "waterproof boots"]
}
```