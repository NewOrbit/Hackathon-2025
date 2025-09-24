"""
Restaurant menu data models - Data classes for restaurant menu objects.
"""

from dataclasses import dataclass
from typing import Optional, List

@dataclass
class MenuItem:
    name: str
    price: float
    size: Optional[str] = None
    description: Optional[str] = None
    is_popular: Optional[bool] = False
    dietary_info: Optional[List[str]] = None  # e.g., ["vegan", "gluten-free"]

@dataclass
class Menu:
    id: int
    name: str
    items: List[MenuItem]