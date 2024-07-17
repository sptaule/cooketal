from database.db_manager import get_connection


class Menu:
    def __init__(self, start_date, end_date, menu_entries=None, _id=None):
        self._id = _id
        self.start_date = start_date
        self.end_date = end_date
        self.menu_entries = menu_entries

    def save_to_db(self):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Créer le menu
            cursor.execute(
                "INSERT INTO menus (start_date, end_date) VALUES (?, ?)",
                (self.start_date, self.end_date)
            )
            menu_id = cursor.lastrowid

            for menu_entry in self.menu_entries:

                meal_date = menu_entry[0]
                lunch_recipe = menu_entry[1]
                dinner_recipe = menu_entry[2]

                # Obtenir l'id de la recette (midi)
                cursor.execute('''SELECT id, meal_type FROM recipes WHERE name = ?''', (lunch_recipe.name,))
                result = cursor.fetchone()
                lunch_recipe_id = result[0]
                lunch_recipe_meal_type = result[1]

                # Insérer la relation menu-recettes dans la table menu_recipes (midi)
                cursor.execute('''
                    INSERT INTO menu_recipes (menu_id, recipe_id, meal_date, meal_time)
                    VALUES (?, ?, ?, ?)
                ''', (menu_id, lunch_recipe_id, meal_date, lunch_recipe_meal_type))

                # Obtenir l'id de la recette (soir)
                cursor.execute('''SELECT id, meal_type FROM recipes WHERE name = ?''', (dinner_recipe.name,))
                result = cursor.fetchone()
                dinner_recipe_id = result[0]
                lunch_recipe_meal_type = result[1]

                # Insérer la relation menu-recettes dans la table menu_recipes (midi)
                cursor.execute('''
                    INSERT INTO menu_recipes (menu_id, recipe_id, meal_date, meal_time)
                    VALUES (?, ?, ?, ?)
                ''', (menu_id, dinner_recipe_id, meal_date, lunch_recipe_meal_type))

            conn.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
