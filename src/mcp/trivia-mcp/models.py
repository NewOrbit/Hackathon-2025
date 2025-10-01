"""
Nutrition Trivia data models - Data classes for nutrition trivia and secrets objects.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class NutritionSecret:
    nutrition_topic: str
    nutrition_secrets: List[str]
    celebrity_nutrition: List[str]
    nutrition_tips: List[str]


@dataclass
class NutritionResponse:
    nutrition_topic: str
    secret_type: str  # "nutrition_secret", "celebrity_nutrition", "nutrition_tip"
    content: str
    category: Optional[str] = None


@dataclass
class NutritionTriviaDatabase:
    """In-memory database structure for nutrition trivia data"""

    nutrition_topics: dict  # nutrition_topic -> NutritionSecret
