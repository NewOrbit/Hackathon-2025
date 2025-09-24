# Macros MCP Server

Estimate macronutrients (calories, protein, carbs, fat) from natural language food descriptions or recipe-style ingredient lists.

## Features

- Natural language parsing (e.g. "2 eggs and 2 slices wholemeal toast with butter")
- Recipe list parsing (array of ingredients)
- Multiple data providers with graceful fallback:
  - Nutritionix (preferred, natural-language endpoint)
  - Edamam Nutrition API
  - OpenFoodFacts (simple product search; per-100g basis)
- MCP Tools, Resource and Prompt

## Setup

```bash
cd src/mcp/macros-mcp
uv sync
```

### .env configuration (recommended)

Create a `.env` file in this folder with any available API keys:

```
NUTRITIONIX_APP_ID=
NUTRITIONIX_API_KEY=
EDAMAM_APP_ID=
EDAMAM_APP_KEY=
```

These are loaded automatically at startup via `python-dotenv`.

### Environment variables

Create a `.env` or otherwise set variables for best accuracy:

- Nutritionix (recommended):
  - `NUTRITIONIX_APP_ID`
  - `NUTRITIONIX_API_KEY`
- Edamam (optional fallback):
  - `EDAMAM_APP_ID`
  - `EDAMAM_APP_KEY`

If no keys are set, the server falls back to OpenFoodFacts when possible (lower confidence).

### Run the server

- Dev mode UI:

```bash
uv run mcp dev main.py
```

- For agent consumption (HTTP on port 8010):

```bash
uv run main.py
```

## Tools

```python
analyze_macros(description: str) -> Dict
analyze_recipe(ingredients: List[str]) -> Dict
```

## Resource

- `macros://{query}` → formatted text summary

## Prompt

```python
macros_summary_prompt(description: str, target_calories: Optional[int] = None)
```

## Example

```python
analyze_macros("chicken breast 200g with rice 150g and olive oil 1 tbsp")

analyze_recipe([
  "2 eggs",
  "2 slices wholemeal bread",
  "1 tbsp butter"
])
```

## Notes

- Estimates depend on provider data and serving parsing. Treat outputs as approximate.
- Nutritionix/Edamam may apply internal databases and heuristics; OpenFoodFacts results are per 100g and may need scaling.
