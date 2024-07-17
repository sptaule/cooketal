import customtkinter as ctk
import controllers.recipe_controller as RecipeController
from views.modify_recipe_view import ModifyRecipeView
import utils.helpers


class ListRecipeView:
    def __init__(self, root):
        self.root = root
        self.controller = RecipeController

        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack()

        self.filter_entry = ctk.CTkEntry(self.frame, placeholder_text="Rechercher...")
        self.filter_entry.pack()
        self.filter_entry.bind("<KeyRelease>", self.filter_listbox)

        self.listbox = utils.helpers.data_list(self.frame)
        self.listbox.pack(pady=10)
        self.listbox.bind('<Double-Button>', self.modify_recipe)

        self.total_recipes_lunch = len(self.controller.get_all_recipes(meal_type='Midi'))
        self.total_recipes_dinner = len(self.controller.get_all_recipes(meal_type='Soir'))
        self.total_recipes_label = ctk.CTkLabel(
            self.frame,
            text=f"{self.total_recipes_lunch + self.total_recipes_dinner} recette(s) ajoutée(s) "
                 f"- {self.total_recipes_lunch} midi - {self.total_recipes_dinner} soir"
        )
        self.total_recipes_label.pack(pady=10)

        self.populate_listbox()

        self.modify_button = ctk.CTkButton(
            self.frame, text="Modifier", state="disabled", command=self.modify_recipe)
        self.modify_button.pack(side="left", expand=True)

        self.delete_button = ctk.CTkButton(
            self.frame, text="Supprimer", state="disabled", command=self.delete_recipe)
        self.delete_button.pack(side="left", expand=True)

        self.refresh_button = ctk.CTkButton(
            self.frame,
            text="",
            width=30,
            command=self.populate_listbox,
            image=utils.helpers.get_icon("refresh"),
            fg_color="#E2C044",
            hover_color="#C29F1E"
        )
        self.refresh_button.pack(side="left", expand=True)

        self.listbox.bind("<<ListboxSelect>>", self.update_buttons)

    def update_total_label(self):
        self.total_recipes_lunch = len(self.controller.get_all_recipes(meal_type='Midi'))
        self.total_recipes_dinner = len(self.controller.get_all_recipes(meal_type='Soir'))
        self.total_recipes_label.configure(
            text=f"{self.total_recipes_lunch + self.total_recipes_dinner} recette(s) ajoutée(s) "
                 f"- {self.total_recipes_lunch} midi - {self.total_recipes_dinner} soir"
        )

    def hide_frame(self):
        self.frame.pack_forget()

    def show_frame(self):
        self.frame.pack()

    def populate_listbox(self):
        self.listbox.delete(0, ctk.END)
        self.ids = []
        self.all_recipes = self.controller.get_all_recipes()
        for idx, recipe in enumerate(self.all_recipes):
            self.ids.append(recipe._id)
            self.listbox.insert(idx, recipe.name)
        self.update_total_label()

    def filter_listbox(self, event):
        filter_text = self.filter_entry.get().lower()
        self.listbox.delete(0, "end")
        self.ids = []
        for idx, recipe in enumerate(self.all_recipes):
            if filter_text in recipe.name.lower():
                self.ids.append(recipe._id)
                self.listbox.insert(idx, recipe.name)

    def update_buttons(self, event):
        if self.listbox.curselection() is not None:
            self.modify_button.configure(state="normal")
            self.delete_button.configure(state="normal")
        else:
            self.modify_button.configure(state="disabled")
            self.delete_button.configure(state="disabled")

    def modify_recipe(self, event=None):
        selected_index = self.listbox.curselection()[0]
        if selected_index is None:
            return

        _id = self.ids[selected_index]
        self.hide_frame()
        ModifyRecipeView(self.root, _id, self.show_frame)

    def delete_recipe(self):
        selected_index = self.listbox.curselection()[0]
        if selected_index is None:
            return

        selected_recipe_name = self.listbox.get(selected_index)
        _id = self.ids[selected_index]
        recipe = self.controller.get_by_id(_id)
        if not recipe:
            return

        answer = utils.helpers.confirm_deletion_popup(f"Supprimer la recette {selected_recipe_name} ?")
        if answer.get() != "Oui":
            return

        if not recipe.delete():
            return

        self.populate_listbox()
        if self.listbox.size() > 0:
            next_index = selected_index if self.listbox.size() > selected_index else selected_index - 1
            self.listbox.selection_set(next_index)
            self.update_buttons(None)
