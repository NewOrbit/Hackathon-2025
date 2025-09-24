def generate_recipes(ingredients):
    """
    Generate suitable recipes based on a list of ingredients.
    Returns a list of recipe strings.
    """
    if not ingredients:
        return ["No ingredients provided."]
    recipes = []

    # Expanded mock recipes
    if "egg" in ingredients and "bread" in ingredients:
        recipes.append("French Toast: Dip bread in beaten eggs, fry until golden.")
    if "egg" in ingredients and "cheese" in ingredients:
        recipes.append("Cheese Omelette: Beat eggs, add cheese, cook in pan.")
    if "tomato" in ingredients and "pasta" in ingredients:
        recipes.append("Tomato Pasta: Cook pasta, add tomato sauce, simmer.")
    if "tomato" in ingredients and "cheese" in ingredients and "bread" in ingredients:
        recipes.append("Cheese & Tomato Sandwich: Layer cheese and tomato between bread slices, grill.")
    if "rice" in ingredients and "chicken" in ingredients:
        recipes.append("Chicken Fried Rice: Stir-fry chicken and rice with veggies.")
    if "rice" in ingredients and "egg" in ingredients:
        recipes.append("Egg Fried Rice: Stir-fry rice with scrambled eggs and vegetables.")
    if "potato" in ingredients and "cheese" in ingredients:
        recipes.append("Cheesy Mashed Potatoes: Boil potatoes, mash, mix with cheese.")
    if "potato" in ingredients and "egg" in ingredients:
        recipes.append("Potato Frittata: Slice potatoes, mix with eggs, bake or fry.")
    if "chicken" in ingredients and "tomato" in ingredients:
        recipes.append("Chicken Tomato Stew: Cook chicken with tomatoes and spices.")
    if "pasta" in ingredients and "cheese" in ingredients:
        recipes.append("Cheesy Pasta: Cook pasta, mix with melted cheese.")
    if "bread" in ingredients and "butter" in ingredients:
        recipes.append("Buttered Toast: Toast bread, spread with butter.")
    if "apple" in ingredients and "cinnamon" in ingredients:
        recipes.append("Cinnamon Apple Slices: Slice apples, sprinkle with cinnamon, bake.")
    if "banana" in ingredients and "milk" in ingredients:
        recipes.append("Banana Smoothie: Blend banana with milk.")
    if "carrot" in ingredients and "potato" in ingredients:
        recipes.append("Carrot & Potato Soup: Boil carrots and potatoes, blend, season.")
    if "lettuce" in ingredients and "tomato" in ingredients:
        recipes.append("Simple Salad: Toss lettuce and tomato with dressing.")
    if "egg" in ingredients and "milk" in ingredients:
        recipes.append("Scrambled Eggs: Beat eggs with milk, cook in pan.")
    if "chicken" in ingredients and "rice" in ingredients and "peas" in ingredients:
        recipes.append("Chicken & Pea Rice Bowl: Cook chicken, rice, and peas together.")
    if "pasta" in ingredients and "spinach" in ingredients:
        recipes.append("Spinach Pasta: Cook pasta, toss with sautéed spinach.")
    if "cheese" in ingredients and "tomato" in ingredients and "pasta" in ingredients:
        recipes.append("Three Cheese Tomato Pasta: Cook pasta, add tomato sauce and three cheeses.")

    # Add more mock variants as needed

    if not recipes:
        recipes.append(f"No matching recipes for: {', '.join(ingredients)}")
    return recipes
