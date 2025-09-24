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
            {"name": "Margherita Pizza", "price": 12.99, "description": "Classic pizza with fresh tomatoes, mozzarella, and basil.", "is_popular": True, "dietary_info": ["vegetarian"]},
            {"name": "Crab and Spinach Pizza", "price": 15.99, "description": "Pizza topped with crab and fresh spinach.", "dietary_info": ["shellfish"]},
            {"name": "Vegan Delight Pizza (GF)", "price": 13.99, "description": "A delicious vegan pizza with a variety of fresh vegetables.", "dietary_info": ["vegan", "gluten-free"]},
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
            {"name": "California Roll", "price": 8.99, "description": "Crab, avocado, and cucumber roll.", "is_popular": True, "dietary_info": ["gluten-free", "shellfish"]},
            {"name": "Spicy Tuna Roll", "price": 9.99, "description": "Tuna with spicy mayo."},
            {"name": "Vegan Avocado Roll (GF)", "price": 7.99, "description": "Fresh avocado roll.", "dietary_info": ["vegan", "gluten-free"]},
            {"name": "Miso Soup", "price": 3.99, "description": "Traditional Japanese soup with tofu and seaweed.", "is_popular": True},
            {"name": "Tempura Udon", "price": 12.99, "description": "Udon noodles with tempura shrimp and vegetables."},
            {"name": "Green Tea Ice Cream", "price": 4.99, "description": "Creamy green tea flavored ice cream.", "dietary_info": ["vegetarian", "gluten-free"]}
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
    }
]