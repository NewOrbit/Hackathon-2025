"""
Movie reviews and information models
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

# movie reviews
@dataclass
class MovieReview:
    movie_id: int
    rating: int
    comment: str
    reviewer: str
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

@dataclass
class MoviesList:
    genre: str
    total_count: int = 0
    movies: List[Movie] = None

@dataclass
class MovieReviewList:
    movie: Movie
    reviews: List[MovieReview]
    total_count: int = 0
    avg_rating: Optional[float] = None