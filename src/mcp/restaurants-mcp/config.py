import random


RESTAURANTS = [
    {
        "id": "rest_101",
        "name": "Trattoria Roma",
        "cuisine": ["italian"],
        "avg_price": 25,
        "hours": [{"day": "Mon-Sun", "open": "12:00", "close": "22:30"}],
        "menu": [
            {"item": "Margherita Pizza", "price": 16, "diet": ["vegetarian"]},
            {"item": "Spaghetti Carbonara", "price": 18, "diet": []}
        ],
        "location": "Los Angeles",
        "venues": ["outdoor"]
    },
    {
        "id": "rest_102",
        "name": "Dragon Wok",
        "cuisine": ["chinese"],
        "avg_price": 20,
        "hours": [{"day": "Tue-Sun", "open": "11:00", "close": "23:00"}],
        "menu": [
            {"item": "Kung Pao Chicken", "price": 17, "diet": []},
            {"item": "Vegetable Dumplings", "price": 12, "diet": ["vegan"]}
        ],
        "location": "Los Angeles",
        "venues": ["indoor"]
    },
    {
        "id": "rest_103",
        "name": "Sakura House",
        "cuisine": ["japanese"],
        "avg_price": 30,
        "hours": [{"day": "Daily", "open": "12:00", "close": "21:30"}],
        "menu": [
            {"item": "Sushi Platter", "price": 28, "diet": []},
            {"item": "Miso Soup", "price": 8, "diet": ["vegan"]}
        ],
        "location": "Los Angeles",
        "venues": ["indoor", "outdoor"]
    },
    {
        "id": "rest_104",
        "name": "Curry Mahal",
        "cuisine": ["indian"],
        "avg_price": 22,
        "hours": [{"day": "Wed-Mon", "open": "11:30", "close": "22:00"}],
        "menu": [
            {"item": "Butter Chicken", "price": 20, "diet": []},
            {"item": "Chana Masala", "price": 16, "diet": ["vegan", "gluten-free"]}
        ],
        "location": "Tasiilaq",
        "venues": ["indoor"]
    },
    {
        "id": "rest_105",
        "name": "Bangkok Spice",
        "cuisine": ["thai"],
        "avg_price": 19,
        "hours": [{"day": "Mon-Sat", "open": "12:00", "close": "23:00"}],
        "menu": [
            {"item": "Pad Thai", "price": 15, "diet": ["gluten-free"]},
            {"item": "Green Curry", "price": 17, "diet": []}
        ],
        "location": "Tasiilaq",
        "venues": ["outdoor"]
    },
    {
        "id": "rest_106",
        "name": "Cantina Mexicana",
        "cuisine": ["mexican"],
        "avg_price": 21,
        "hours": [{"day": "Daily", "open": "11:00", "close": "22:30"}],
        "menu": [
            {"item": "Tacos al Pastor", "price": 14, "diet": []},
            {"item": "Vegetarian Quesadilla", "price": 13, "diet": ["vegetarian"]}
        ],
        "location": "Tasiilaq",
        "venues": ["indoor", "outdoor"]
    },
    # Add the rest of the restaurants here with the same pattern
]


CUISINES = {cuisine: cuisine.capitalize() for restaurant in RESTAURANTS for cuisine in restaurant["cuisine"]}

LOCATIONS = {restaurant["location"]: restaurant["location"] for restaurant in RESTAURANTS}