from views.main_view import MainView
from views.add_ingredient_view import AddIngredientView
from views.add_recipe_view import AddRecipeView
from views.generate_menu_view import GenerateMenuView


class MainController:
    def __init__(self, root):
        self.root = root
        self.main_view = MainView(root, self)

    def add_ingredient(self):
        self.add_ingredient_view = AddIngredientView(self.root)
        self.add_ingredient_view.frame.tkraise()

    def add_recipe(self):
        self.add_recipe_view = AddRecipeView(self.root)
        self.add_recipe_view.frame.tkraise()

    def generate_menu(self):
        self.generate_menu_view = GenerateMenuView(self.root, self)
        self.generate_menu_view.frame.tkraise()
