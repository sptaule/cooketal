import datetime
import random
import tkinter as tk
from tkcalendar import DateEntry
import customtkinter as ctk
import controllers.recipe_controller as RecipeController
import controllers.menu_controller as MenuController
from models.menu import Menu
import utils.helpers


class GenerateMenuView:
    def __init__(self, root):
        self.root = root
        self.controller = MenuController

        self.is_changing_meal = False

        self.frame = ctk.CTkFrame(self.root, fg_color="#333333")
        self.frame.pack()

        # Champ de saisie de la date de début
        self.label_start_date = ctk.CTkLabel(self.frame, text="Date de début :")
        self.label_start_date.pack(padx=10, pady=10, side="left")

        self.start_date_entry = DateEntry(
            self.frame,
            locale="fr",
            width=12,
            day=utils.helpers.get_date()[0],
            month=utils.helpers.get_date()[1],
            year=utils.helpers.get_date()[2]
        )
        self.start_date_entry.pack(padx=10, pady=10, side="left")

        # Champ de saisie de la date de fin
        self.label_end_date = ctk.CTkLabel(self.frame, text="Date de fin :")
        self.label_end_date.pack(padx=10, pady=10, side="left")

        self.end_date_entry = DateEntry(
            self.frame,
            locale="fr",
            width=12,
            day=utils.helpers.get_date(delta=15)[0],
            month=utils.helpers.get_date(delta=15)[1],
            year=utils.helpers.get_date(delta=15)[2]
        )
        self.end_date_entry.pack(padx=10, pady=10, side="left")

        # Bouton pour générer le menu
        self.generate_menu_button = ctk.CTkButton(self.frame, text="Générer", command=self.generate_menu)
        self.generate_menu_button.pack(padx=10, pady=10)

        # Frame pour afficher le menu généré
        self.menu_frame = ctk.CTkScrollableFrame(self.root, fg_color="#444444", height=500)
        self.menu_frame.pack(fill="x", pady=15)

        self.save_menu_button = ctk.CTkButton(
            self.root,
            text="Enregistrer le menu",
            height=55,
            image=utils.helpers.get_icon("check"),
            command=self.save_menu
        )
        self.save_menu_button.pack(pady=10, side="right", ipadx=25)

    def save_menu(self):
        menu = Menu(
            start_date=self.start_date_entry.get_date(),
            end_date=self.end_date_entry.get_date(),
            menu_entries=self.generated_menu
        )
        if menu.save_to_db():
            utils.helpers.success("Menu sauvegardé")
            return
        utils.helpers.alert("Échec lors de la sauvegarde du menu")

    def generate_menu(self):
        try:
            start_date = self.start_date_entry.get_date()
            end_date = self.end_date_entry.get_date()
            if start_date > end_date:
                utils.helpers.alert("La date de début doit être antérieure à la date de fin")
                return

            recipes = RecipeController.get_all_recipes()
            if not recipes:
                utils.helpers.alert("Aucune recette trouvée.")
                return

            lunch_recipes = [recipe for recipe in recipes if recipe.meal_type == 'Midi']
            dinner_recipes = [recipe for recipe in recipes if recipe.meal_type == 'Soir']

            if not lunch_recipes or not dinner_recipes:
                utils.helpers.alert("Pas assez de recettes disponibles pour générer le menu")
                return

            menu_days = (end_date - start_date).days + 1
            self.generated_menu = []

            current_date = start_date

            while len(self.generated_menu) < menu_days:
                # Select lunch recipe
                if not lunch_recipes:
                    break
                lunch_recipe = random.choice(lunch_recipes)
                lunch_recipes.remove(lunch_recipe)

                for _ in range(lunch_recipe.meal_count):
                    if len(self.generated_menu) >= menu_days:
                        break
                    self.generated_menu.append((current_date, lunch_recipe, None))
                    current_date += datetime.timedelta(days=1)

            current_date = start_date
            index = 0
            while index < menu_days:
                if not dinner_recipes:
                    break
                dinner_recipe = random.choice(dinner_recipes)
                dinner_recipes.remove(dinner_recipe)

                for _ in range(dinner_recipe.meal_count):
                    if index >= menu_days:
                        break
                    date, lunch_recipe, _ = self.generated_menu[index]
                    self.generated_menu[index] = (date, lunch_recipe, dinner_recipe)
                    index += 1

            self.display_menu(self.generated_menu)

        except Exception as e:
            utils.helpers.alert(f"Une erreur s'est produite : {e}")

    def display_menu(self, menu):
        # Clear previous menu display
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        # Display each day's menu
        for i, (date, lunch_recipe, dinner_recipe) in enumerate(menu):
            row_frame = ctk.CTkFrame(self.menu_frame)
            row_frame.pack(fill="x", pady=(5 if i > 0 else 0, 0))

            ctk.CTkLabel(
                row_frame,
                text=utils.helpers.format_date_fr(date),
                width=400
            ).pack(side="left", padx=10, pady=5)

            self.lunch_label = ctk.CTkLabel(row_frame, text=lunch_recipe.name, width=400)
            self.lunch_label._index = i
            self.lunch_label._name = str(date) + "_midi"
            self.lunch_label._meal_type = "midi"
            self.lunch_label.pack(side="left", padx=10, pady=5)
            self.lunch_label.bind(
                "<Double-1>",
                lambda e, d=date, mt='Midi', value=lunch_recipe.name, field_name=self.lunch_label._name:
                self.on_double_click(e, d, mt, value, field_name)
            )

            self.dinner_label = ctk.CTkLabel(row_frame, text=dinner_recipe.name, width=400)
            self.dinner_label._index = i
            self.dinner_label._name = str(date) + "_soir"
            self.dinner_label._meal_type = "soir"
            self.dinner_label.pack(side="left", padx=10, pady=5)
            self.dinner_label.bind(
                "<Double-1>",
                lambda e, d=date, mt='Soir', value=dinner_recipe.name, field_name=self.dinner_label._name:
                    self.on_double_click(e, d, mt, value, field_name)
            )

    def on_double_click(self, event, date, meal_type, value, field_name):
        if self.is_changing_meal:
            utils.helpers.alert(f"Finissez la modification en cours")
            return

        self.is_changing_meal = True
        self.generate_menu_button.configure(state="disabled")
        self.save_menu_button.configure(state="disabled")

        recipes = sorted([recipe.name for recipe in RecipeController.get_all_recipes(meal_type=meal_type)])

        # Change background color of the clicked label
        self.field_name = field_name

        if utils.helpers.check_widget_type(event.widget) == tk.Label:
            event.widget.configure(fg="yellow")
        elif utils.helpers.check_widget_type(event.widget) == ctk.CTkCanvas:
            pass
            # ...

        self.recipe_label = ctk.CTkLabel(
            self.root,
            text=f"Modifier la recette du {utils.helpers.format_date_fr(date)} ({meal_type})"
        )
        self.recipe_label.pack(pady=15, side="left")

        self.recipe_name = ctk.CTkComboBox(self.root, values=recipes, state="readonly", width=350)
        self.recipe_name.pack(padx=15, pady=15, side="left")
        self.recipe_name.set(value)

        self.confirm_button = ctk.CTkButton(
            self.root,
            text="Modifier",
            command=self.edit_chosen_recipe
        )
        self.confirm_button.pack(pady=15, side="left")

    def edit_chosen_recipe(self):
        self.generate_menu_button.configure(state="normal")
        self.save_menu_button.configure(state="normal")

        new_recipe_name = self.recipe_name.get()
        new_recipe = next(recipe for recipe in RecipeController.get_all_recipes() if recipe.name == new_recipe_name)

        for i, (date, lunch_recipe, dinner_recipe) in enumerate(self.generated_menu):
            if self.field_name == str(date) + "_midi":
                self.generated_menu[i] = (date, new_recipe, dinner_recipe)
                break
            elif self.field_name == str(date) + "_soir":
                self.generated_menu[i] = (date, lunch_recipe, new_recipe)
                break

        self.is_changing_meal = False
        self.recipe_label.destroy()
        self.recipe_name.destroy()
        self.confirm_button.destroy()

        self.display_menu(self.generated_menu)
