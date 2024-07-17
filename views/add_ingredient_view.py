import customtkinter as ctk
import utils.helpers as utils
import controllers.ingredient_controller as IngredientController
from models.ingredient import Ingredient


class AddIngredientView:
    def __init__(self, root):
        self.root = root
        self.controller = IngredientController

        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(fill="both", expand=True)

        self.name_entry = ctk.CTkEntry(self.frame, placeholder_text="Nom", width=250)
        self.name_entry.pack(pady=5)
        self.name_entry.bind("<Return>", lambda event: self.add_ingredient())

        categories = IngredientController.get_all_categories()
        self.category = ctk.CTkComboBox(self.frame, state="readonly", width=250)
        self.category.pack(pady=10)
        self.category.set(categories[0])
        self.category.configure(values=categories)

        self.add_button = ctk.CTkButton(self.frame, text="Ajouter", command=self.add_ingredient)
        self.add_button.pack(pady=10)

    def add_ingredient(self):
        name = self.name_entry.get()
        category_id = IngredientController.get_category_id_by_category_name(self.category.get())

        if not name or not category_id:
            utils.alert("Tous les champs sont requis")
            return

        if self.controller.already_in_use(name):
            self.error_label = ctk.CTkLabel(self.frame, text=f"{name} est déjà dans la liste", text_color="red")
            self.error_label.pack(pady=5)
            self.error_label.after(3000, self.error_label.destroy)
            return

        ingredient = Ingredient(name=name, category_id=category_id)
        if ingredient.save_to_db():
            self.name_entry.delete(0, ctk.END)
            self.success_label = ctk.CTkLabel(self.frame, text=f"{name} : ajouté à la liste", text_color="green")
            self.success_label.pack(pady=5)
            self.success_label.after(3000, self.success_label.destroy)
        else:
            utils.alert("L'ingrédient n'a pas pu être ajouté")
