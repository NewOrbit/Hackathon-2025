"""
Trivia data models - Data classes for trivia and secrets objects.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class AttractionSecret:
    attraction_id: str
    secrets: List[str]
    celebrity_sightings: List[str]
    insider_tips: List[str]


@dataclass
class SecretResponse:
    attraction_id: str
    secret_type: str  # "secret", "sighting", "tip"
    content: str
    category: Optional[str] = None


@dataclass
class TriviaDatabase:
    """In-memory database structure for trivia data"""

    attractions: dict  # attraction_id -> AttractionSecret
