import sqlite3
import customtkinter as ctk
from customtkinter import filedialog
import controllers.ingredient_controller as IngredientController
import utils.helpers
import database.db_manager as DB


class ImportOptionView:
    def __init__(self, root):
        self.root = root
        self.controller = IngredientController

        self.ingredients_frame = ctk.CTkFrame(self.root)
        self.ingredients_frame.pack(pady=20)

        self.ingredients_count = len(self.controller.get_all_ingredients())
        self.imported_ingredients = 0

        self.ingredients_label = ctk.CTkLabel(
            self.ingredients_frame,
            text=f"{self.ingredients_count} ingrédient(s) actuellement enregistré(s) dans la base"
        )
        self.ingredients_label.pack(padx=15, pady=20, side="left")

        self.import_ingredients_button = ctk.CTkButton(
            self.ingredients_frame,
            text="Importer des ingrédients",
            command=self.load_file
        )
        self.import_ingredients_button.pack(pady=20, side="left")

    def insert_names(self, names):
        conn = DB.get_connection()
        cursor = conn.cursor()

        inserted_count = 0
        for name in names:
            try:
                cursor.execute('INSERT INTO ingredients (name) VALUES (?)', (name,))
                inserted_count += 1
            except sqlite3.IntegrityError:
                pass

        conn.commit()
        conn.close()
        return inserted_count

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                names = [line.strip() for line in file if line.strip()]
            self.imported_ingredients = self.insert_names(names)

            # Mise à jour de l'interface utilisateur
            self.ingredients_count += self.imported_ingredients
            self.ingredients_label.configure(
                text=f"{self.ingredients_count} ingrédient(s) actuellement enregistré(s) dans la base"
            )

            # Affichage d'un message de succès
            utils.helpers.success(f"Ingrédient(s) importé(s) : {self.imported_ingredients}")

            # Réinitialiser le compteur d'ingrédients importés
            self.imported_ingredients = 0
