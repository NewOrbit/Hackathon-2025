# Nutritional Plan MCP Server

Compose long-term daily calorie and macro targets based on a user profile and goal.

## Features

- Calculates BMR (Mifflin–St Jeor) and TDEE (activity multipliers)
- Goal-driven targets: lose weight, maintain, gain muscle
- Adjustable weekly change rate (kg/week)
- Macro allocation heuristics with protein emphasis
- Tools, Resource and Prompt available

## Setup

```bash
cd src/mcp/nutritional-plan-mcp
uv sync
```

## Run

- Dev UI:

```bash
uv run mcp dev main.py
```

- For agent (HTTP on port 8011):

```bash
uv run main.py
```

## Tools

```python
compose_plan(
  sex: str,
  age_years: int,
  height_cm: float,
  weight_kg: float,
  activity_level: str = "sedentary",
  goal: str = "lose_weight",
  weekly_rate: Optional[float] = None,
) -> Dict
```

## Resource

- `nutrition-plan://{sex}/{age}/{height}/{weight}/{activity}/{goal}` → formatted plan

## Prompt

```python
plan_summary_prompt(goal: str, constraints: Optional[str] = None)
```

## Example

```python
# Example: male, 30y, 170cm, 68kg, lightly active, goal: lose weight ~0.4 kg/week
compose_plan(
  sex="male", age_years=30, height_cm=170, weight_kg=68,
  activity_level="lightly_active", goal="lose_weight", weekly_rate=0.4
)
```

## Notes

- Defaults avoid extreme deficits/surpluses by clamping around BMR.
- Reassess every 2–4 weeks and adjust targets based on progress.
