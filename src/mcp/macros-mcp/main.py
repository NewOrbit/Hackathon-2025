"""
Macros MCP Server - Estimate macronutrients from a natural language food description.

Integration strategy:
- Nutritionix Natural Language API (preferred when NUTRITIONIX_APP_ID/KEY set)
- Edamam Nutrition Data API (when EDAMAM_APP_ID/KEY set)
- OpenFoodFacts search as a fallback for single-product queries without keys
"""

from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

from nutrition_service import (
    estimate_macros_from_description,
    estimate_macros_from_ingredients,
    build_formatted_resource,
)


load_dotenv()

mcp = FastMCP("Macros", port=8014)


@mcp.tool()
def analyze_macros(description: str) -> Dict[str, Any]:
    """Estimate macronutrients for a natural language food description.

    Args:
        description: Natural language description, e.g. "2 eggs and 2 slices of toast with butter"

    Returns:
        Dict containing total macros, per-item breakdown, serving guidance, source and confidence
    """
    return estimate_macros_from_description(description)


@mcp.tool()
def analyze_recipe(ingredients: List[str]) -> Dict[str, Any]:
    """Estimate macronutrients for a list of ingredient lines (recipe style).

    Args:
        ingredients: List of ingredient lines, e.g. ["2 eggs", "2 slices wholemeal bread", "1 tbsp butter"]

    Returns:
        Dict containing total macros and per-ingredient breakdown
    """
    return estimate_macros_from_ingredients(ingredients)


@mcp.resource("macros://{query}")
def get_macros_resource(query: str) -> str:
    """Formatted macros summary as a resource."""
    data = estimate_macros_from_description(query)
    return build_formatted_resource(query, data)


@mcp.prompt()
def macros_summary_prompt(description: str, target_calories: Optional[int] = None) -> str:
    """Generate a prompt to summarize macros and portion suggestions."""
    base = f"Analyze the following food and estimate macronutrients: {description}."
    if target_calories:
        return base + f" Then suggest a portion to target approximately {target_calories} kcal."
    return base


if __name__ == "__main__":
    mcp.run("streamable-http")
