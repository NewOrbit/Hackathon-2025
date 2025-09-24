# Restaurants MCP Server

A comprehensive Model Context Protocol (MCP) server for restaurant discovery, menu browsing, and reservation booking. This service provides detailed restaurant information with nutritional data for restaurants in London, Paris, and Rome, designed to integrate with nutrition and macro tracking services.

## Features

### 🍽️ Restaurant Discovery
- Browse restaurants by location (London, Paris, Rome)
- Search by cuisine type, price range, and rating
- Detailed restaurant information including hours, contact details, and special features

### 📋 Menu & Nutrition
- Complete menu items with detailed nutritional information
- Ingredient-level nutritional breakdown (calories, protein, carbs, fat, fiber)
- Allergen and dietary restriction information
- Search and filter menu items by nutritional criteria

### 📅 Reservation System
- Book restaurant reservations with availability checking
- Manage reservations (view, cancel)
- Support for special requests and dietary accommodations

### 🔗 Integration Ready
- Designed to integrate with macros-mcp for nutritional analysis
- Compatible with nutritional-plan-mcp for meal planning
- Works with trivia-mcp for nutrition education

## Installation

```bash
# Install dependencies
uv sync

# Run the server
uv run mcp dev main.py
```

## Available Tools

### Restaurant Discovery
- `get_restaurants(location)` - Get restaurants by city
- `search_restaurants_tool(location, cuisine_type, price_range, rating_min)` - Search with filters
- `get_restaurant_details(restaurant_id)` - Get detailed restaurant information

### Menu & Nutrition
- `get_restaurant_menu_tool(restaurant_id)` - Get complete menu with nutritional data
- `search_menu_items_tool(restaurant_id, category, max_calories, dietary_tags, allergen_free)` - Search menu items

### Reservations
- `book_restaurant_reservation(restaurant_id, customer_name, email, phone, date, time, party_size, special_requests)` - Book a reservation
- `get_reservation_details(reservation_id)` - Get reservation information
- `cancel_restaurant_reservation(reservation_id)` - Cancel a reservation
- `get_restaurant_availability_tool(restaurant_id, date)` - Check available time slots

## Available Resources

- `restaurants://{restaurant_id}` - Formatted restaurant information
- `restaurants://menu/{restaurant_id}` - Formatted menu with nutritional data

## Available Prompts

- `restaurant_booking_prompt(location, cuisine_type)` - Restaurant booking assistance
- `nutrition_restaurant_prompt(restaurant_id, dietary_goals)` - Nutrition-focused guidance

## Sample Data

The service includes hardcoded data for restaurants in London, Paris, and Rome:

### London Restaurants
- **The Ivy** - Classic British cuisine ($$$$, 4.5★)
- **Dishoom** - Bombay-style Indian street food ($$, 4.3★)

### Paris Restaurants
- **L'Atelier de Joël Robuchon** - Michelin-starred French cuisine ($$$$, 4.7★)
- **Le Comptoir du Relais** - Traditional French bistro ($$$, 4.2★)

### Rome Restaurants
- **Roscioli** - Historic Roman trattoria with traditional cuisine ($$$, 4.6★)
- **Armando al Pantheon** - Family-run trattoria near the Pantheon ($$, 4.4★)

## Nutritional Data Structure

Each menu item includes:
- **Macronutrients**: Calories, protein, carbohydrates, fat, fiber
- **Ingredients**: Detailed breakdown with nutritional values per ingredient
- **Allergens**: Comprehensive allergen information
- **Dietary Tags**: Vegetarian, vegan, gluten-free, etc.
- **Preparation Info**: Cooking time and spice level

## Integration Examples

### With Macros MCP
```python
# Get menu item nutritional data
menu_item = get_restaurant_menu_tool("london_1")
# Use macros-mcp to analyze nutritional content
macros_analysis = analyze_macros(menu_item["description"])
```

### With Nutritional Plan MCP
```python
# Search for low-calorie options
low_calorie_items = search_menu_items_tool(
    restaurant_id="paris_1",
    max_calories=500,
    dietary_tags=["vegetarian"]
)
# Integrate with meal planning
```

## Configuration

The server runs on port 8014 by default. To change the port, modify the `FastMCP` initialization in `main.py`.

## Development

### Project Structure
```
restaurants-mcp/
├── main.py                 # MCP server implementation
├── models.py              # Data models and structures
├── restaurant_data.py     # Hardcoded restaurant data
├── restaurant_service.py  # Business logic and operations
├── pyproject.toml         # Dependencies and configuration
└── README.md              # This file
```

### Adding New Restaurants
1. Add restaurant data to `restaurant_data.py`
2. Include detailed menu items with nutritional information
3. Update the data models if needed

### Extending Functionality
- Add new tools in `main.py`
- Implement business logic in `restaurant_service.py`
- Update data models in `models.py` as needed

## License

This project is part of the Hackathon 2025 MCP services ecosystem.