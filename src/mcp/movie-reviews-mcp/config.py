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

# Mock attractions data for demonstration
MOCK_MOVIES = [
    {
        "id": 1,
        "title": "Inception",
        "synopsis": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        "rating": 8.8,
        "durationMins": 148,
        "genre": "sci-fi"
    },
    {
        "id": 2,
        "title": "The Godfather",
        "synopsis": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
        "rating": 9.2,
        "durationMins": 175,
        "genre": "drama"
    },
    {
        "id": 3,
        "title": "The Dark Knight",
        "synopsis": "When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham. The Dark Knight must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
        "rating": 9.0,
        "durationMins": 152,
        "genre": "action"
    },
    {
        "id": 4,
        "title": "Pulp Fiction",
        "synopsis": "The lives of two mob hitmen, a boxer, a gangster's wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
        "rating": 8.9,
        "durationMins": 154,
        "genre": "crime"
    },
    {
        "id": 5,
        "title": "Forrest Gump",
        "synopsis": "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with a low IQ.",
        "rating": 8.8,
        "durationMins": 142,
        "genre": "drama"
    },
    {
        "id": 6,
        "title": "Interstellar",
        "synopsis": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
        "rating": 8.6,
        "durationMins": 169,
        "genre": "sci-fi"
    },
    {
        "id": 7,
        "title": "Parasite",
        "synopsis": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
        "rating": 8.6,
        "durationMins": 132,
        "genre": "thriller"
    },
    {
        "id": 8,
        "title": "Schindler's List",
        "synopsis": "In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis.",
        "rating": 8.9,
        "durationMins": 195,
        "genre": "history"
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
        "comment": "A mind-bending masterpiece with stunning visuals and a gripping plot."
    },
    {
        "movie_id": 1,
        "reviewer": "Bob",
        "rating": 4,
        "comment": "Complex and thought-provoking, but a bit hard to follow at times."
    },
    {
        "movie_id": 2,
        "reviewer": "Charlie",
        "rating": 5,
        "comment": "An epic tale of family and power. A must-watch classic."
    },
    {
        "movie_id": 2,
        "reviewer": "Diana",
        "rating": 5,
        "comment": "Brilliant performances and an unforgettable story."
    },
    {
        "movie_id": 3,
        "reviewer": "Eve",
        "rating": 5,
        "comment": "Heath Ledger's Joker is iconic. A thrilling ride from start to finish."
    },
    {
        "movie_id": 3,
        "reviewer": "Frank",
        "rating": 4,
        "comment": "Great action and depth, though a bit dark for my taste."
    },
    {
        "movie_id": 4,
        "reviewer": "Grace",
        "rating": 5,
        "comment": "A wild, stylish film with unforgettable dialogue."
    },
    {
        "movie_id": 4,
        "reviewer": "Henry",
        "rating": 4,
        "comment": "Unique storytelling and great cast."
    },
    {
        "movie_id": 5,
        "reviewer": "Ivy",
        "rating": 5,
        "comment": "Heartwarming and inspirational. Tom Hanks is fantastic."
    },
    {
        "movie_id": 5,
        "reviewer": "Jack",
        "rating": 4,
        "comment": "A touching story with memorable moments."
    },
    {
        "movie_id": 6,
        "reviewer": "Karen",
        "rating": 5,
        "comment": "Visually stunning and emotionally powerful."
    },
    {
        "movie_id": 6,
        "reviewer": "Leo",
        "rating": 4,
        "comment": "Ambitious sci-fi with a moving story."
    },
    {
        "movie_id": 7,
        "reviewer": "Mona",
        "rating": 5,
        "comment": "A brilliant social satire with suspenseful twists."
    },
    {
        "movie_id": 7,
        "reviewer": "Nate",
        "rating": 4,
        "comment": "Darkly funny and deeply unsettling."
    },
    {
        "movie_id": 8,
        "reviewer": "Olivia",
        "rating": 5,
        "comment": "A powerful and emotional historical drama."
    },
    {
        "movie_id": 8,
        "reviewer": "Paul",
        "rating": 5,
        "comment": "Heart-wrenching and beautifully acted."
    },
    {
        "movie_id": 9,
        "reviewer": "Quinn",
        "rating": 5,
        "comment": "A moving story of hope and friendship."
    },
    {
        "movie_id": 9,
        "reviewer": "Rita",
        "rating": 5,
        "comment": "Timeless and uplifting. A true classic."
    },
    {
        "movie_id": 10,
        "reviewer": "Sam",
        "rating": 5,
        "comment": "Magical animation with a rich, imaginative world."
    },
    {
        "movie_id": 10,
        "reviewer": "Tina",
        "rating": 4,
        "comment": "Beautiful visuals and a touching story."
    },
    {
        "movie_id": 11,
        "reviewer": "Uma",
        "rating": 5,
        "comment": "Epic battles and a compelling hero."
    },
    {
        "movie_id": 11,
        "reviewer": "Victor",
        "rating": 4,
        "comment": "Intense action and strong performances."
    },
    {
        "movie_id": 12,
        "reviewer": "Wendy",
        "rating": 5,
        "comment": "Mind-blowing concept and great action."
    },
    {
        "movie_id": 12,
        "reviewer": "Xander",
        "rating": 4,
        "comment": "Innovative and entertaining sci-fi."
    },
    {
        "movie_id": 13,
        "reviewer": "Yara",
        "rating": 5,
        "comment": "Dark, clever, and unforgettable."
    },
    {
        "movie_id": 13,
        "reviewer": "Zane",
        "rating": 4,
        "comment": "Unique story with strong performances."
    },
    {
        "movie_id": 14,
        "reviewer": "Abby",
        "rating": 5,
        "comment": "Epic fantasy with breathtaking visuals."
    },
    {
        "movie_id": 14,
        "reviewer": "Ben",
        "rating": 5,
        "comment": "A fitting end to a legendary trilogy."
    },
    {
        "movie_id": 15,
        "reviewer": "Cara",
        "rating": 5,
        "comment": "A childhood favorite with memorable songs."
    },
    {
        "movie_id": 15,
        "reviewer": "Dan",
        "rating": 4,
        "comment": "Beautiful animation and a touching story."
    },
    {
        "movie_id": 16,
        "reviewer": "Ella",
        "rating": 5,
        "comment": "Gripping crime drama with stellar acting."
    },
    {
        "movie_id": 16,
        "reviewer": "Finn",
        "rating": 4,
        "comment": "Intense and well-crafted mob story."
    },
    {
        "movie_id": 17,
        "reviewer": "Gina",
        "rating": 5,
        "comment": "Chilling and suspenseful thriller."
    },
    {
        "movie_id": 17,
        "reviewer": "Hank",
        "rating": 4,
        "comment": "Great performances and a gripping plot."
    },
    {
        "movie_id": 18,
        "reviewer": "Iris",
        "rating": 5,
        "comment": "A powerful and realistic war film."
    },
    {
        "movie_id": 18,
        "reviewer": "Jake",
        "rating": 4,
        "comment": "Intense and emotional storytelling."
    },
    {
        "movie_id": 19,
        "reviewer": "Kara",
        "rating": 5,
        "comment": "A fascinating tale of rivalry and obsession."
    },
    {
        "movie_id": 19,
        "reviewer": "Liam",
        "rating": 4,
        "comment": "Intriguing plot with excellent twists."
    },
    {
        "movie_id": 20,
        "reviewer": "Mia",
        "rating": 5,
        "comment": "Electrifying performances and a compelling story."
    },
    {
        "movie_id": 20,
        "reviewer": "Noah",
        "rating": 4,
        "comment": "Intense and inspiring musical drama."
    },
    {
        "movie_id": 1,
        "reviewer": "Oscar",
        "rating": 2,
        "comment": "Too confusing and dragged on for too long."
    },
    {
        "movie_id": 5,
        "reviewer": "Pam",
        "rating": 2,
        "comment": "Overrated and slow, didn't connect with the story."
    },
    {
        "movie_id": 7,
        "reviewer": "Quentin",
        "rating": 1,
        "comment": "Found it boring and hard to follow."
    },
    {
        "movie_id": 12,
        "reviewer": "Ralph",
        "rating": 2,
        "comment": "Not as groundbreaking as people say, felt dated."
    },
    {
        "movie_id": 15,
        "reviewer": "Sophie",
        "rating": 1,
        "comment": "Didn't enjoy the animation style or the music."
    }
]