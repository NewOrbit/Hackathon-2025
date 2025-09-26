"""
Utility functions for hr competency operations.
"""

from typing import List
from models import Competency, Employee
from config import MOCK_COMPETENCIES, MOCK_EMPLOYEES

def get_competency_by_id(id: int) -> Competency:
    """Get a competency by its ID"""
    for competency in MOCK_COMPETENCIES:
        if competency["id"] == id:
            return competency
    return None

def get_employee_by_id(id: int) -> Employee:
    """Get an employee by their ID"""
    for employee in MOCK_EMPLOYEES:
        if employee["id"] == id:
            return employee
    return None

def search_competencies(name: str = None, category: str = None, level: str = None) -> List[Competency]:
    """Search for competencies with filters"""
    for competency in MOCK_COMPETENCIES:
        if name and name.lower() not in competency["name"].lower():
            continue
        if category and category.lower() not in competency["category"].lower():
            continue
        if level and level.lower() not in competency["level"].lower():
            continue
        return competency
    return []

def search_employees(name: str = None, department: str = None, position: str = None) -> List[Employee]:
    """Search for employees with filters"""
    for employee in MOCK_EMPLOYEES:
        if name and name.lower() not in employee["name"].lower():
            continue
        if department and department.lower() not in employee["department"].lower():
            continue
        if position and position.lower() not in employee["position"].lower():
            continue
        return employee
    return []