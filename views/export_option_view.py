import os
import customtkinter as ctk
import controllers.ingredient_controller as IngredientController
import utils.helpers


class ExportOptionView:
    def __init__(self, root):
        self.root = root
        self.controller = IngredientController

        self.ingredients_frame = ctk.CTkFrame(self.root)
        self.ingredients_frame.pack(pady=20)

        self.ingredients_count = len(self.controller.get_all_ingredients())

        self.ingredients_label = ctk.CTkLabel(
            self.ingredients_frame,
            text="Sauvegarder les ingrédients dans un fichier"
        )
        self.ingredients_label.pack(padx=15, pady=20, side="left")

        self.export_ingredients_button = ctk.CTkButton(
            self.ingredients_frame,
            state="disabled" if self.ingredients_count == 0 else "normal",
            text=f"Exporter {self.ingredients_count} ingrédients",
            command=self.export_ingredients
        )
        self.export_ingredients_button.pack(pady=20, side="left")

    def export_ingredients(self):
        ingredients = self.controller.get_all_ingredients_name()

        # Demander à l'utilisateur où enregistrer le fichier
        file_path = ctk.filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Fichier texte", "*.txt")],
            title="Exporter les ingrédients",
            initialfile="ingredients",
            initialdir=os.path.expanduser("~")
        )

        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("\n".join(ingredients))

            utils.helpers.success(f"{self.ingredients_count} ingrédients exportés")
