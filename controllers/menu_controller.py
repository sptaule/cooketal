import sqlite3
from database.db_manager import get_connection
import controllers.recipe_controller as RecipeController
from models.menu import Menu


def get_all_menus(start_date=None, end_date=None):
    conn = get_connection()
    menus = []
    try:
        cursor = conn.cursor()
        query = "SELECT id, start_date, end_date FROM menus"
        if start_date is not None and end_date is not None:
            query += f" WHERE start_date >= {start_date} AND end_date <= {end_date}"
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:

            menu_entries = []
            cursor.execute('''
                SELECT menu_id, recipe_id, meal_date, meal_time FROM menu_recipes WHERE menu_id = ?
            ''', (row[0],))
            menu_recipes_entries = cursor.fetchall()
            for menu_recipes_entry in menu_recipes_entries:
                menu_entries.append(
                    (menu_recipes_entry[0], menu_recipes_entry[1], menu_recipes_entry[2], menu_recipes_entry[3])
                )

            menu = Menu(
                _id=row[0],
                start_date=row[1],
                end_date=row[2],
                menu_entries=menu_entries
            )
            menus.append(menu)

        conn.commit()
        return menus
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()


def get_by_id(_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, start_date, end_date FROM menus WHERE id = ?
        ''', (_id,))
        result = cursor.fetchone()

        menu_entries = []
        cursor.execute('''
            SELECT menu_id, recipe_id, meal_date, meal_time FROM menu_recipes WHERE menu_id = ?
        ''', (_id,))
        menu_recipes_entries = cursor.fetchall()

        for menu_recipes_entry in menu_recipes_entries:

            recipe = RecipeController.get_by_id(menu_recipes_entry[1])

            menu_entries.append(
                (menu_recipes_entry[0], menu_recipes_entry[1], menu_recipes_entry[2], menu_recipes_entry[3], recipe)
            )

        menu = Menu(
            _id=_id,
            start_date=result[1],
            end_date=result[2],
            menu_entries=menu_entries
        )

        conn.commit()
        return menu
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()
