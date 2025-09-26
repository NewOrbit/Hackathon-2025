"""
HR competency data models - Data classes for hr competency objects.
"""

from dataclasses import dataclass
from typing import List

@dataclass
class Employee:
    id: int
    name: str
    email: str
    phone: str
    department: str
    position: str
    completed_courses: List[str] # ids of the courses completed
