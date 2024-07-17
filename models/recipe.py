import sqlite3
from database.db_manager import get_connection
import controllers.recipe_controller as RecipeController


class Recipe:
    def __init__(self, name, meal_type, meal_count, instructions, ingredients, _id=None):
        self._id = _id
        self.name = name
        self.meal_type = meal_type
        self.meal_count = meal_count
        self.instructions = instructions
        self.ingredients = ingredients

    def save_to_db(self):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Check name not already taken
            if RecipeController.already_in_use(self.name):
                return False

            # Insérer la recette dans la table recipes
            cursor.execute('''
                  INSERT INTO recipes (name, meal_type, meal_count, instructions)
                  VALUES (?, ?, ?, ?)
              ''', (self.name, self.meal_type, self.meal_count, self.instructions))
            recipe_id = cursor.lastrowid

            for ingredient in self.ingredients:
                ingredient_name = ingredient['name']
                quantity = ingredient['quantity']
                unit = ingredient['unit']

                # Vérifier si l'ingrédient existe
                cursor.execute('SELECT id FROM ingredients WHERE name = ?', (ingredient_name,))
                result = cursor.fetchone()
                ingredient_id = result[0]

                # Insérer la relation recette-ingrédient dans la table recipe_ingredients
                cursor.execute('''
                      INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit)
                      VALUES (?, ?, ?, ?)
                  ''', (recipe_id, ingredient_id, quantity, unit))

            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def update(self):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Insérer la recette dans la table recipes
            cursor.execute('''
                  UPDATE recipes SET name = ?, meal_type = ?, meal_count = ?, instructions = ?
                  WHERE id = ?
              ''', (self.name, self.meal_type, self.meal_count, self.instructions, self._id))

            # Supprimer les anciennes relations
            cursor.execute('DELETE FROM recipe_ingredients WHERE recipe_id = ?', (self._id,))

            for ingredient in self.ingredients:
                ingredient_name = ingredient['name']
                quantity = ingredient['quantity']
                unit = ingredient['unit']

                # Vérifier si l'ingrédient existe déjà dans la table ingredients
                cursor.execute('SELECT id FROM ingredients WHERE name = ?', (ingredient_name,))
                result = cursor.fetchone()

                if result is None:
                    return False

                ingredient_id = result[0]

                # Insérer la relation recette-ingrédient dans la table recipe_ingredients
                cursor.execute('''
                      INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit)
                      VALUES (?, ?, ?, ?)
                  ''', (self._id, ingredient_id, quantity, unit))

            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def delete(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM recipes WHERE id = ?",
                (self._id,)
            )
            cursor.execute(
                "DELETE FROM recipe_ingredients WHERE recipe_id = ?",
                (self._id,)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Erreur lors de la suppression de la recette {self.name}: {e}")
            return False
