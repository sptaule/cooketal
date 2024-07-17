import sqlite3
from database.db_manager import get_connection
from models.ingredient import Ingredient


def get_all_ingredients():
    ingredients = []

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, category_id FROM ingredients ORDER BY name")
        rows = cursor.fetchall()

        for row in rows:
            ingredient = Ingredient(_id=row[0], name=row[1], category_id=row[2])
            ingredients.append(ingredient)

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    return ingredients


def get_all_ingredients_name():
    ingredients = []

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM ingredients ORDER BY name")
        rows = cursor.fetchall()

        for row in rows:
            ingredients.append(row[0])

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    return ingredients


def get_by_id(_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, category_id FROM ingredients WHERE id = ?", (_id,))
        result = cursor.fetchone()
        ingredient = Ingredient(_id=result[0], name=result[1], category_id=result[2])
        conn.commit()
        conn.close()
        return ingredient
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None


def get_name_by_id(_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM ingredients WHERE id = ?", (_id,))
        result = cursor.fetchone()
        name = result[0]
        conn.commit()
        conn.close()
        return name
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None


def get_all_categories():
    categories = []
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM ingredients_categories")
        rows = cursor.fetchall()
        for row in rows:
            categories.append(row[0])
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    return categories


def get_category_by_id(_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ic.id, ic.name, ic.bg_color, ic.text_color
            FROM ingredients i
            LEFT JOIN ingredients_categories ic ON i.category_id = ic.id
            WHERE i.id = ?
        ''', (_id,))
        result = cursor.fetchone()
        if result:
            category_id = result[0]
            category_name = result[1]
            category_bg_color = result[2]
            category_text_color = result[3]
            conn.commit()
            conn.close()
            return category_id, category_name, category_bg_color, category_text_color
        else:
            conn.commit()
            conn.close()
            return None, None, None
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None, None, None


def get_category_name_by_id(_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ic.name 
            FROM ingredients i
            LEFT JOIN ingredients_categories ic ON i.category_id = ic.id
            WHERE i.id = ?
        ''', (_id,))
        result = cursor.fetchone()
        name = result[0]
        conn.commit()
        conn.close()
        return name
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None


def get_category_id_by_category_name(name):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ic.id FROM ingredients_categories ic WHERE ic.name = ?
        ''', (name,))
        result = cursor.fetchone()
        id = result[0]
        conn.commit()
        conn.close()
        return id
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None


def already_in_use(name):
    name = name.lower()
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM ingredients WHERE LOWER(name) = ?", (name,))
        result = cursor.fetchone()

        if result is None:
            return False

        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None


def update_ingredient(index, new_name, new_category):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE ingredients SET name = ?, category_id = ? WHERE id = ?", (new_name, new_category, index))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False
