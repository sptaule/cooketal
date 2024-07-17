import customtkinter as ctk
import utils.helpers as utils
import controllers.recipe_controller as RecipeController
import controllers.ingredient_controller as IngredientController
from models.recipe import Recipe


def get_ingredients_list():
    ingredients_list = []
    for ingredient in IngredientController.get_all_ingredients():
        ingredients_list.append(ingredient.name)
    return ingredients_list


class ModifyRecipeView:
    def __init__(self, root, recipe_id, show_main_frame_callback):
        self.root = root
        self.controller = RecipeController
        self.recipe_id = recipe_id
        self.recipe = self.controller.get_by_id(recipe_id)
        self.show_main_frame_callback = show_main_frame_callback

        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack()

        self.name_entry = ctk.CTkEntry(self.frame, placeholder_text="Nom", width=200)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, self.recipe.name)

        self.recipe_meal_type = ctk.CTkComboBox(self.frame, values=["Midi", "Soir"], state="readonly")
        self.recipe_meal_type.set(self.recipe.meal_type)
        self.recipe_meal_type.pack(pady=10)

        self.meal_count_frame = ctk.CTkFrame(self.frame, height=50)
        self.meal_count_frame.pack(pady=5)

        self.meal_count = ctk.CTkSlider(
            self.meal_count_frame,
            from_=1,
            to=3,
            number_of_steps=2,
            height=20,
            button_color="#C29F1E",
            button_hover_color="#D4AD21",
            command=self.meal_count_event
        )
        self.meal_count.set(self.recipe.meal_count)
        self.meal_count.pack(padx=10, side="left")

        self.meal_count_label = ctk.CTkLabel(
            master=self.meal_count_frame,
            text=f"{int(self.meal_count.get())} repas",
            height=25, width=25
        )
        self.meal_count_label.pack(padx=10, side="right")

        self.instructions_label = ctk.CTkLabel(self.frame, text="Instructions")
        self.instructions_label.pack(pady=(10, 0))
        self.instructions = ctk.CTkTextbox(self.frame, width=800, height=50)
        self.instructions.pack(pady=5, fill="both", expand=True)
        self.instructions.insert("0.0", self.recipe.instructions)

        self.add_ingredient_button = ctk.CTkButton(
            self.frame,
            text="Ajouter un ingrédient",
            command=self.add_ingredient,
            fg_color="#E2C044",
            hover_color="#C29F1E",
            text_color="black"
        )
        self.add_ingredient_button.pack(pady=10)

        self.ingredients_container = ctk.CTkScrollableFrame(self.frame, fg_color="transparent", height=400)
        self.ingredients_container.pack(padx=10, pady=10, fill="both", expand=True)

        self.action_button_frame = ctk.CTkFrame(self.frame, fg_color="#212121")
        self.action_button_frame.pack()

        self.update_recipe_button = ctk.CTkButton(
            self.action_button_frame,
            text="Mettre à jour la recette",
            command=self.update_recipe,
            width=220,
            height=50
        )
        self.update_recipe_button.pack(pady=10, side="right")

        self.back_button = ctk.CTkButton(
            self.action_button_frame,
            text="",
            command=self.go_back,
            fg_color="#4A4A4A",
            image=utils.get_icon("previous"),
            height=50,
            width=50
        )
        self.back_button.pack(pady=10, padx=15, side="left")

        self.ingredients = []
        self.ingredients_list = get_ingredients_list()

        self.load_ingredients()

    def meal_count_event(self, value):
        self.meal_count_label.configure(text=f"{utils.convert_float_to_int_if_zero(value)} repas")

    def load_ingredients(self):
        for ingredient in self.recipe.ingredients:
            recipe_ingredient = {
                'name': IngredientController.get_by_id(ingredient['id']).name,
                'quantity': ingredient['quantity'],
                'unit': ingredient['unit']
            }
            self.add_ingredient(existing_ingredient=recipe_ingredient)

    def add_ingredient(self, existing_ingredient=None):
        ingredient_frame = ctk.CTkFrame(self.ingredients_container, height=50, fg_color="#333333")
        ingredient_frame.pack(pady=5, fill="both", expand=True)

        def filter_ingredients(event):
            filter_text = ingredient_filter_entry.get().lower()
            filtered_ingredients = [
                ingredient for ingredient in self.ingredients_list if filter_text in ingredient.lower()
            ]
            ingredient_name.configure(values=filtered_ingredients)
            if len(filtered_ingredients) == 1:
                ingredient_name.set(filtered_ingredients[0])

        ingredient_filter_entry = ctk.CTkEntry(
            ingredient_frame,
            width=200,
            placeholder_text="Rechercher un ingrédient..."
        )
        ingredient_filter_entry.pack(padx=10, side="left")
        ingredient_filter_entry.bind("<KeyRelease>", filter_ingredients)

        ingredient_name = ctk.CTkComboBox(ingredient_frame, values=self.ingredients_list, width=300)
        ingredient_name.pack(padx=10, pady=5, fill="both", expand=True)
        if existing_ingredient:
            ingredient_name.set(existing_ingredient['name'])
        else:
            ingredient_name.set("")

        ingredient_quantity = ctk.CTkEntry(ingredient_frame, placeholder_text="Quantité")
        ingredient_quantity.pack(padx=10, pady=5, side="left", expand=True, fill="both")
        if existing_ingredient:
            ingredient_quantity.insert(0, utils.convert_float_to_int_if_zero(existing_ingredient['quantity']))

        self.ingredient_units = RecipeController.get_ingredient_units()
        ingredient_unit = ctk.CTkComboBox(ingredient_frame, values=self.ingredient_units, state="readonly")
        if existing_ingredient:
            ingredient_unit.set(existing_ingredient['unit'])
        else:
            ingredient_unit.set("U")
        ingredient_unit.pack(padx=10, pady=5, side="left", expand=True, fill="both")

        delete_ingredient_button = ctk.CTkButton(
            ingredient_frame,
            text="",
            fg_color="#B9C1CA",
            hover_color="#96A3B0",
            width=30,
            image=utils.get_icon("minus"),
            command=lambda: self.delete_ingredient(ingredient_frame)
        )
        delete_ingredient_button.pack(padx=10, pady=5)

        self.ingredients.append((
            ingredient_frame,
            ingredient_name,
            ingredient_quantity,
            ingredient_unit,
            delete_ingredient_button
        ))

    def delete_ingredient(self, ingredient_frame):
        for i, (frame, name, quantity, unit, button) in enumerate(self.ingredients):
            if frame == ingredient_frame:
                frame.destroy()
                del self.ingredients[i]
                break

    def reset(self):
        self.name_entry.delete(0, ctk.END)
        self.instructions.delete("0.0", "end")
        self.recipe_meal_type.set("Midi")
        while self.ingredients:
            frame, name, quantity, unit, button = self.ingredients.pop()
            frame.destroy()

    def update_recipe(self):
        name = self.name_entry.get()
        meal_type = self.recipe_meal_type.get()
        meal_count = int(self.meal_count.get())
        instructions = self.instructions.get("0.0", "end")

        if not name:
            utils.alert("Tous les champs sont requis")
            return

        ingredients = []
        for frame, name_widget, quantity_widget, unit_widget, button in self.ingredients:
            ingredient_name = name_widget.get()
            ingredient_quantity = quantity_widget.get()
            ingredient_unit = unit_widget.get()

            if not ingredient_name or not ingredient_quantity:
                utils.alert("Tous les champs sont requis")
                return

            ingredients.append({
                'name': ingredient_name,
                'quantity': ingredient_quantity,
                'unit': ingredient_unit
            })

        recipe = Recipe(
            _id=self.recipe_id,
            name=name,
            meal_type=meal_type,
            meal_count=meal_count,
            instructions=instructions,
            ingredients=ingredients
        )
        if not recipe.update():
            utils.alert("Échec de la mise à jour")

        utils.success("La recette a été mise à jour")
        self.go_back()

    def go_back(self):
        self.frame.pack_forget()
        self.show_main_frame_callback()
