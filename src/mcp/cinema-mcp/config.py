"""
Cinema MCP configuration and mock data.
"""

from datetime import date, time

# Cinema configuration
CINEMA_NAME = "MovieMagic Cinema"
CINEMA_LOCATION = "Downtown Plaza"

# Room/Theater configurations
CINEMA_ROOMS = {
    "theater_a": {"name": "Theater A", "capacity": 150, "type": "standard"},
    "theater_b": {"name": "Theater B", "capacity": 200, "type": "premium"},
    "theater_c": {"name": "Theater C", "capacity": 100, "type": "vip"},
    "imax": {"name": "IMAX Theater", "capacity": 300, "type": "imax"}
}

# Movie genres
MOVIE_GENRES = {
    "action": "Action",
    "comedy": "Comedy", 
    "drama": "Drama",
    "horror": "Horror",
    "sci-fi": "Science Fiction",
    "romance": "Romance",
    "thriller": "Thriller",
    "animation": "Animation",
    "documentary": "Documentary",
    "family": "Family"
}

# Movie ratings
MOVIE_RATINGS = ["G", "PG", "PG-13", "R", "NC-17"]

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

# Mock movie presentations data for demonstration
MOCK_MOVIE_PRESENTATIONS = [
    {
        "id": "movie_001",
        "title": "Galactic Adventures",
        "description": "An epic space adventure following a crew of explorers as they journey through distant galaxies to save humanity from an alien threat.",
        "date": date(2025, 9, 25),
        "time": time(14, 30),  # 2:30 PM
        "room": "theater_a",
        "seats_available": 150,
        "seats_booked": 45,
        "duration_minutes": 142,
        "genre": "sci-fi",
        "rating": "PG-13",
        "price_per_seat": 12.50,
        "director": "Sarah Johnson",
        "cast": ["Alex Thompson", "Maria Rodriguez", "James Chen"],
        "poster_url": "https://example.com/galactic-adventures.jpg"
    },
    {
        "id": "movie_002", 
        "title": "The Midnight Mystery",
        "description": "A thrilling detective story about a small town sheriff investigating a series of mysterious disappearances that all happen at midnight.",
        "date": date(2025, 9, 25),
        "time": time(19, 15),  # 7:15 PM
        "room": "theater_b",
        "seats_available": 200,
        "seats_booked": 125,
        "duration_minutes": 118,
        "genre": "thriller",
        "rating": "R",
        "price_per_seat": 14.00,
        "director": "Michael Davis",
        "cast": ["Emma Wilson", "Robert Garcia", "Lisa Park"],
        "poster_url": "https://example.com/midnight-mystery.jpg"
    },
    {
        "id": "movie_003",
        "title": "Laugh Out Loud",
        "description": "A hilarious comedy about three friends who accidentally become viral internet sensations and must navigate their newfound fame.",
        "date": date(2025, 9, 25),
        "time": time(21, 45),  # 9:45 PM
        "room": "theater_a",
        "seats_available": 150,
        "seats_booked": 89,
        "duration_minutes": 95,
        "genre": "comedy",
        "rating": "PG-13",
        "price_per_seat": 12.50,
        "director": "Jennifer Lee",
        "cast": ["Tom Martinez", "Sarah Kim", "David Brown"],
        "poster_url": "https://example.com/laugh-out-loud.jpg"
    },
    {
        "id": "movie_004",
        "title": "Dragon's Heart",
        "description": "An animated fantasy adventure about a young girl who discovers she can communicate with dragons and must save her village from an ancient curse.",
        "date": date(2025, 9, 26),
        "time": time(10, 00),  # 10:00 AM
        "room": "theater_c",
        "seats_available": 100,
        "seats_booked": 23,
        "duration_minutes": 103,
        "genre": "animation",
        "rating": "G",
        "price_per_seat": 10.00,
        "director": "Animation Studios Inc.",
        "cast": ["Voice Cast: Amy Johnson", "Mark Stevens", "Luna Rodriguez"],
        "poster_url": "https://example.com/dragons-heart.jpg"
    },
    {
        "id": "movie_005",
        "title": "City of Shadows",
        "description": "A noir drama set in 1940s New York following a detective uncovering corruption in the police department while solving a murder case.",
        "date": date(2025, 9, 26),
        "time": time(16, 20),  # 4:20 PM
        "room": "theater_b",
        "seats_available": 200,
        "seats_booked": 156,
        "duration_minutes": 134,
        "genre": "drama",
        "rating": "R",
        "price_per_seat": 14.00,
        "director": "Vincent Romano",
        "cast": ["Antonio Silva", "Catherine Moore", "Frank Williams"],
        "poster_url": "https://example.com/city-of-shadows.jpg"
    },
    {
        "id": "movie_006",
        "title": "Ocean's Edge",
        "description": "A spectacular IMAX documentary exploring the deepest parts of our oceans and the incredible creatures that call them home.",
        "date": date(2025, 9, 26),
        "time": time(20, 00),  # 8:00 PM
        "room": "imax",
        "seats_available": 300,
        "seats_booked": 78,
        "duration_minutes": 87,
        "genre": "documentary",
        "rating": "G",
        "price_per_seat": 18.00,
        "director": "Ocean Explorer Films",
        "cast": ["Narrator: David Attenborough"],
        "poster_url": "https://example.com/oceans-edge.jpg"
    },
    {
        "id": "movie_007",
        "title": "Love in Paris",
        "description": "A romantic comedy about an American tourist who gets lost in Paris and finds love with a local café owner who helps her navigate the city.",
        "date": date(2025, 9, 27),
        "time": time(15, 45),  # 3:45 PM
        "room": "theater_c",
        "seats_available": 100,
        "seats_booked": 67,
        "duration_minutes": 108,
        "genre": "romance",
        "rating": "PG",
        "price_per_seat": 11.50,
        "director": "Claire Dubois",
        "cast": ["Sophie Martin", "Jean-Luc Moreau", "Isabella Jones"],
        "poster_url": "https://example.com/love-in-paris.jpg"
    },
    {
        "id": "movie_008",
        "title": "Nightmare Manor",
        "description": "A spine-chilling horror film about a family that inherits an old mansion, only to discover it's haunted by the spirits of its previous owners.",
        "date": date(2025, 9, 27),
        "time": time(22, 30),  # 10:30 PM
        "room": "theater_a",
        "seats_available": 150,
        "seats_booked": 92,
        "duration_minutes": 106,
        "genre": "horror",
        "rating": "R",
        "price_per_seat": 13.00,
        "director": "Horror Productions",
        "cast": ["Scary Actor 1", "Scary Actor 2", "Scary Actor 3"],
        "poster_url": "https://example.com/nightmare-manor.jpg"
    }
]

# World famous movies for random selection
POPULAR_MOVIES = [
    "movie_001", "movie_002", "movie_003", "movie_006"
]