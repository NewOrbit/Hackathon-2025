from dataclasses import dataclass
from typing import Any, Optional, List


@dataclass
class RestaurantsList:
    category: str
    location: Optional[str] = None
    total_count: int = 0
    restaurants: List[Any] = None