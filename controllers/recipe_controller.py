import sqlite3
from database.db_manager import get_connection
from models.recipe import Recipe


def get_all_recipes(meal_type=None):
    recipes = []
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT id, name, meal_type, meal_count, instructions FROM recipes"
        if meal_type is not None:
            query += f" WHERE meal_type = '{meal_type}'"
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            recipe = Recipe(
                _id=row[0],
                name=row[1],
                meal_type=row[2],
                meal_count=row[3],
                instructions=row[4],
                ingredients=get_recipe_ingredients(row[0])
            )
            recipes.append(recipe)

        conn.commit()
        conn.close()
        return recipes
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None


def get_recipe_ingredients(_id):
    recipe_ingredients = []
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ingredient_id, quantity, unit FROM recipe_ingredients WHERE recipe_id = ?
        ''', (_id,))
        rows = cursor.fetchall()

        for row in rows:
            recipe_ingredients.append({
                'id': row[0],
                'quantity': row[1],
                'unit': row[2]
            })

        conn.commit()
        conn.close()
        return recipe_ingredients
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None


def already_in_use(name):
    name = name.lower()
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM recipes WHERE LOWER(name) = ?", (name,))
        result = cursor.fetchone()

        if result is None:
            return False

        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None


def get_ingredient_units():
    units = []
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM ingredients_units")
        rows = cursor.fetchall()

        for row in rows:
            units.append(row[0])

        conn.commit()
        conn.close()
        return units
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None


def get_by_id(_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, meal_type, meal_count, instructions FROM recipes WHERE id = ?", (_id,))
        result = cursor.fetchone()

        if result is None:
            return None

        ingredients = get_recipe_ingredients(_id=result[0])
        recipe = Recipe(
            _id=result[0],
            name=result[1],
            meal_type=result[2],
            meal_count=result[3],
            instructions=result[4],
            ingredients=ingredients
        )
        conn.commit()
        conn.close()
        return recipe
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None


def get_name_by_id(_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM recipes WHERE id = ?", (_id,))
        result = cursor.fetchone()

        if result is None:
            return None

        name = result[0]
        conn.commit()
        conn.close()
        return name
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
