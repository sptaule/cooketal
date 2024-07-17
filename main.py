import customtkinter as ctk
import utils.helpers as utils
import database.db_manager as DB
from controllers.main_controller import MainController
from views.add_ingredient_view import AddIngredientView
from views.list_ingredient_view import ListIngredientView
from views.add_recipe_view import AddRecipeView
from views.list_recipe_view import ListRecipeView
from views.import_option_view import ImportOptionView
from views.export_option_view import ExportOptionView
from views.generate_menu_view import GenerateMenuView
from views.history_menu_view import HistoryMenuView

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry(utils.center_geometry(width=1280, height=900))
app.iconbitmap(utils.get_icon('icon', 'ico', True))
app.title("Cooketal")

MAIN_MENU_FONT = ctk.CTkFont(size=16)
SECONDARY_MENU_FONT = ctk.CTkFont(size=14)
LABEL_FONT = ctk.CTkFont(size=12)


def main():
    DB.create_tables()
    controller = MainController(app)

    main_menu = _main_menu(controller)
    menus_menu = _menus_menu(controller, main_menu)
    recipes_menu = _recipes_menu(controller, main_menu)
    ingredients_menu = _ingredients_menu(controller, main_menu)
    options_menu = _options_menu(controller, main_menu)

    app.mainloop()


def _main_menu(controller):
    main_menu = ctk.CTkTabview(master=app)
    main_menu.pack(fill="both", expand=True, padx=20, pady=10)
    main_menu._segmented_button.configure(font=MAIN_MENU_FONT, width=250)
    main_menu.add("Menus")
    main_menu.add("Recettes")
    main_menu.add("Ingrédients")
    main_menu.add("Options")
    return main_menu


def _menus_menu(controller, parent):
    menus_menu = ctk.CTkTabview(master=parent.tab("Menus"))
    menus_menu.pack(fill="both", expand=True, padx=20)
    menus_menu._segmented_button.configure(font=SECONDARY_MENU_FONT)
    generate_menu_tab = menus_menu.add("Générer un menu")
    ctk.CTkLabel(generate_menu_tab, text="Générer un menu pour une période donnée", font=LABEL_FONT).pack()
    history_menu_tab = menus_menu.add("Historique des menus")
    ctk.CTkLabel(history_menu_tab, text="Rechercher dans l'historique des menus", font=LABEL_FONT).pack()
    generate_menu_view = GenerateMenuView(generate_menu_tab)
    history_menu_view = HistoryMenuView(history_menu_tab)
    return menus_menu


def _recipes_menu(controller, parent):
    recipes_menu = ctk.CTkTabview(master=parent.tab("Recettes"))
    recipes_menu.pack(fill="both", expand=True, padx=20)
    recipes_menu._segmented_button.configure(font=SECONDARY_MENU_FONT)
    list_tab = recipes_menu.add("Liste des recettes")
    add_tab = recipes_menu.add("Ajouter une recette")
    ctk.CTkLabel(list_tab, text="Consulter la liste de toutes les recettes", font=LABEL_FONT).pack()
    ctk.CTkLabel(add_tab, text="Permet d'ajouter une recette à la liste", font=LABEL_FONT).pack()
    add_recipe_view = AddRecipeView(add_tab)
    list_recipe_view = ListRecipeView(list_tab)
    return recipes_menu


def _ingredients_menu(controller, parent):
    ingredients_menu = ctk.CTkTabview(master=parent.tab("Ingrédients"))
    ingredients_menu.pack(fill="both", expand=True, padx=20)
    ingredients_menu._segmented_button.configure(font=SECONDARY_MENU_FONT)
    list_tab = ingredients_menu.add("Liste des ingrédients")
    add_tab = ingredients_menu.add("Ajouter un ingrédient")
    ctk.CTkLabel(list_tab, text="Consulter la liste de tous les ingrédients", font=LABEL_FONT).pack()
    ctk.CTkLabel(add_tab, text="Ajouter un ingrédient à la liste", font=LABEL_FONT).pack()
    add_ingredient_view = AddIngredientView(add_tab)
    list_ingredient_view = ListIngredientView(list_tab)
    return ingredients_menu


def _options_menu(controller, parent):
    options_menu = ctk.CTkTabview(master=parent.tab("Options"))
    options_menu.pack(fill="both", expand=True, padx=20)
    options_menu._segmented_button.configure(font=SECONDARY_MENU_FONT)
    export_tab = options_menu.add("Exporter")
    import_tab = options_menu.add("Importer")
    ctk.CTkLabel(export_tab, text="Exporter des données", font=LABEL_FONT).pack()
    ctk.CTkLabel(import_tab, text="Importer des données", font=LABEL_FONT).pack()
    export_option_view = ExportOptionView(export_tab)
    import_option_view = ImportOptionView(import_tab)
    return options_menu


if __name__ == "__main__":
    main()
