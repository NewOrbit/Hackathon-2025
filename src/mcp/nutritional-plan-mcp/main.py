"""
Nutritional Plan MCP - Compose long-term daily calorie and macro targets based on user profile and goal.
"""

from typing import Dict, Any, Optional

from mcp.server.fastmcp import FastMCP

from plan_service import UserProfile, plan_calories, build_text_plan


mcp = FastMCP("NutritionalPlan", port=8013)


@mcp.tool()
def compose_plan(
    sex: str,
    age_years: int,
    height_cm: float,
    weight_kg: float,
    activity_level: str = "sedentary",
    goal: str = "lose_weight",
    weekly_rate: Optional[float] = None,
) -> Dict[str, Any]:
    """Compose a nutrition plan with daily calories and macros.

    Args:
        sex: "male" or "female"
        age_years: Age in years
        height_cm: Height in centimeters
        weight_kg: Weight in kilograms
        activity_level: sedentary|lightly_active|moderately_active|very_active|extra_active
        goal: lose_weight|maintain|gain_muscle
        weekly_rate: Optional kg/week rate (e.g., 0.4 for loss, 0.25 for gain)
    """
    profile = UserProfile(
        sex=sex,
        age_years=age_years,
        height_cm=height_cm,
        weight_kg=weight_kg,
        activity_level=activity_level,
        goal=goal,
        weekly_rate=weekly_rate,
    )
    return plan_calories(profile)


@mcp.resource("nutrition-plan://{sex}/{age}/{height}/{weight}/{activity}/{goal}")
def plan_resource(
    sex: str,
    age: int,
    height: float,
    weight: float,
    activity: str,
    goal: str,
) -> str:
    profile = UserProfile(
        sex=sex,
        age_years=age,
        height_cm=height,
        weight_kg=weight,
        activity_level=activity,
        goal=goal,
    )
    data = plan_calories(profile)
    return build_text_plan(profile, data)


@mcp.prompt()
def plan_summary_prompt(goal: str, constraints: Optional[str] = None) -> str:
    base = f"Create a concise nutrition plan summary to {goal}."
    if constraints:
        base += f" Consider: {constraints}."
    base += " Include daily calories, macro split, and 3 guidance bullets."
    return base


if __name__ == "__main__":
    mcp.run("streamable-http")
