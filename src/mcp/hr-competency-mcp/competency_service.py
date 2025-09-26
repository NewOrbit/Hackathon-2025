"""
hr competency service - employee lookup utilities.
"""

from typing import Dict, Any, Optional, List
from config import MOCK_EMPLOYEES


def search_employees_data(
    id: Optional[int] = None,
    name: Optional[str] = None,
    department: Optional[str] = None,
    position: Optional[str] = None,
    completed_course_id: Optional[str] = None,
) -> Dict[str, Any]:
    """search employees by department, position, and/or completed courses."""
    filtered: List[Dict[str, Any]] = list(MOCK_EMPLOYEES)

    if id:
        filtered = [e for e in filtered if e.get("id") == id]

    if name:
        name_l = name.lower()
        filtered = [
            e for e in filtered if (e.get("name") or "").lower() == name_l
        ]

    if department:
        dept_l = department.lower()
        filtered = [
            e for e in filtered if (e.get("department") or "").lower() == dept_l
        ]

    if position:
        pos_l = position.lower()
        filtered = [
            e for e in filtered if (e.get("position") or "").lower() == pos_l
        ]

    if completed_course_id:
        cid = str(completed_course_id)
        filtered = [e for e in filtered if cid in (e.get("completed_courses") or [])]

    return {
        "total_count": len(filtered),
        "employees": [
            {
                "id": e["id"],
                "name": e["name"],
                "email": e["email"],
                "phone": e["phone"],
                "department": e["department"],
                "position": e["position"],
                "completed_courses": e.get("completed_courses", []),
            }
            for e in filtered
        ],
    }
