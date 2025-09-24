"""
Movie reviews and information models
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

# movie reviews
@dataclass
class MovieReview:
    movieId: int
    rating: int
    review: str
    reviewDate: datetime

# movie
@dataclass
class Movie:
    id: int
    title: str
    synopsis: str
    rating: float
    durationMins: int
    year: int
    genres: List[str]
    reviews: List[MovieReview]

@dataclass
class MoviesList:
    genre: str
    total_count: int = 0
    movies: List[Movie] = None
