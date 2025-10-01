"""
Nutrition Trivia service with MCP tools for nutrition secrets and insider information.
"""

import random
from typing import Dict, Any, List, Optional
from dataclasses import asdict

from nutrition_config import NUTRITION_TRIVIA_DATABASE, NUTRITION_TIP_CATEGORIES, NUTRITION_SECRET_TYPES
from models import NutritionSecret, NutritionResponse

try:
    from config import SECRET_DATABASE, TIP_CATEGORIES, SECRET_TYPES
except ImportError:
    SECRET_DATABASE = {}
    TIP_CATEGORIES = {}
    SECRET_TYPES = []


# Nutrition trivia functions
def get_nutrition_secret(nutrition_topic: str) -> Dict[str, Any]:
    """Get a random nutrition secret, celebrity fact, or nutrition tip for a topic

    Args:
        nutrition_topic: ID of the nutrition topic (e.g., "protein", "carbs", "vitamins")

    Returns:
        NutritionResponse object as dictionary or error dict
    """
    try:
        nutrition_topic = nutrition_topic.lower().replace(" ", "_")

        if nutrition_topic not in NUTRITION_TRIVIA_DATABASE:
            return {
                "error": f"Nutrition topic '{nutrition_topic}' not found in our nutrition database"
            }

        topic_data = NUTRITION_TRIVIA_DATABASE[nutrition_topic]

        # Collect all available content
        all_content = []
        for secret_type in NUTRITION_SECRET_TYPES:
            if secret_type in topic_data:
                for content in topic_data[secret_type]:
                    all_content.append({"type": secret_type, "content": content})

        if not all_content:
            return {"error": f"No nutrition secrets found for topic '{nutrition_topic}'"}

        # Pick a random item
        random_item = random.choice(all_content)

        nutrition_response = NutritionResponse(
            nutrition_topic=nutrition_topic,
            secret_type=random_item["type"],
            content=random_item["content"],
            category=random_item["type"],
        )

        return asdict(nutrition_response)

    except Exception as e:
        return {"error": f"Failed to get nutrition secret: {str(e)}"}


def get_nutrition_tips(
    nutrition_topic: str, tip_type: Optional[str] = None
) -> Dict[str, Any]:
    """Get nutrition tips for a specific topic, optionally filtered by type

    Args:
        nutrition_topic: ID of the nutrition topic
        tip_type: Optional tip category filter ("macros", "vitamins", "hydration", etc.)

    Returns:
        List of nutrition tips as dictionary or error dict
    """
    try:
        nutrition_topic = nutrition_topic.lower().replace(" ", "_")

        if nutrition_topic not in NUTRITION_TRIVIA_DATABASE:
            return {
                "error": f"Nutrition topic '{nutrition_topic}' not found in our nutrition database"
            }

        topic_data = NUTRITION_TRIVIA_DATABASE[nutrition_topic]

        if "nutrition_tips" not in topic_data:
            return {"error": f"No nutrition tips found for topic '{nutrition_topic}'"}

        tips = topic_data["nutrition_tips"]

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
                    "nutrition_topic": nutrition_topic,
                    "tip_type": tip_type,
                    "tips": [],
                    "message": f"No tips found matching category '{tip_type}'",
                }

        return {
            "nutrition_topic": nutrition_topic,
            "tip_type": tip_type or "all",
            "tips": tips,
            "total_count": len(tips),
        }

    except Exception as e:
        return {"error": f"Failed to get nutrition tips: {str(e)}"}


def get_celebrity_nutrition(location: str) -> Dict[str, Any]:
    """Get celebrity nutrition facts and secrets for a topic

    Args:
        location: Nutrition topic name (e.g., "protein", "carbs", "vitamins")

    Returns:
        Celebrity nutrition facts as dictionary or error dict
    """
    try:
        location = location.lower().replace(" ", "_")

        if location not in NUTRITION_TRIVIA_DATABASE:
            return {"error": f"Nutrition topic '{location}' not found in our nutrition database"}

        topic_data = NUTRITION_TRIVIA_DATABASE[location]

        if "celebrity_nutrition" not in topic_data:
            return {"error": f"No celebrity nutrition facts found for topic '{location}'"}

        celebrity_facts = topic_data["celebrity_nutrition"]

        # Get a random celebrity fact
        random_fact = random.choice(celebrity_facts) if celebrity_facts else None

        return {
            "nutrition_topic": location,
            "celebrity_fact": random_fact,
            "all_facts": celebrity_facts,
            "total_count": len(celebrity_facts),
        }

    except Exception as e:
        return {"error": f"Failed to get celebrity nutrition: {str(e)}"}


def get_all_nutrition_secrets(nutrition_topic: str) -> Dict[str, Any]:
    """Get all nutrition secrets, celebrity facts, and tips for a topic

    Args:
        nutrition_topic: ID of the nutrition topic

    Returns:
        Complete NutritionSecret object as dictionary or error dict
    """
    try:
        nutrition_topic = nutrition_topic.lower().replace(" ", "_")

        if nutrition_topic not in NUTRITION_TRIVIA_DATABASE:
            return {
                "error": f"Nutrition topic '{nutrition_topic}' not found in our nutrition database"
            }

        topic_data = NUTRITION_TRIVIA_DATABASE[nutrition_topic]

        nutrition_secret = NutritionSecret(
            nutrition_topic=nutrition_topic,
            nutrition_secrets=topic_data.get("nutrition_secrets", []),
            celebrity_nutrition=topic_data.get("celebrity_nutrition", []),
            nutrition_tips=topic_data.get("nutrition_tips", []),
        )

        return asdict(nutrition_secret)

    except Exception as e:
        return {"error": f"Failed to get nutrition secrets: {str(e)}"}


def get_available_nutrition_topics() -> Dict[str, Any]:
    """Get list of all nutrition topics with secrets available

    Returns:
        List of available nutrition topics as dictionary
    """
    try:
        topics = list(NUTRITION_TRIVIA_DATABASE.keys())

        return {
            "total_topics": len(topics),
            "topics": topics,
            "tip_categories": list(NUTRITION_TIP_CATEGORIES.keys()),
            "secret_types": NUTRITION_SECRET_TYPES,
        }

    except Exception as e:
        return {"error": f"Failed to get available nutrition topics: {str(e)}"}


def format_nutrition_secrets(nutrition_topic: str) -> str:
    """Format all nutrition secrets for a topic as a readable string

    Args:
        nutrition_topic: ID of the nutrition topic

    Returns:
        Formatted string with all nutrition secrets
    """
    try:
        data = get_all_nutrition_secrets(nutrition_topic)
        if "error" in data:
            return f"Error: {data['error']}"

        result = f"🥗 **Nutrition Secrets for {nutrition_topic.replace('_', ' ').title()}**\n\n"

        if data.get("nutrition_secrets"):
            result += "🔬 **Nutrition Secrets:**\n"
            for i, secret in enumerate(data["nutrition_secrets"], 1):
                result += f"{i}. {secret}\n"
            result += "\n"

        if data.get("celebrity_nutrition"):
            result += "⭐ **Celebrity Nutrition Facts:**\n"
            for i, fact in enumerate(data["celebrity_nutrition"], 1):
                result += f"{i}. {fact}\n"
            result += "\n"

        if data.get("nutrition_tips"):
            result += "💡 **Nutrition Tips:**\n"
            for i, tip in enumerate(data["nutrition_tips"], 1):
                result += f"{i}. {tip}\n"

        return result

    except Exception as e:
        return f"Error: Failed to format nutrition secrets: {str(e)}"
