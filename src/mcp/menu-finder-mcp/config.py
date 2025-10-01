"""
Restaurant menus MCP configuration mocks data.
"""
MOCK_MENUS = [
    {
        "id": 1,
        "name": "The Gourmet Kitchen",
        "location": "123 Food St, Flavor Town",
        "cuisine": "Italian",
        "menu_items": [
            {"name": "Margherita Pizza", "price": 12.99, "size": "12in", "description": "Classic pizza with fresh tomatoes, mozzarella, and basil.", "is_popular": True, "dietary_info": ["vegetarian"]},
            {"name": "Crab and Spinach Pizza", "price": 15.99, "size": "12in", "description": "Pizza topped with crab and fresh spinach.", "dietary_info": ["shellfish"]},
            {"name": "Vegan Delight Pizza (GF)", "price": 13.99, "size": "12in", "description": "A delicious vegan pizza with a variety of fresh vegetables.", "dietary_info": ["vegan", "gluten-free"]},
            {"name": "Caprese Salad", "price": 10.99, "description": "Fresh mozzarella, tomatoes, and basil."},
            {"name": "Pasta Carbonara", "price": 14.99, "description": "Creamy pasta with pancetta and parmesan.", "is_popular": True},
            {"name": "Tiramisu", "price": 6.99, "description": "Classic Italian dessert with mascarpone and coffee."}
        ]
    },
    {
        "id": 2,
        "name": "Sushi World",
        "location": "456 Ocean Ave, Seaside City",
        "cuisine": "Japanese",
        "menu_items": [
            {"name": "California Roll", "price": 8.99, "size": "4 rolls", "description": "Crab, avocado, and cucumber roll.", "is_popular": True, "dietary_info": ["gluten-free", "shellfish"]},
            {"name": "Spicy Tuna Roll", "price": 9.99, "size": "4 rolls", "description": "Tuna with spicy mayo."},
            {"name": "Vegan Avocado Roll (GF)", "price": 7.99, "size": "6 rolls", "description": "Fresh avocado roll.", "dietary_info": ["vegan", "gluten-free"]},
            {"name": "Miso Soup", "price": 3.99, "description": "Traditional Japanese soup with tofu and seaweed.", "is_popular": True},
            {"name": "Tempura Udon", "price": 12.99, "description": "Udon noodles with tempura shrimp and vegetables."},
            {"name": "Green Tea Ice Cream", "price": 4.99, "size": "2 scoops", "description": "Creamy green tea flavored ice cream.", "dietary_info": ["vegetarian", "gluten-free"]}
        ]
    },
    {
        "id": 3,
        "name": "Just Desserts",
        "location": "789 Sweet St, Candy City",
        "cuisine": "Desserts",
        "menu_items": [
            {"name": "Chocolate Lava Cake", "price": 7.99, "description": "Warm chocolate cake with a gooey center.", "is_popular": True, "dietary_info": ["vegetarian"]},
            {"name": "Strawberry Cheesecake", "price": 6.99, "description": "Classic cheesecake topped with fresh strawberries."},
            {"name": "Vegan Chocolate Mousse (GF)", "price": 5.99, "description": "Rich chocolate mousse made with avocado.", "dietary_info": ["vegan", "gluten-free"]},
            {"name": "Ice Cream Sundae", "price": 4.99, "description": "Vanilla ice cream with chocolate sauce and whipped cream.", "is_popular": True},
            {"name": "Fruit Tart", "price": 5.49, "description": "Tart filled with custard and topped with fresh fruit."}
        ],
    },
    {
        "id": 4,
        "name": "Cantina Mexicana",
        "location": "321 Fiesta Rd, Spicy Town",
        "cuisine": "Mexican",
        "menu_items": [
            {"name": "Tacos al Pastor", "price": 9.99, "size": "3 tacos", "description": "Marinated pork tacos with pineapple.", "is_popular": True},
            {"name": "Chicken Quesadilla", "price": 8.99, "size": "1 quesadilla", "description": "Grilled chicken with cheese in a flour tortilla."},
            {"name": "Vegan Burrito Bowl (GF)", "price": 10.99, "description": "Rice bowl with beans, vegetables, and guacamole.", "dietary_info": ["vegan", "gluten-free"]},
            {"name": "Churros", "price": 4.99, "description": "Fried dough pastries rolled in cinnamon sugar.", "is_popular": True, "dietary_info": ["vegetarian"]},
            {"name": "Guacamole and Chips", "price": 5.99, "description": "Fresh guacamole served with tortilla chips."}
        ]
    },
    {
        "id": 5,
        "name": "Finch's Fish and Chips",
        "location": "654 Harbor Blvd, Bay City",
        "cuisine": "Seafood",
        "menu_items": [
            {"name": "Cod Fish and Chips", "price": 11.99, "description": "Battered cod served with fries.", "is_popular": True},
            {"name": "Shrimp Basket", "price": 10.99, "size": "10 pieces", "description": "Fried shrimp served with cocktail sauce.", "dietary_info": ["shellfish"]},
            {"name": "Vegan Fish and Chips (GF)", "price": 12.99, "description": "Battered tofu served with fries.", "dietary_info": ["vegan", "gluten-free"]},
            {"name": "Chicken and Chips", "price": 9.99, "description": "Battered chicken served with fries.", "is_popular": True},
            {"name": "Chicken Curry Sauce", "price": 2.99, "size": "M", "description": "Spicy curry sauce for dipping."},
            {"name": "Chicken Curry Sauce", "price": 3.99, "size": "L", "description": "Spicy curry sauce for dipping."}
        ]
    }
]