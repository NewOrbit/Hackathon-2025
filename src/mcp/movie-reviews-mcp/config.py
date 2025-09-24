"""
Tourist attractions MCP configuration mocks data.
"""

MOVIE_GENRES = {
    "action": "Action",
    "comedy": "Comedy",
    "drama": "Drama",
    "horror": "Horror",
    "romance": "Romance",
    "thriller": "Thriller",
    "sci-fi": "Science Fiction",
    "fantasy": "Fantasy",
    "documentary": "Documentary",
    "animation": "Animation"
}

# Default values
DEFAULT_SEARCH_LIMIT = 20
MAX_SEARCH_LIMIT = 100
DEFAULT_RATING_MIN = 3.0

# Mock movies data matching cinema-mcp for demonstration
MOCK_MOVIES = [
    {
        "id": 1,
        "title": "Galactic Adventures",
        "synopsis": "An epic space adventure following a crew of explorers as they journey through distant galaxies to save humanity from an alien threat.",
        "rating": 8.7,
        "durationMins": 142,
        "genre": "sci-fi"
    },
    {
        "id": 2,
        "title": "The Midnight Mystery",
        "synopsis": "A thrilling detective story about a small town sheriff investigating a series of mysterious disappearances that all happen at midnight.",
        "rating": 8.2,
        "durationMins": 118,
        "genre": "thriller"
    },
    {
        "id": 3,
        "title": "Laugh Out Loud",
        "synopsis": "A hilarious comedy about three friends who accidentally become viral internet sensations and must navigate their newfound fame.",
        "rating": 7.8,
        "durationMins": 95,
        "genre": "comedy"
    },
    {
        "id": 4,
        "title": "Dragon's Heart",
        "synopsis": "An animated fantasy adventure about a young girl who discovers she can communicate with dragons and must save her village from an ancient curse.",
        "rating": 8.5,
        "durationMins": 103,
        "genre": "animation"
    },
    {
        "id": 5,
        "title": "City of Shadows",
        "synopsis": "A noir drama set in 1940s New York following a detective uncovering corruption in the police department while solving a murder case.",
        "rating": 8.9,
        "durationMins": 134,
        "genre": "drama"
    },
    {
        "id": 6,
        "title": "Ocean's Edge",
        "synopsis": "A spectacular IMAX documentary exploring the deepest parts of our oceans and the incredible creatures that call them home.",
        "rating": 9.1,
        "durationMins": 87,
        "genre": "documentary"
    },
    {
        "id": 7,
        "title": "Love in Paris",
        "synopsis": "A romantic comedy about an American tourist who gets lost in Paris and finds love with a local café owner who helps her navigate the city.",
        "rating": 7.6,
        "durationMins": 108,
        "genre": "romance"
    },
    {
        "id": 8,
        "title": "Nightmare Manor",
        "synopsis": "A spine-chilling horror film about a family that inherits an old mansion, only to discover it's haunted by the spirits of its previous owners.",
        "rating": 7.4,
        "durationMins": 106,
        "genre": "horror"
    },
    {
        "id": 9,
        "title": "The Shawshank Redemption",
        "synopsis": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        "rating": 9.3,
        "durationMins": 142,
        "genre": "drama"
    },
    {
        "id": 10,
        "title": "Spirited Away",
        "synopsis": "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, where humans are changed into beasts.",
        "rating": 8.6,
        "durationMins": 125,
        "genre": "animation"
    },
    {
        "id": 11,
        "title": "Gladiator",
        "synopsis": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.",
        "rating": 8.5,
        "durationMins": 155,
        "genre": "action"
    },
    {
        "id": 12,
        "title": "The Matrix",
        "synopsis": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
        "rating": 8.7,
        "durationMins": 136,
        "genre": "sci-fi"
    },
    {
        "id": 13,
        "title": "Fight Club",
        "synopsis": "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into something much more.",
        "rating": 8.8,
        "durationMins": 139,
        "genre": "drama"
    },
    {
        "id": 14,
        "title": "The Lord of the Rings: The Return of the King",
        "synopsis": "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.",
        "rating": 8.9,
        "durationMins": 201,
        "genre": "fantasy"
    },
    {
        "id": 15,
        "title": "The Lion King",
        "synopsis": "Lion prince Simba and his father are targeted by his bitter uncle, who wants to ascend the throne himself.",
        "rating": 8.5,
        "durationMins": 88,
        "genre": "animation"
    },
    {
        "id": 16,
        "title": "Goodfellas",
        "synopsis": "The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners.",
        "rating": 8.7,
        "durationMins": 146,
        "genre": "crime"
    },
    {
        "id": 17,
        "title": "The Silence of the Lambs",
        "synopsis": "A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to catch another serial killer.",
        "rating": 8.6,
        "durationMins": 118,
        "genre": "thriller"
    },
    {
        "id": 18,
        "title": "Saving Private Ryan",
        "synopsis": "Following the Normandy Landings, a group of U.S. soldiers go behind enemy lines to retrieve a paratrooper whose brothers have been killed in action.",
        "rating": 8.6,
        "durationMins": 169,
        "genre": "war"
    },
    {
        "id": 19,
        "title": "The Prestige",
        "synopsis": "After a tragic accident, two stage magicians engage in a battle to create the ultimate illusion while sacrificing everything they have to outwit each other.",
        "rating": 8.5,
        "durationMins": 130,
        "genre": "mystery"
    },
    {
        "id": 20,
        "title": "Whiplash",
        "synopsis": "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing to realize a student's potential.",
        "rating": 8.5,
        "durationMins": 106,
        "genre": "drama"
    }
]

MOCK_REVIEWS = [
    {
        "movie_id": 1,
        "reviewer": "Alice",
        "rating": 5,
        "comment": "An epic space adventure with stunning visuals and compelling characters. The galaxy scenes are breathtaking!",
        "reviewDate": "2024-09-01"
    },
    {
        "movie_id": 1,
        "reviewer": "Bob",
        "rating": 4,
        "comment": "Great sci-fi adventure, though the plot gets a bit convoluted in the middle. Overall very entertaining.",
        "reviewDate": "2024-09-02"
    },
    {
        "movie_id": 2,
        "reviewer": "Charlie",
        "rating": 5,
        "comment": "A masterful thriller that keeps you guessing until the very end. Perfect midnight mystery vibes!",
        "reviewDate": "2024-09-03"
    },
    {
        "movie_id": 2,
        "reviewer": "Diana",
        "rating": 4,
        "comment": "Excellent detective work and atmospheric tension. The midnight setting adds to the suspense.",
        "reviewDate": "2024-09-04"
    },
    {
        "movie_id": 3,
        "reviewer": "Eve",
        "rating": 4,
        "comment": "Hilarious from start to finish! The social media angle is spot-on and very relatable.",
        "reviewDate": "2024-09-05"
    },
    {
        "movie_id": 3,
        "reviewer": "Frank",
        "rating": 5,
        "comment": "Best comedy I've seen this year. The friendship dynamics are heartwarming and funny.",
        "reviewDate": "2024-09-06"
    },
    {
        "movie_id": 4,
        "reviewer": "Grace",
        "rating": 5,
        "comment": "Beautiful animation and a heartwarming story about dragons and friendship. Perfect for families!",
        "reviewDate": "2024-09-07"
    },
    {
        "movie_id": 4,
        "reviewer": "Henry",
        "rating": 4,
        "comment": "Lovely animated adventure with great voice acting and stunning visuals.",
        "reviewDate": "2024-09-08"
    },
    {
        "movie_id": 5,
        "reviewer": "Ivy",
        "rating": 5,
        "comment": "A masterful noir drama with incredible atmosphere. The 1940s setting is perfectly captured.",
        "reviewDate": "2024-09-09"
    },
    {
        "movie_id": 5,
        "reviewer": "Jack",
        "rating": 4,
        "comment": "Gripping detective story with excellent cinematography and strong performances.",
        "reviewDate": "2024-09-10"
    },
    {
        "movie_id": 6,
        "reviewer": "Karen",
        "rating": 5,
        "comment": "Absolutely breathtaking documentary! The ocean footage is stunning and educational.",
        "reviewDate": "2024-09-11"
    },
    {
        "movie_id": 6,
        "reviewer": "Leo",
        "rating": 5,
        "comment": "David Attenborough's narration combined with incredible underwater cinematography. A must-see!",
        "reviewDate": "2024-09-12"
    },
    {
        "movie_id": 7,
        "reviewer": "Mona",
        "rating": 4,
        "comment": "Charming romantic comedy with beautiful Parisian scenery. Predictable but delightful!",
        "reviewDate": "2024-09-13"
    },
    {
        "movie_id": 7,
        "reviewer": "Nate",
        "rating": 3,
        "comment": "Sweet story but a bit clichéd. The Paris setting makes up for the predictable plot.",
        "reviewDate": "2024-09-14"
    },
    {
        "movie_id": 8,
        "reviewer": "Olivia",
        "rating": 4,
        "comment": "Genuinely scary horror film with great atmosphere. The old mansion setting is perfect!",
        "reviewDate": "2024-09-15"
    },
    {
        "movie_id": 8,
        "reviewer": "Paul",
        "rating": 3,
        "comment": "Classic haunted house horror but some jump scares felt forced. Good for horror fans.",
        "reviewDate": "2024-09-16"
    },
    {
        "movie_id": 9,
        "reviewer": "Quinn",
        "rating": 5,
        "comment": "A moving story of hope and friendship.",
        "reviewDate": "2024-03-17"
    },
    {
        "movie_id": 9,
        "reviewer": "Rita",
        "rating": 5,
        "comment": "Timeless and uplifting. A true classic.",
        "reviewDate": "2024-03-18"
    },
    {
        "movie_id": 10,
        "reviewer": "Sam",
        "rating": 5,
        "comment": "Magical animation with a rich, imaginative world.",
        "reviewDate": "2024-03-19"
    },
    {
        "movie_id": 10,
        "reviewer": "Tina",
        "rating": 4,
        "comment": "Beautiful visuals and a touching story.",
        "reviewDate": "2024-03-20"
    },
    {
        "movie_id": 11,
        "reviewer": "Uma",
        "rating": 5,
        "comment": "Epic battles and a compelling hero.",
        "reviewDate": "2024-03-21"
    },
    {
        "movie_id": 11,
        "reviewer": "Victor",
        "rating": 4,
        "comment": "Intense action and strong performances.",
        "reviewDate": "2024-03-22"
    },
    {
        "movie_id": 12,
        "reviewer": "Wendy",
        "rating": 5,
        "comment": "Mind-blowing concept and great action.",
        "reviewDate": "2024-03-23"
    },
    {
        "movie_id": 12,
        "reviewer": "Xander",
        "rating": 4,
        "comment": "Innovative and entertaining sci-fi.",
        "reviewDate": "2024-03-24"
    },
    {
        "movie_id": 13,
        "reviewer": "Yara",
        "rating": 5,
        "comment": "Dark, clever, and unforgettable.",
        "reviewDate": "2024-03-25"
    },
    {
        "movie_id": 13,
        "reviewer": "Zane",
        "rating": 4,
        "comment": "Unique story with strong performances.",
        "reviewDate": "2024-03-26"
    },
    {
        "movie_id": 14,
        "reviewer": "Abby",
        "rating": 5,
        "comment": "Epic fantasy with breathtaking visuals.",
        "reviewDate": "2024-03-27"
    },
    {
        "movie_id": 14,
        "reviewer": "Ben",
        "rating": 5,
        "comment": "A fitting end to a legendary trilogy.",
        "reviewDate": "2024-03-28"
    },
    {
        "movie_id": 15,
        "reviewer": "Cara",
        "rating": 5,
        "comment": "A childhood favorite with memorable songs.",
        "reviewDate": "2024-03-29"
    },
    {
        "movie_id": 15,
        "reviewer": "Dan",
        "rating": 4,
        "comment": "Beautiful animation and a touching story.",
        "reviewDate": "2024-03-30"
    },
    {
        "movie_id": 16,
        "reviewer": "Ella",
        "rating": 5,
        "comment": "Gripping crime drama with stellar acting.",
        "reviewDate": "2024-03-31"
    },
    {
        "movie_id": 16,
        "reviewer": "Finn",
        "rating": 4,
        "comment": "Intense and well-crafted mob story.",
        "reviewDate": "2024-04-01"
    },
    {
        "movie_id": 17,
        "reviewer": "Gina",
        "rating": 5,
        "comment": "Chilling and suspenseful thriller.",
        "reviewDate": "2024-04-02"
    },
    {
        "movie_id": 17,
        "reviewer": "Hank",
        "rating": 4,
        "comment": "Great performances and a gripping plot.",
        "reviewDate": "2024-04-03"
    },
    {
        "movie_id": 18,
        "reviewer": "Iris",
        "rating": 5,
        "comment": "A powerful and realistic war film.",
        "reviewDate": "2024-04-04"
    },
    {
        "movie_id": 18,
        "reviewer": "Jake",
        "rating": 4,
        "comment": "Intense and emotional storytelling.",
        "reviewDate": "2024-04-05"
    },
    {
        "movie_id": 19,
        "reviewer": "Kara",
        "rating": 5,
        "comment": "A fascinating tale of rivalry and obsession.",
        "reviewDate": "2024-04-06"
    },
    {
        "movie_id": 19,
        "reviewer": "Liam",
        "rating": 4,
        "comment": "Intriguing plot with excellent twists.",
        "reviewDate": "2024-04-07"
    },
    {
        "movie_id": 20,
        "reviewer": "Mia",
        "rating": 5,
        "comment": "Electrifying performances and a compelling story.",
        "reviewDate": "2024-04-08"
    },
    {
        "movie_id": 20,
        "reviewer": "Noah",
        "rating": 4,
        "comment": "Intense and inspiring musical drama.",
        "reviewDate": "2024-04-09"
    },
    {
        "movie_id": 1,
        "reviewer": "Oscar",
        "rating": 2,
        "comment": "Too confusing and dragged on for too long.",
        "reviewDate": "2024-04-10"
    },
    {
        "movie_id": 5,
        "reviewer": "Pam",
        "rating": 2,
        "comment": "Overrated and slow, didn't connect with the story.",
        "reviewDate": "2024-04-11"
    },
    {
        "movie_id": 7,
        "reviewer": "Quentin",
        "rating": 1,
        "comment": "Found it boring and hard to follow.",
        "reviewDate": "2024-04-12"
    },
    {
        "movie_id": 12,
        "reviewer": "Ralph",
        "rating": 2,
        "comment": "Not as groundbreaking as people say, felt dated.",
        "reviewDate": "2024-04-13"
    },
    {
        "movie_id": 15,
        "reviewer": "Sophie",
        "rating": 1,
        "comment": "Didn't enjoy the animation style or the music.",
        "reviewDate": "2024-04-14"
    }
]