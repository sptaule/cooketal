from tkcalendar import DateEntry
from collections import defaultdict
import customtkinter as ctk
import controllers.menu_controller as MenuController
import controllers.ingredient_controller as IngredientController
import controllers.recipe_controller as RecipeController
import utils.helpers


class HistoryMenuView:
    def __init__(self, root):
        self.root = root
        self.controller = MenuController

        self.is_changing_meal = False

        self.frame = ctk.CTkFrame(self.root, fg_color="#333333")
        self.frame.pack()

        # Date de début (optionnel)
        self.label_start_date = ctk.CTkLabel(self.frame, text="Date de début :")
        self.label_start_date.pack(padx=10, pady=10, side="left")
        self.start_date_var = ctk.StringVar()
        self.start_date = DateEntry(self.frame, textvariable=self.start_date_var)
        self.start_date.pack(padx=10, pady=10, side="left")
        self.start_date_var.set("")

        # Date de fin (optionnel)
        self.label_end_date = ctk.CTkLabel(self.frame, text="Date de fin :")
        self.label_end_date.pack(padx=10, pady=10, side="left")
        self.end_date_var = ctk.StringVar()
        self.end_date = DateEntry(self.frame, textvariable=self.end_date_var)
        self.end_date.pack(padx=10, pady=10, side="left")
        self.end_date_var.set("")

        # Bouton pour générer le menu
        self.display_menus_button = ctk.CTkButton(self.frame, text="Rechercher", command=self.display_menus)
        self.display_menus_button.pack(padx=10, pady=10, side="left")

        # Frame pour afficher le menu généré
        self.menu_frame = ctk.CTkScrollableFrame(self.root, fg_color="#444444", height=500)
        self.menu_frame.pack(fill="x", pady=15)

        self.display_menus()

    def display_menus(self):
        for element in self.menu_frame.winfo_children():
            element.destroy()

        menus = self.controller.get_all_menus()

        for menu in menus:
            frame = ctk.CTkFrame(self.menu_frame)
            frame.pack(pady=(0, 5), fill="x", expand=True)

            start_date = utils.helpers.format_date_str(menu.start_date)
            end_date = utils.helpers.format_date_str(menu.end_date)
            delta_days = utils.helpers.calculate_days_between_dates(menu.start_date, menu.end_date)
            date_label = ctk.CTkLabel(frame, text=f"Du {start_date} au {end_date} ({delta_days})")
            date_label.pack(pady=10, expand=True, side="left")

            menu_info_button = ctk.CTkButton(
                frame,
                text="Voir le menu",
                command=lambda: self.show_menu_info(menu._id)
            )
            menu_info_button.pack(padx=10, side="left")

            menu_ingredients_button = ctk.CTkButton(
                frame,
                text="Voir les ingrédients",
                command=lambda: self.show_menu_ingredients(menu._id)
            )
            menu_ingredients_button.pack(padx=10, side="left")

    def show_menu_info(self, menu_id):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.menu_info_frame = ctk.CTkFrame(self.root)
        self.menu_info_frame.pack(fill="both", expand=True)

        menu = MenuController.get_by_id(menu_id)

        self.menu_info_container = ctk.CTkScrollableFrame(self.menu_info_frame)
        self.menu_info_container.pack(fill="both", expand=True)

        for i, (menu_id, recipe_id, date, meal_type, recipe) in enumerate(menu.menu_entries):
            frame = ctk.CTkFrame(self.menu_info_container)
            frame.pack(fill="x", expand=True, pady=(5 if i > 0 else 0, 0))
            day_label = ctk.CTkLabel(frame, text=utils.helpers.format_date_str(date), width=400)
            day_label.pack(padx=10, side="left")
            recipe_meal_type_label = ctk.CTkLabel(frame, text=meal_type, width=400)
            recipe_meal_type_label.pack(padx=10, side="left")
            recipe_name_label = ctk.CTkLabel(frame, text=recipe.name, width=400)
            recipe_name_label.pack(padx=10, side="left")

            if utils.helpers.is_time_of_day(date, meal_type):
                frame.configure(fg_color="#FBBE4B")
                day_label.configure(text_color="#1B1B1B")
                recipe_meal_type_label.configure(text_color="#1B1B1B")
                recipe_name_label.configure(text_color="#1B1B1B")

        self.back_to_menus_button = ctk.CTkButton(
            self.menu_info_frame,
            text="Retour aux menus",
            command=self.back_to_menus,
            fg_color="#4A4A4A",
            image=utils.helpers.get_icon("previous"),
            height=30,
            width=50
        )
        self.back_to_menus_button.pack(pady=(10, 0), side="left")

    def show_menu_ingredients(self, menu_id):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.menu_ingredients_frame = ctk.CTkFrame(self.root)
        self.menu_ingredients_frame.pack(fill="both", expand=True)

        menu = MenuController.get_by_id(menu_id)

        self.menu_ingredients_container = ctk.CTkScrollableFrame(self.menu_ingredients_frame)
        self.menu_ingredients_container.pack(fill="both", expand=True)

        # Initialiser le dictionnaire en dehors de la boucle principale
        ingredient_quantities = defaultdict(lambda: defaultdict(lambda: {'quantity': 0.0, 'recipes': set()}))
        processed_recipes = set()  # Pour éviter de doubler les ingrédients pour la même recette

        for i, (menu_id, recipe_id, date, meal_type, recipe) in enumerate(menu.menu_entries):

            recipe_name = RecipeController.get_name_by_id(recipe_id)

            if (recipe_id, recipe.meal_count) in processed_recipes:
                continue  # Skip if this recipe has already been processed with the same meal_count

            processed_recipes.add((recipe_id, recipe.meal_count))

            for index, (ingredient) in enumerate(recipe.ingredients):
                ingredient_id = ingredient['id']
                quantity = ingredient['quantity']
                unit = ingredient['unit']
                # Ajouter la quantité à la quantité totale pour cette unité
                ingredient_quantities[ingredient_id][unit]['quantity'] += quantity
                # Ajouter le nom de la recette dans la liste des recettes correspondantes
                ingredient_quantities[ingredient_id][unit]['recipes'].add(recipe_name)

        category_grouped_results = defaultdict(list)
        category_details = {}

        # Après avoir parcouru toutes les entrées du menu, afficher les résultats
        for ingredient_id, units in ingredient_quantities.items():
            ingredient_name = IngredientController.get_name_by_id(ingredient_id)
            category_id, category_name, category_bg_color, category_text_color = IngredientController.get_category_by_id(ingredient_id)

            # Stocker les détails de la catégorie
            if category_id not in category_details:
                category_details[category_id] = {
                    'name': category_name,
                    'bg_color': category_bg_color,
                    'text_color': category_text_color
                }

            quantities_list = []
            recipe_names = set()
            for unit, data in units.items():
                quantity = data['quantity']
                if quantity.is_integer():
                    quantity = int(quantity)
                quantities_list.append(f"{quantity} {unit}")
                recipe_names.update(data['recipes'])
            concatenated_quantities = " + ".join(quantities_list)
            recipes_str = ", ".join(recipe_names)
            category_grouped_results[category_id].append([ingredient_name, concatenated_quantities, recipes_str])

        # Trier les catégories par leur ID
        sorted_category_ids = sorted(category_grouped_results.keys())

        # Créer des sections par catégorie avec des entêtes
        for idx, category_id in enumerate(sorted_category_ids):
            category_name = category_details[category_id]['name']
            bg_color = '#' + category_details[category_id]['bg_color']
            text_color = '#' + category_details[category_id]['text_color']

            category_frame = ctk.CTkFrame(self.menu_ingredients_container, fg_color=bg_color)
            category_frame.pack(fill="x", expand=True, pady=(10 if idx > 0 else 0, 0))

            category_label = ctk.CTkLabel(
                category_frame,
                text=category_name,
                text_color=text_color,
                font=ctk.CTkFont(size=14, weight="bold")
            )
            category_label.pack(padx=10, pady=5, anchor="w")

            results = category_grouped_results[category_id]
            for i, result in enumerate(results):
                ingredient_frame = ctk.CTkFrame(self.menu_ingredients_container)
                ingredient_frame.pack(fill="x", expand=True, pady=(5, 0))

                ingredient_name_label = ctk.CTkLabel(ingredient_frame, text=result[0], width=250)
                ingredient_name_label.pack(padx=10, side="left")
                ingredient_quantities_label = ctk.CTkLabel(ingredient_frame, text=result[1], width=300)
                ingredient_quantities_label.pack(padx=10, side="left")
                ingredient_recipes_label = ctk.CTkLabel(
                    ingredient_frame,
                    text=result[2],
                    width=600,
                    font=ctk.CTkFont(size=11)
                )
                ingredient_recipes_label.pack(padx=10, side="left")

        self.back_to_menus_button = ctk.CTkButton(
            self.menu_ingredients_frame,
            text="Retour aux menus",
            command=self.back_to_menus,
            fg_color="#4A4A4A",
            image=utils.helpers.get_icon("previous"),
            height=30,
            width=50
        )
        self.back_to_menus_button.pack(pady=(10, 0), side="left")

    def back_to_menus(self):
        if hasattr(self, 'menu_info_frame'):
            for widget in self.menu_info_frame.winfo_children():
                widget.destroy()
            self.menu_info_frame.destroy()
        if hasattr(self, 'menu_ingredients_frame'):
            for widget in self.menu_ingredients_frame.winfo_children():
                widget.destroy()
            self.menu_ingredients_frame.destroy()
        HistoryMenuView(self.root)
