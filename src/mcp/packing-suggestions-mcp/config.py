"""
Configuration constants for the packing lists MCP server.
"""

# Default cold weather threshold in Celsius
DEFAULT_COLD_THRESHOLD_C = 10

# Activity categories
ACTIVITY_CATEGORIES = [
    "outdoor",
    "travel", 
    "adventure",
    "indoor",
    "sports",
    "professional"
]

# Comprehensive packing list data for different activities
PACKING_LISTS = {
    "day_hike": {
        "description": "Single day hiking adventure",
        "category": "outdoor",
        "typical_duration": "4-8 hours",
        "base_items": [
            "daypack",
            "water bottle",
            "snacks/energy bars",
            "first aid kit",
            "map/GPS device",
            "headlamp/flashlight",
            "sunscreen",
            "sunglasses",
            "hiking boots",
            "moisture-wicking shirt",
            "hiking pants/shorts"
        ],
        "cold_items": [
            "insulated jacket",
            "beanie/warm hat",
            "gloves",
            "warm layers",
            "thermal underwear"
        ],
        "rain_items": [
            "rain shell/jacket",
            "pack cover",
            "waterproof boots",
            "rain pants"
        ]
    },
    
    "multi_day_hike": {
        "description": "Multi-day hiking expedition with overnight camping",
        "category": "outdoor",
        "typical_duration": "2-7 days",
        "base_items": [
            "backpack (40-65L)",
            "tent",
            "sleeping bag",
            "sleeping pad",
            "camp stove",
            "cookware",
            "water filter/purification",
            "food for all days",
            "first aid kit",
            "map/GPS",
            "headlamp + extra batteries",
            "hiking boots",
            "multiple clothing sets"
        ],
        "cold_items": [
            "winter sleeping bag",
            "insulated jacket",
            "warm hat",
            "gloves",
            "thermal layers",
            "warm socks"
        ],
        "rain_items": [
            "waterproof tent",
            "rain gear (jacket/pants)",
            "pack cover",
            "waterproof stuff sacks"
        ]
    },
    
    "camping": {
        "description": "Car camping or established campground stay",
        "category": "outdoor", 
        "typical_duration": "1-3 days",
        "base_items": [
            "tent",
            "sleeping bag",
            "sleeping pad/air mattress",
            "pillow",
            "camp chairs",
            "camp table",
            "cooler with ice",
            "camp stove",
            "cookware and utensils",
            "plates/bowls/cups",
            "lantern",
            "firewood/fire starters",
            "first aid kit"
        ],
        "cold_items": [
            "warm sleeping bag",
            "extra blankets",
            "warm clothing",
            "hot beverage supplies"
        ],
        "rain_items": [
            "tarp/canopy",
            "rain gear",
            "waterproof tent",
            "extra tarps"
        ]
    },
    
    "beach_trip": {
        "description": "Relaxing day or vacation at the beach",
        "category": "outdoor",
        "typical_duration": "1 day - 1 week",
        "base_items": [
            "swimwear",
            "beach towels",
            "sunscreen (high SPF)",
            "sunglasses",
            "sun hat",
            "beach umbrella/shelter",
            "water bottle",
            "snacks",
            "beach bag",
            "flip-flops/sandals",
            "waterproof phone case"
        ],
        "cold_items": [
            "light jacket/hoodie",
            "long pants",
            "closed-toe shoes"
        ],
        "rain_items": [
            "beach tent",
            "rain poncho",
            "waterproof bag"
        ]
    },
    
    "business_travel": {
        "description": "Professional travel for meetings, conferences, or work",
        "category": "professional",
        "typical_duration": "2-5 days",
        "base_items": [
            "business suits/formal wear",
            "dress shirts",
            "ties/accessories",
            "dress shoes",
            "laptop and charger",
            "business cards",
            "phone charger",
            "toiletries",
            "underwear/socks",
            "belt",
            "briefcase/laptop bag"
        ],
        "cold_items": [
            "warm coat/overcoat",
            "scarf",
            "gloves",
            "warm business attire"
        ],
        "rain_items": [
            "umbrella",
            "rain coat",
            "waterproof shoe covers"
        ]
    },
    
    "city_break": {
        "description": "Short urban vacation with sightseeing and culture",
        "category": "travel",
        "typical_duration": "2-4 days",
        "base_items": [
            "comfortable walking shoes",
            "day bag/small backpack",
            "camera",
            "phone/charger",
            "city map/guidebook",
            "casual clothing",
            "nice outfit for dining",
            "sunglasses",
            "water bottle",
            "money/cards"
        ],
        "cold_items": [
            "warm jacket",
            "scarf",
            "warm layers"
        ],
        "rain_items": [
            "compact umbrella",
            "rain jacket",
            "waterproof bag"
        ]
    },
    
    "backpacking": {
        "description": "Extended travel with minimal luggage",
        "category": "travel",
        "typical_duration": "weeks to months",
        "base_items": [
            "backpack (50-70L)",
            "quick-dry clothing",
            "comfortable walking shoes",
            "sandals",
            "toiletries",
            "first aid kit",
            "travel documents",
            "money belt",
            "phone/charger",
            "universal adapter",
            "travel towel"
        ],
        "cold_items": [
            "warm jacket",
            "thermal layers",
            "warm hat/gloves"
        ],
        "rain_items": [
            "rain jacket",
            "pack cover",
            "waterproof stuff sacks"
        ]
    },
    
    "skiing": {
        "description": "Alpine or cross-country skiing adventure",
        "category": "sports",
        "typical_duration": "1-7 days",
        "base_items": [
            "skis/boots/poles",
            "helmet",
            "ski goggles",
            "base layers",
            "ski jacket",
            "ski pants",
            "ski gloves",
            "ski socks",
            "après-ski boots",
            "lift tickets",
            "sunscreen",
            "sunglasses"
        ],
        "cold_items": [
            "face mask/balaclava",
            "hand warmers",
            "extra warm layers",
            "insulated jacket"
        ],
        "rain_items": [
            "waterproof ski gear",
            "goggle cleaner"
        ]
    },
    
    "rock_climbing": {
        "description": "Rock climbing adventure, indoor or outdoor",
        "category": "adventure",
        "typical_duration": "4-8 hours",
        "base_items": [
            "climbing shoes",
            "harness",
            "helmet",
            "dynamic rope",
            "quickdraws",
            "belay device",
            "carabiners",
            "chalk bag",
            "approach shoes",
            "first aid kit",
            "headlamp",
            "water",
            "energy snacks"
        ],
        "cold_items": [
            "warm layers",
            "gloves (fingerless)",
            "beanie"
        ],
        "rain_items": [
            "rain shell",
            "waterproof gear bag"
        ]
    },
    
    "kayaking": {
        "description": "Kayaking on rivers, lakes, or ocean",
        "category": "adventure",
        "typical_duration": "3-8 hours",
        "base_items": [
            "kayak and paddle",
            "personal flotation device (PFD)",
            "dry bag",
            "quick-dry clothing",
            "sun hat",
            "sunglasses with strap",
            "sunscreen",
            "water bottle",
            "snacks",
            "whistle",
            "first aid kit"
        ],
        "cold_items": [
            "wetsuit/dry suit",
            "neoprene gloves",
            "thermal layers",
            "warm hat"
        ],
        "rain_items": [
            "rain jacket",
            "waterproof bags",
            "extra dry clothing"
        ]
    },
    
    "conference": {
        "description": "Professional conference or seminar attendance",
        "category": "professional",
        "typical_duration": "1-3 days",
        "base_items": [
            "business casual attire",
            "comfortable shoes",
            "notepad and pens",
            "laptop/tablet",
            "chargers",
            "business cards",
            "name badge holder",
            "water bottle",
            "snacks",
            "blazer/jacket"
        ],
        "cold_items": [
            "warm sweater",
            "scarf",
            "warm jacket"
        ],
        "rain_items": [
            "umbrella",
            "light rain coat"
        ]
    },
    
    "wedding": {
        "description": "Wedding ceremony and reception attendance",
        "category": "indoor",
        "typical_duration": "1 day",
        "base_items": [
            "formal attire",
            "dress shoes",
            "appropriate accessories",
            "clutch/small bag",
            "camera",
            "gift",
            "tissues",
            "phone charger",
            "comfortable backup shoes",
            "makeup touch-up kit"
        ],
        "cold_items": [
            "wrap/shawl",
            "formal coat",
            "tights/hosiery"
        ],
        "rain_items": [
            "umbrella",
            "rain coat",
            "shoe protectors"
        ]
    },
    
    "gym_workout": {
        "description": "Indoor gym or fitness center workout",
        "category": "sports",
        "typical_duration": "1-2 hours",
        "base_items": [
            "workout clothes",
            "athletic shoes",
            "water bottle",
            "towel",
            "earbuds/headphones",
            "gym membership card",
            "protein shake/snack",
            "shower kit",
            "change of clothes",
            "lock for locker"
        ],
        "cold_items": [
            "warm-up jacket",
            "long sleeves"
        ],
        "rain_items": [
            "umbrella",
            "rain jacket for travel"
        ]
    },
    
    "photography": {
        "description": "Photography expedition or photo walk",
        "category": "outdoor",
        "typical_duration": "3-8 hours",
        "base_items": [
            "camera body",
            "lenses",
            "extra batteries",
            "memory cards",
            "tripod",
            "camera bag",
            "lens cleaning kit",
            "comfortable shoes",
            "water bottle",
            "snacks",
            "phone/GPS"
        ],
        "cold_items": [
            "warm gloves (fingerless)",
            "warm jacket",
            "hand warmers"
        ],
        "rain_items": [
            "camera rain cover",
            "waterproof camera bag",
            "rain jacket"
        ]
    },
    
    "road_trip": {
        "description": "Multi-day driving adventure with various stops",
        "category": "travel",
        "typical_duration": "3-14 days",
        "base_items": [
            "driver's license",
            "vehicle registration/insurance",
            "road atlas/GPS",
            "phone car charger",
            "first aid kit",
            "emergency kit",
            "cooler",
            "snacks and drinks",
            "entertainment (music, audiobooks)",
            "comfortable clothes",
            "pillow and blanket",
            "toiletries"
        ],
        "cold_items": [
            "warm blankets",
            "emergency heat packs",
            "warm clothing"
        ],
        "rain_items": [
            "umbrella",
            "rain gear",
            "emergency tarp"
        ]
    }
}