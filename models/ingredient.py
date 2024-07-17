import sqlite3
from database.db_manager import get_connection


class Ingredient:
    def __init__(self, name, category_id, _id=None):
        self._id = _id
        self.name = name
        self.category_id = category_id

    def save_to_db(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO ingredients (name, category_id) VALUES (?, ?)",
                (self.name, self.category_id)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Erreur lors de l'insertion de l'ingrédient {self.name}: {e}")
            return False

    def delete(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Supprimer les relations
            cursor.execute('DELETE FROM recipe_ingredients WHERE ingredient_id = ?', (self._id,))

            # Supprimer l'ingrédient
            cursor.execute(
                "DELETE FROM ingredients WHERE id = ?",
                (self._id,)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Erreur lors de la suppression de l'ingrédient {self.name}: {e}")
            return False
