"""
Trivia service with MCP tools for local secrets and insider information.
"""

import random
from typing import Dict, Any, List, Optional
from dataclasses import asdict

from config import SECRET_DATABASE, TIP_CATEGORIES, SECRET_TYPES
from models import AttractionSecret, SecretResponse


def get_attraction_secret(attraction_id: str) -> Dict[str, Any]:
    """Get a random secret, celebrity sighting, or insider tip for an attraction

    Args:
        attraction_id: ID of the attraction (e.g., "space_needle", "pike_place")

    Returns:
        SecretResponse object as dictionary or error dict
    """
    try:
        attraction_id = attraction_id.lower().replace(" ", "_")

        if attraction_id not in SECRET_DATABASE:
            return {
                "error": f"Attraction '{attraction_id}' not found in our secrets database"
            }

        attraction_data = SECRET_DATABASE[attraction_id]

        # Collect all available content
        all_content = []
        for secret_type in SECRET_TYPES:
            if secret_type in attraction_data:
                for content in attraction_data[secret_type]:
                    all_content.append({"type": secret_type, "content": content})

        if not all_content:
            return {"error": f"No secrets found for attraction '{attraction_id}'"}

        # Pick a random item
        random_item = random.choice(all_content)

        secret_response = SecretResponse(
            attraction_id=attraction_id,
            secret_type=random_item["type"],
            content=random_item["content"],
            category=random_item["type"],
        )

        return asdict(secret_response)

    except Exception as e:
        return {"error": f"Failed to get attraction secret: {str(e)}"}


def get_insider_tip(
    attraction_id: str, tip_type: Optional[str] = None
) -> Dict[str, Any]:
    """Get insider tips for a specific attraction, optionally filtered by type

    Args:
        attraction_id: ID of the attraction
        tip_type: Optional tip category filter ("photo", "food", "timing", "access", "local")

    Returns:
        List of insider tips as dictionary or error dict
    """
    try:
        attraction_id = attraction_id.lower().replace(" ", "_")

        if attraction_id not in SECRET_DATABASE:
            return {
                "error": f"Attraction '{attraction_id}' not found in our secrets database"
            }

        attraction_data = SECRET_DATABASE[attraction_id]

        if "insider_tips" not in attraction_data:
            return {"error": f"No insider tips found for attraction '{attraction_id}'"}

        tips = attraction_data["insider_tips"]

        # If tip_type is specified, try to filter (this is a simple keyword match)
        if tip_type:
            tip_type = tip_type.lower()
            filtered_tips = []
            for tip in tips:
                if tip_type in tip.lower():
                    filtered_tips.append(tip)

            if filtered_tips:
                tips = filtered_tips
            else:
                return {
                    "attraction_id": attraction_id,
                    "tip_type": tip_type,
                    "tips": [],
                    "message": f"No tips found matching category '{tip_type}'",
                }

        return {
            "attraction_id": attraction_id,
            "tip_type": tip_type or "all",
            "tips": tips,
            "total_count": len(tips),
        }

    except Exception as e:
        return {"error": f"Failed to get insider tips: {str(e)}"}


def get_celebrity_drama(location: str) -> Dict[str, Any]:
    """Get celebrity sightings and drama for a location

    Args:
        location: Location name (e.g., "space_needle", "pike_place", "times_square")

    Returns:
        Celebrity sightings and drama as dictionary or error dict
    """
    try:
        location = location.lower().replace(" ", "_")

        if location not in SECRET_DATABASE:
            return {"error": f"Location '{location}' not found in our secrets database"}

        attraction_data = SECRET_DATABASE[location]

        if "celebrity_sightings" not in attraction_data:
            return {"error": f"No celebrity sightings found for location '{location}'"}

        sightings = attraction_data["celebrity_sightings"]

        # Get a random celebrity sighting
        random_sighting = random.choice(sightings) if sightings else None

        return {
            "location": location,
            "celebrity_sighting": random_sighting,
            "all_sightings": sightings,
            "total_count": len(sightings),
        }

    except Exception as e:
        return {"error": f"Failed to get celebrity drama: {str(e)}"}


def get_all_attraction_secrets(attraction_id: str) -> Dict[str, Any]:
    """Get all secrets, celebrity sightings, and insider tips for an attraction

    Args:
        attraction_id: ID of the attraction

    Returns:
        Complete AttractionSecret object as dictionary or error dict
    """
    try:
        attraction_id = attraction_id.lower().replace(" ", "_")

        if attraction_id not in SECRET_DATABASE:
            return {
                "error": f"Attraction '{attraction_id}' not found in our secrets database"
            }

        attraction_data = SECRET_DATABASE[attraction_id]

        attraction_secret = AttractionSecret(
            attraction_id=attraction_id,
            secrets=attraction_data.get("secrets", []),
            celebrity_sightings=attraction_data.get("celebrity_sightings", []),
            insider_tips=attraction_data.get("insider_tips", []),
        )

        return asdict(attraction_secret)

    except Exception as e:
        return {"error": f"Failed to get attraction secrets: {str(e)}"}


def get_available_attractions() -> Dict[str, Any]:
    """Get list of all attractions with secrets available

    Returns:
        List of available attractions as dictionary
    """
    try:
        attractions = list(SECRET_DATABASE.keys())

        return {
            "total_attractions": len(attractions),
            "attractions": attractions,
            "tip_categories": list(TIP_CATEGORIES.keys()),
            "secret_types": SECRET_TYPES,
        }

    except Exception as e:
        return {"error": f"Failed to get available attractions: {str(e)}"}


def format_attraction_secrets(attraction_id: str) -> str:
    """Format all secrets for an attraction as a readable string

    Args:
        attraction_id: ID of the attraction

    Returns:
        Formatted string with all attraction secrets
    """
    try:
        data = get_all_attraction_secrets(attraction_id)
        if "error" in data:
            return f"Error: {data['error']}"

        result = f"🔍 **Secrets for {attraction_id.replace('_', ' ').title()}**\n\n"

        if data.get("secrets"):
            result += "🤫 **Local Secrets:**\n"
            for i, secret in enumerate(data["secrets"], 1):
                result += f"{i}. {secret}\n"
            result += "\n"

        if data.get("celebrity_sightings"):
            result += "⭐ **Celebrity Sightings:**\n"
            for i, sighting in enumerate(data["celebrity_sightings"], 1):
                result += f"{i}. {sighting}\n"
            result += "\n"

        if data.get("insider_tips"):
            result += "💡 **Insider Tips:**\n"
            for i, tip in enumerate(data["insider_tips"], 1):
                result += f"{i}. {tip}\n"

        return result

    except Exception as e:
        return f"Error: Failed to format attraction secrets: {str(e)}"
