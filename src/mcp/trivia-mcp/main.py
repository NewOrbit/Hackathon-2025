"""
Nutrition Trivia MCP Server - Nutrition secrets, celebrity facts, and insider tips.

To run this server:
    uv run mcp dev main.py

Provides nutrition secrets, celebrity nutrition facts, and nutrition tips.
"""

from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from trivia_service import (
    # Nutrition trivia functions
    get_nutrition_secret,
    get_nutrition_tips,
    get_celebrity_nutrition,
    get_all_nutrition_secrets,
    get_available_nutrition_topics,
    format_nutrition_secrets,
)

mcp = FastMCP("Trivia", port=8012)


# Nutrition trivia tools
@mcp.tool()
def get_nutrition_secret_tool(nutrition_topic: str) -> Dict[str, Any]:
    """Get a random nutrition secret, celebrity fact, or nutrition tip for a topic

    Args:
        nutrition_topic: ID of the nutrition topic (e.g., "protein", "carbs", "vitamins")

    Returns:
        NutritionResponse object as dictionary with random nutrition secret/fact/tip
    """
    return get_nutrition_secret(nutrition_topic)


@mcp.tool()
def get_nutrition_tips_tool(
    nutrition_topic: str, tip_type: Optional[str] = None
) -> Dict[str, Any]:
    """Get nutrition tips for a specific topic, optionally filtered by type

    Args:
        nutrition_topic: ID of the nutrition topic
        tip_type: Optional tip category filter ("macros", "vitamins", "hydration", etc.)

    Returns:
        List of nutrition tips as dictionary
    """
    return get_nutrition_tips(nutrition_topic, tip_type)


@mcp.tool()
def get_celebrity_nutrition_tool(nutrition_topic: str) -> Dict[str, Any]:
    """Get celebrity nutrition facts and secrets for a topic

    Args:
        nutrition_topic: Nutrition topic name (e.g., "protein", "carbs", "vitamins")

    Returns:
        Celebrity nutrition facts as dictionary
    """
    return get_celebrity_nutrition(nutrition_topic)


@mcp.tool()
def get_all_nutrition_secrets_tool(nutrition_topic: str) -> Dict[str, Any]:
    """Get all nutrition secrets, celebrity facts, and tips for a topic

    Args:
        nutrition_topic: ID of the nutrition topic

    Returns:
        Complete NutritionSecret object as dictionary
    """
    return get_all_nutrition_secrets(nutrition_topic)


@mcp.tool()
def get_available_nutrition_topics_tool() -> Dict[str, Any]:
    """Get list of all nutrition topics with secrets available

    Returns:
        List of available nutrition topics as dictionary
    """
    return get_available_nutrition_topics()


# Nutrition trivia resources
@mcp.resource("nutrition://topic/{nutrition_topic}")
def get_nutrition_secrets_resource(nutrition_topic: str) -> str:
    """Get all nutrition secrets for a topic as a formatted resource"""
    return format_nutrition_secrets(nutrition_topic)


@mcp.resource("nutrition://topics")
def get_available_nutrition_topics_resource() -> str:
    """Get list of available nutrition topics as a formatted resource"""
    data = get_available_nutrition_topics()
    if "error" in data:
        return f"Error: {data['error']}"

    result = "🥗 **Available Nutrition Topics with Secrets**\n\n"
    result += f"Total Topics: {data['total_topics']}\n\n"

    for topic in data["topics"]:
        result += f"• **{topic.replace('_', ' ').title()}**\n"

    result += f"\n**Tip Categories:** {', '.join(data['tip_categories'])}\n"
    result += f"**Secret Types:** {', '.join(data['secret_types'])}\n"

    return result


# Nutrition trivia prompts
@mcp.prompt()
def nutrition_secrets_prompt(nutrition_topic: str) -> str:
    """Generate a prompt for discovering nutrition secrets"""
    return f"""Please help discover and share nutrition secrets about {nutrition_topic.replace('_', ' ').title()}, including:
1. Scientific nutrition facts and research
2. Celebrity nutrition secrets and diets
3. Insider tips for optimal nutrition
4. Hidden benefits and surprising facts
5. Common myths and misconceptions
6. Best practices for health and performance
7. Nutrient timing and absorption secrets
8. Professional athlete and celebrity nutrition strategies

Focus on providing insider knowledge that only nutrition experts and celebrities would know."""


@mcp.prompt()
def celebrity_nutrition_prompt(nutrition_topic: str) -> str:
    """Generate a prompt for discovering celebrity nutrition facts"""
    return f"""Please help uncover celebrity nutrition secrets for {nutrition_topic.replace('_', ' ').title()}, including:
1. Celebrity diets and nutrition strategies
2. Famous people's nutrition secrets and routines
3. Celebrity nutrition drama and controversies
4. Professional athlete nutrition facts
5. Celebrity nutrition transformations
6. Famous people's supplement routines
7. Celebrity nutrition tips and tricks
8. Insider celebrity nutrition knowledge

Share the kind of nutrition knowledge that makes you feel like a celebrity insider."""


@mcp.prompt()
def nutrition_optimization_prompt(nutrition_topic: str) -> str:
    """Generate a prompt for nutrition optimization and performance"""
    return f"""Please help with nutrition optimization for {nutrition_topic.replace('_', ' ').title()}, including:
1. Performance-enhancing nutrition strategies
2. Scientific nutrition facts and research
3. Optimal nutrient timing and combinations
4. Nutrition for specific goals (muscle building, fat loss, performance)
5. Supplement strategies and recommendations
6. Nutrition myths and facts
7. Professional and celebrity nutrition secrets
8. Advanced nutrition techniques and tips

Focus on the most effective nutrition strategies used by professionals and celebrities."""


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
