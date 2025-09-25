"""
Endorsements service functions - Business logic for managing endorsements.
"""

from typing import Dict, Any, List
from models import Endorsement, EndorsementStats
from utils import (
    load_endorsements,
    add_endorsement_to_file,
    remove_endorsement_from_file,
    get_endorsement_statistics,
    format_endorsements_for_display
)


def add_endorsement_data(name: str, comment: str = "") -> Dict[str, Any]:
    """Add a new endorsement"""
    if not name or not name.strip():
        return {
            "success": False,
            "message": "Name is required to add an endorsement",
            "endorsement": None
        }
    
    success = add_endorsement_to_file(name.strip(), comment.strip())
    
    if success:
        # Get the newly added endorsement
        endorsements = load_endorsements()
        new_endorsement = next((e for e in endorsements if e.name.lower() == name.lower().strip()), None)
        
        return {
            "success": True,
            "message": f"Thank you {name} for endorsing our travel agent!",
            "endorsement": {
                "name": new_endorsement.name,
                "comment": new_endorsement.comment,
                "timestamp": new_endorsement.timestamp.isoformat()
            } if new_endorsement else None
        }
    else:
        return {
            "success": False,
            "message": f"{name} has already endorsed this travel agent",
            "endorsement": None
        }


def get_endorsements_data() -> Dict[str, Any]:
    """Get all endorsements"""
    endorsements = load_endorsements()
    
    return {
        "endorsements": [
            {
                "name": e.name,
                "comment": e.comment,
                "timestamp": e.timestamp.isoformat()
            } for e in endorsements
        ],
        "count": len(endorsements),
        "formatted_display": format_endorsements_for_display(endorsements)
    }


def get_endorsement_stats_data() -> Dict[str, Any]:
    """Get endorsement statistics"""
    stats = get_endorsement_statistics()
    return stats.to_dict()


def remove_endorsement_data(name: str) -> Dict[str, Any]:
    """Remove an endorsement by name"""
    if not name or not name.strip():
        return {
            "success": False,
            "message": "Name is required to remove an endorsement"
        }
    
    success = remove_endorsement_from_file(name.strip())
    
    if success:
        return {
            "success": True,
            "message": f"Removed endorsement from {name}"
        }
    else:
        return {
            "success": False,
            "message": f"No endorsement found for {name}"
        }


def get_endorsement_prompt() -> str:
    """Get a friendly prompt for users to add endorsements"""
    stats = get_endorsement_statistics()
    
    if stats.total_count == 0:
        return ("🌟 This travel agent has no endorsements yet! "
                "Be the first to share your positive experience by adding your endorsement.")
    else:
        return (f"🌟 This travel agent has {stats.total_count} endorsement(s) from satisfied travelers! "
                f"Add your own endorsement to help others discover this great service.")


def format_endorsement_summary() -> str:
    """Get a brief summary of endorsements for display"""
    stats = get_endorsement_statistics()
    
    if stats.total_count == 0:
        return "No endorsements yet - be the first!"
    
    summary = f"✨ {stats.total_count} endorsement(s)"
    
    if stats.recent_count > 0:
        summary += f" ({stats.recent_count} in the last 30 days)"
    
    if stats.latest_endorsement:
        summary += f"\n📝 Latest: {stats.latest_endorsement.name}"
        if stats.latest_endorsement.comment:
            summary += f' - "{stats.latest_endorsement.comment[:50]}{"..." if len(stats.latest_endorsement.comment) > 50 else ""}"'
    
    return summary