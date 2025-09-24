"""
Tourist attractions MCP configuration mocks data.
"""

# World Tourist Attractions API configuration
ATTRACTIONS_BASE_URL = "https://www.world-tourist-attractions-api.com"
API_VERSION = "v1"

# API Endpoints
ENDPOINTS = {
    "attraction_by_id": f"/api/{API_VERSION}/attraction",
    "random_famous": f"/api/{API_VERSION}/random/famous",
    "random_india": f"/api/{API_VERSION}/random/india", 
    "wonders": f"/api/{API_VERSION}/wonders",
    "search": f"/api/{API_VERSION}/search",
    "categories": f"/api/{API_VERSION}/categories"
}

# Attraction categories
ATTRACTION_CATEGORIES = {
    "historical": "Historical Sites",
    "natural": "Natural Wonders", 
    "cultural": "Cultural Sites",
    "religious": "Religious Sites",
    "modern": "Modern Attractions",
    "museums": "Museums",
    "parks": "Parks & Gardens",
    "beaches": "Beaches",
    "mountains": "Mountains",
    "architecture": "Architecture",
    "entertainment": "Entertainment",
    "adventure": "Adventure Sports"
}

# Popular countries/regions
POPULAR_REGIONS = [
    "India", "France", "Italy", "Spain", "Greece", "Egypt", 
    "Thailand", "Japan", "China", "USA", "UK", "Germany",
    "Turkey", "Morocco", "Brazil", "Peru", "Australia"
]

# Booking status codes
BOOKING_STATUS = {
    "pending": "Pending Confirmation",
    "confirmed": "Confirmed", 
    "cancelled": "Cancelled",
    "completed": "Completed"
}

# Default values
DEFAULT_SEARCH_LIMIT = 20
MAX_SEARCH_LIMIT = 100
DEFAULT_RATING_MIN = 3.0

# Mock attractions data for demonstration
MOCK_ATTRACTIONS = [
    {
        "id": 1,
        "name": "Eiffel Tower",
        "description": "Iconic iron lattice tower located on the Champ de Mars in Paris, France",
        "category": "architecture",
        "location": {"city": "Paris", "country": "France", "region": "Île-de-France"},
        "rating": 4.6,
        "image_url": "https://example.com/eiffel-tower.jpg",
        "website": "https://www.toureiffel.paris",
        "opening_hours": "9:30 AM - 11:45 PM",
        "entry_fee": "€29.40 - €73.30"
    },
    {
        "id": 2,
        "name": "Taj Mahal",
        "description": "Ivory-white marble mausoleum on the right bank of the river Yamuna in Agra",
        "category": "historical",
        "location": {"city": "Agra", "country": "India", "region": "Uttar Pradesh"},
        "rating": 4.8,
        "image_url": "https://example.com/taj-mahal.jpg",
        "website": "https://www.tajmahal.gov.in",
        "opening_hours": "6:00 AM - 7:00 PM",
        "entry_fee": "₹1100 (foreigners), ₹50 (Indians)"
    },
    {
        "id": 3,
        "name": "Colosseum",
        "description": "Ancient Roman amphitheater in the center of Rome, Italy",
        "category": "historical",
        "location": {"city": "Rome", "country": "Italy", "region": "Lazio"},
        "rating": 4.5,
        "image_url": "https://example.com/colosseum.jpg",
        "website": "https://www.coopculture.it",
        "opening_hours": "8:30 AM - 7:15 PM",
        "entry_fee": "€16 - €22"
    },
    {
        "id": 4,
        "name": "Machu Picchu",
        "description": "Ancient Incan city set high in the Andes Mountains of Peru",
        "category": "historical",
        "location": {"city": "Cusco", "country": "Peru", "region": "Cusco"},
        "rating": 4.9,
        "image_url": "https://example.com/machu-picchu.jpg",
        "website": "https://www.machupicchu.gob.pe",
        "opening_hours": "6:00 AM - 5:30 PM",
        "entry_fee": "$47 - $62"
    },
    {
        "id": 5,
        "name": "Louvre Museum",
        "description": "World's largest art museum and historic monument in Paris",
        "category": "museums",
        "location": {"city": "Paris", "country": "France", "region": "Île-de-France"},
        "rating": 4.4,
        "image_url": "https://example.com/louvre.jpg",
        "website": "https://www.louvre.fr",
        "opening_hours": "9:00 AM - 6:00 PM",
        "entry_fee": "€17"
    },
    {
        "id": 6,
        "name": "Great Wall of China",
        "description": "Ancient fortification built across northern China",
        "category": "historical",
        "location": {"city": "Beijing", "country": "China", "region": "Beijing"},
        "rating": 4.7,
        "image_url": "https://example.com/great-wall.jpg",
        "website": "https://www.mutianyu.com",
        "opening_hours": "7:30 AM - 5:30 PM",
        "entry_fee": "¥45 - ¥65"
    },
    {
        "id": 7,
        "name": "Santorini",
        "description": "Beautiful Greek island with white buildings and blue domes",
        "category": "natural",
        "location": {"city": "Santorini", "country": "Greece", "region": "Cyclades"},
        "rating": 4.6,
        "image_url": "https://example.com/santorini.jpg",
        "website": "https://www.santorini.com",
        "opening_hours": "24/7",
        "entry_fee": "Free"
    },
    {
        "id": 8,
        "name": "Angkor Wat",
        "description": "Largest religious monument in the world, originally a Hindu temple",
        "category": "religious",
        "location": {"city": "Siem Reap", "country": "Cambodia", "region": "Siem Reap"},
        "rating": 4.8,
        "image_url": "https://example.com/angkor-wat.jpg",
        "website": "https://www.angkorwat.com",
        "opening_hours": "5:00 AM - 6:00 PM",
        "entry_fee": "$37 (1 day), $62 (3 days)"
    },
    {
        "id": 9,
        "name": "Central Park",
        "description": "Large public park in Manhattan, New York City",
        "category": "parks",
        "location": {"city": "New York", "country": "USA", "region": "New York"},
        "rating": 4.3,
        "image_url": "https://example.com/central-park.jpg",
        "website": "https://www.centralparknyc.org",
        "opening_hours": "6:00 AM - 1:00 AM",
        "entry_fee": "Free"
    },
    {
        "id": 10,
        "name": "Petra",
        "description": "Archaeological city famous for rock-cut architecture and water conduit system",
        "category": "historical",
        "location": {"city": "Ma'an", "country": "Jordan", "region": "Ma'an"},
        "rating": 4.7,
        "image_url": "https://example.com/petra.jpg",
        "website": "https://www.visitpetra.jo",
        "opening_hours": "6:00 AM - 6:00 PM",
        "entry_fee": "70 JOD (1 day), 55 JOD (2 days)"
    },
    {
        "id": 11,
        "name": "Statue of Liberty",
        "description": "Neoclassical sculpture on Liberty Island in New York Harbor",
        "category": "modern",
        "location": {"city": "New York", "country": "USA", "region": "New York"},
        "rating": 4.4,
        "image_url": "https://example.com/statue-liberty.jpg",
        "website": "https://www.nps.gov/stli",
        "opening_hours": "8:30 AM - 4:00 PM",
        "entry_fee": "$23.80 - $24.30"
    },
    {
        "id": 12,
        "name": "Sagrada Familia",
        "description": "Unfinished Roman Catholic minor basilica in Barcelona, Spain",
        "category": "religious",
        "location": {"city": "Barcelona", "country": "Spain", "region": "Catalonia"},
        "rating": 4.6,
        "image_url": "https://example.com/sagrada-familia.jpg",
        "website": "https://sagradafamilia.org",
        "opening_hours": "9:00 AM - 8:00 PM",
        "entry_fee": "€26 - €40"
    },
    {
        "id": 13,
        "name": "Kinkaku-ji",
        "description": "Golden Pavilion, a Zen temple in Kyoto, Japan",
        "category": "religious",
        "location": {"city": "Kyoto", "country": "Japan", "region": "Kansai"},
        "rating": 4.5,
        "image_url": "https://example.com/kinkaku-ji.jpg",
        "website": "https://www.shokoku-ji.jp",
        "opening_hours": "9:00 AM - 5:00 PM",
        "entry_fee": "¥500"
    },
    {
        "id": 14,
        "name": "Sydney Opera House",
        "description": "Multi-venue performing arts center in Sydney, Australia",
        "category": "modern",
        "location": {"city": "Sydney", "country": "Australia", "region": "New South Wales"},
        "rating": 4.4,
        "image_url": "https://example.com/sydney-opera.jpg",
        "website": "https://www.sydneyoperahouse.com",
        "opening_hours": "9:00 AM - 8:30 PM",
        "entry_fee": "$43 - $175"
    },
    {
        "id": 15,
        "name": "Christ the Redeemer",
        "description": "Art Deco statue of Jesus Christ in Rio de Janeiro, Brazil",
        "category": "religious",
        "location": {"city": "Rio de Janeiro", "country": "Brazil", "region": "Rio de Janeiro"},
        "rating": 4.5,
        "image_url": "https://example.com/christ-redeemer.jpg",
        "website": "https://www.cristoredentor.com.br",
        "opening_hours": "8:00 AM - 7:00 PM",
        "entry_fee": "R$65 - R$98"
    }
]

# World wonders mock data
WORLD_WONDERS = [1, 2, 3, 4, 6, 8, 10, 15]  # IDs from MOCK_ATTRACTIONS that are world wonders