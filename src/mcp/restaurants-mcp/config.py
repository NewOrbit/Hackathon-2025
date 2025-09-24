MOCK_RESTAURANTS = [
    {
        "id": "rest_101",
        "name": "Green Bowl",
        "cuisine": "healthy",
        "location": "New York",
        "average_price": 25.0,
        "rating": 4.2,
        "opens_at": 700,
        "closes_at": 2100
    },
    {
        "id": "rest_102",
        "name": "Pizza Palace",
        "cuisine": "italian",
        "location": "New York",
        "average_price": 15.0,
        "rating": 3.8,
        "opens_at": 700,
        "closes_at": 2300
    },
    {
        "id": "rest_103",
        "name": "Sushi Central",
        "cuisine": "japanese",
        "location": "New York",
        "average_price": 65.0,
        "rating": 4.6,
        "opens_at": 1700,
        "closes_at": 2200
    },
    {
        "id": "rest_104",
        "name": "Burger Haven",
        "cuisine": "american",
        "location": "Chicago",
        "average_price": 18.0,
        "rating": 4.1,
        "opens_at": 1000,
        "closes_at": 2400
    },
    {
        "id": "rest_105",
        "name": "Taco Town",
        "cuisine": "mexican",
        "location": "New York",
        "average_price": 12.0,
        "rating": 4.3,
        "opens_at": 1100,
        "closes_at": 2200
    },
    {
        "id": "rest_106",
        "name": "Pasta Point",
        "cuisine": "italian",
        "location": "Chicago",
        "average_price": 28.0,
        "rating": 3.9,
        "opens_at": 1600,
        "closes_at": 2200
    },
    {
        "id": "rest_107",
        "name": "Curry Corner",
        "cuisine": "indian",
        "location": "Chicago",
        "average_price": 22.0,
        "rating": 4.4,
        "opens_at": 1200,
        "closes_at": 2200
    },
    {
        "id": "rest_108",
        "name": "BBQ Barn",
        "cuisine": "american",
        "location": "Chicago",
        "average_price": 45.0,
        "rating": 4.7,
        "opens_at": 1600,
        "closes_at": 2300
    },
    {
        "id": "rest_109",
        "name": "Falafel Factory",
        "cuisine": "mediterranean",
        "location": "Seattle",
        "average_price": 14.0,
        "rating": 4.0,
        "opens_at": 1000,
        "closes_at": 2100
    },
    {
        "id": "rest_110",
        "name": "Noodle Nest",
        "cuisine": "asian",
        "location": "Seattle",
        "average_price": 20.0,
        "rating": 3.7,
        "opens_at": 1130,
        "closes_at": 2230
    }
]

MOCK_MENUS = [
    {
        "restaurant_id": "rest_101",
        "restaurant_name": "Green Bowl",
        "menu_items": [
            {
                "id": "item_rest_101_001",
                "name": "Quinoa Power Bowl",
                "description": "Quinoa, kale, avocado, chickpeas, and tahini dressing",
                "price": 18.50,
                "category": "bowls",
                "dietary_info": ["vegetarian", "gluten-free"]
            },
            {
                "id": "item_rest_101_002",
                "name": "Grilled Salmon Salad",
                "description": "Fresh salmon over mixed greens with lemon vinaigrette",
                "price": 24.00,
                "category": "salads",
                "dietary_info": ["pescatarian", "keto-friendly"]
            },
            {
                "id": "item_rest_101_003",
                "name": "Green Smoothie",
                "description": "Spinach, banana, mango, and coconut water",
                "price": 8.50,
                "category": "beverages",
                "dietary_info": ["vegan", "raw"]
            }
        ]
    },
    {
        "restaurant_id": "rest_102",
        "restaurant_name": "Pizza Palace",
        "menu_items": [
            {
                "id": "item_rest_102_001",
                "name": "Margherita Pizza",
                "description": "Classic tomato, mozzarella, and fresh basil",
                "price": 16.00,
                "category": "pizza",
                "dietary_info": ["vegetarian"]
            },
            {
                "id": "item_rest_102_002",
                "name": "Pepperoni Supreme",
                "description": "Pepperoni, mushrooms, bell peppers, and extra cheese",
                "price": 19.50,
                "category": "pizza",
                "dietary_info": []
            },
            {
                "id": "item_rest_102_003",
                "name": "Caesar Salad",
                "description": "Romaine lettuce, parmesan, croutons, and Caesar dressing",
                "price": 12.00,
                "category": "salads",
                "dietary_info": ["vegetarian"]
            }
        ]
    },
    {
        "restaurant_id": "rest_103",
        "restaurant_name": "Sushi Central",
        "menu_items": [
            {
                "id": "item_rest_103_001",
                "name": "Omakase Tasting Menu",
                "description": "Chef's selection of 12 pieces of premium sushi",
                "price": 85.00,
                "category": "tasting_menu",
                "dietary_info": ["pescatarian"]
            },
            {
                "id": "item_rest_103_002",
                "name": "Dragon Roll",
                "description": "Eel, cucumber, topped with avocado and eel sauce",
                "price": 18.50,
                "category": "specialty_rolls",
                "dietary_info": ["pescatarian"]
            },
            {
                "id": "item_rest_103_003",
                "name": "Miso Soup",
                "description": "Traditional soybean paste soup with tofu and seaweed",
                "price": 6.00,
                "category": "appetizers",
                "dietary_info": ["vegetarian", "vegan"]
            }
        ]
    },
    {
        "restaurant_id": "rest_104",
        "restaurant_name": "Burger Haven",
        "menu_items": [
            {
                "id": "item_rest_104_001",
                "name": "Classic Cheeseburger",
                "description": "Beef patty, cheese, lettuce, tomato, onion, and pickles",
                "price": 16.50,
                "category": "burgers",
                "dietary_info": []
            },
            {
                "id": "item_rest_104_002",
                "name": "Truffle Fries",
                "description": "Hand-cut fries with truffle oil and parmesan",
                "price": 12.00,
                "category": "sides",
                "dietary_info": ["vegetarian"]
            },
            {
                "id": "item_rest_104_003",
                "name": "Chocolate Milkshake",
                "description": "Rich chocolate shake topped with whipped cream",
                "price": 8.50,
                "category": "beverages",
                "dietary_info": ["vegetarian"]
            }
        ]
    },
    {
        "restaurant_id": "rest_105",
        "restaurant_name": "Taco Town",
        "menu_items": [
            {
                "id": "item_rest_105_001",
                "name": "Carnitas Tacos",
                "description": "Slow-cooked pork with onions, cilantro, and lime",
                "price": 11.50,
                "category": "tacos",
                "dietary_info": []
            },
            {
                "id": "item_rest_105_002",
                "name": "Vegetarian Burrito Bowl",
                "description": "Black beans, rice, peppers, guac, and cheese",
                "price": 13.00,
                "category": "bowls",
                "dietary_info": ["vegetarian"]
            },
            {
                "id": "item_rest_105_003",
                "name": "Horchata",
                "description": "Traditional rice and cinnamon drink",
                "price": 4.50,
                "category": "beverages",
                "dietary_info": ["vegetarian"]
            }
        ]
    },
    {
        "restaurant_id": "rest_106",
        "restaurant_name": "Pasta Point",
        "menu_items": [
            {
                "id": "item_rest_106_001",
                "name": "Fettuccine Alfredo",
                "description": "Creamy alfredo sauce with fresh fettuccine pasta",
                "price": 22.00,
                "category": "pasta",
                "dietary_info": ["vegetarian"]
            },
            {
                "id": "item_rest_106_002",
                "name": "Chicken Parmigiana",
                "description": "Breaded chicken breast with marinara and mozzarella",
                "price": 28.50,
                "category": "entrees",
                "dietary_info": []
            },
            {
                "id": "item_rest_106_003",
                "name": "Tiramisu",
                "description": "Classic Italian dessert with coffee and mascarpone",
                "price": 9.00,
                "category": "desserts",
                "dietary_info": ["vegetarian"]
            }
        ]
    },
    {
        "restaurant_id": "rest_107",
        "restaurant_name": "Curry Corner",
        "menu_items": [
            {
                "id": "item_rest_107_001",
                "name": "Butter Chicken",
                "description": "Tender chicken in creamy tomato-based curry sauce",
                "price": 19.50,
                "category": "curries",
                "dietary_info": []
            },
            {
                "id": "item_rest_107_002",
                "name": "Vegetable Biryani",
                "description": "Fragrant basmati rice with mixed vegetables and spices",
                "price": 16.00,
                "category": "rice_dishes",
                "dietary_info": ["vegetarian", "vegan"]
            },
            {
                "id": "item_rest_107_003",
                "name": "Garlic Naan",
                "description": "Fresh baked bread with garlic and cilantro",
                "price": 4.50,
                "category": "breads",
                "dietary_info": ["vegetarian"]
            }
        ]
    },
    {
        "restaurant_id": "rest_108",
        "restaurant_name": "BBQ Barn",
        "menu_items": [
            {
                "id": "item_rest_108_001",
                "name": "Smoked Brisket Platter",
                "description": "12-hour smoked brisket with coleslaw and cornbread",
                "price": 32.00,
                "category": "bbq_platters",
                "dietary_info": []
            },
            {
                "id": "item_rest_108_002",
                "name": "Pulled Pork Sandwich",
                "description": "Slow-smoked pork with BBQ sauce on brioche bun",
                "price": 18.50,
                "category": "sandwiches",
                "dietary_info": []
            },
            {
                "id": "item_rest_108_003",
                "name": "Mac and Cheese",
                "description": "Creamy three-cheese mac with bacon crumbles",
                "price": 14.00,
                "category": "sides",
                "dietary_info": ["vegetarian"]
            }
        ]
    },
    {
        "restaurant_id": "rest_109",
        "restaurant_name": "Falafel Factory",
        "menu_items": [
            {
                "id": "item_rest_109_001",
                "name": "Falafel Wrap",
                "description": "Crispy falafel with hummus, tahini, and fresh vegetables",
                "price": 12.50,
                "category": "wraps",
                "dietary_info": ["vegetarian", "vegan"]
            },
            {
                "id": "item_rest_109_002",
                "name": "Mediterranean Platter",
                "description": "Hummus, baba ganoush, olives, and pita bread",
                "price": 16.00,
                "category": "platters",
                "dietary_info": ["vegetarian", "vegan"]
            },
            {
                "id": "item_rest_109_003",
                "name": "Baklava",
                "description": "Flaky phyllo pastry with honey and pistachios",
                "price": 6.50,
                "category": "desserts",
                "dietary_info": ["vegetarian"]
            }
        ]
    },
    {
        "restaurant_id": "rest_110",
        "restaurant_name": "Noodle Nest",
        "menu_items": [
            {
                "id": "item_rest_110_001",
                "name": "Pad Thai",
                "description": "Stir-fried rice noodles with shrimp, tofu, and peanuts",
                "price": 17.50,
                "category": "noodles",
                "dietary_info": ["pescatarian"]
            },
            {
                "id": "item_rest_110_002",
                "name": "Ramen Bowl",
                "description": "Rich pork broth with fresh noodles and soft-boiled egg",
                "price": 21.00,
                "category": "soups",
                "dietary_info": []
            },
            {
                "id": "item_rest_110_003",
                "name": "Spring Rolls",
                "description": "Fresh vegetables wrapped in rice paper with peanut sauce",
                "price": 8.50,
                "category": "appetizers",
                "dietary_info": ["vegetarian", "vegan"]
            }
        ]
    }
]