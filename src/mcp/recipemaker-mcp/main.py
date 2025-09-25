from mcp.server.fastmcp import FastMCP
from generator import generate_recipes

# Create an MCP server
# you can add the port here so that it doesnt clash with other mcp servers
mcp = FastMCP("myname", port=8123)

# Add an addition tool

# Recipe generator tool
@mcp.tool()
def recipe_from_ingredients(ingredients: list[str]) -> list[str]:
    """Generate suitable recipes from a list of ingredients"""
    return generate_recipes(ingredients)


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

# Add a recipe prompt
@mcp.prompt()
def recipe_suggestion_prompt(ingredients: list[str]) -> str:
    """Generate a prompt for recipe suggestions"""
    if not ingredients:
        return "Please provide some ingredients to get recipe suggestions."
    return f"Suggest recipes using the following ingredients: {', '.join(ingredients)}"

# Add a recipe resource
@mcp.resource("recipe://{ingredients}")
def get_recipe_resource(ingredients: list[str]) -> str:
    """Get recipes as a formatted resource"""
    recipes = generate_recipes(ingredients)
    return "\n".join(recipes)
    
if __name__ == "__main__":
   mcp.run("streamable-http")