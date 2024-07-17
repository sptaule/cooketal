import customtkinter as ctk
import controllers.ingredient_controller as IngredientController
import utils.helpers


class ListIngredientView:
    def __init__(self, root):
        self.root = root
        self.controller = IngredientController

        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack()

        self.filter_entry = ctk.CTkEntry(self.frame, placeholder_text="Rechercher...")
        self.filter_entry.pack()
        self.filter_entry.bind("<KeyRelease>", self.filter_listbox)

        self.listbox = utils.helpers.data_list(self.frame)
        self.listbox.pack(pady=10)
        self.listbox.bind('<Double-Button>', self.modify_ingredient)

        self.populate_listbox()

        # Boutons en bas de la listbox
        self.modify_button = ctk.CTkButton(
            self.frame, text="Modifier", state="disabled", command=self.modify_ingredient)
        self.modify_button.pack(side="left", expand=True)

        self.delete_button = ctk.CTkButton(
            self.frame, text="Supprimer", state="disabled", command=self.delete_ingredient)
        self.delete_button.pack(side="left", expand=True)

        self.refresh_button = ctk.CTkButton(
            self.frame,
            text="",
            width=30,
            command=self.populate_listbox,
            image=utils.helpers.get_icon("refresh"),
            fg_color="#E2C044",
            hover_color="#C29F1E",
        )
        self.refresh_button.pack(side="left", expand=True)

        # Lier la sélection de la listbox aux boutons
        self.listbox.bind("<<ListboxSelect>>", self.update_buttons)

        # Sélectionner le premier élément de la listbox
        if self.listbox.size() > 0:
            self.listbox.selection_set(0)
            self.update_buttons(None)

    def populate_listbox(self):
        self.listbox.delete(0, ctk.END)
        self.ids = []
        self.all_ingredients = self.controller.get_all_ingredients()
        for idx, ingredient in enumerate(self.all_ingredients):
            self.ids.append(ingredient._id)
            self.listbox.insert(idx, ingredient.name)

    def filter_listbox(self, event):
        filter_text = self.filter_entry.get().lower()
        self.listbox.delete(0, "end")
        self.ids = []
        for idx, ingredient in enumerate(self.all_ingredients):
            if filter_text in ingredient.name.lower():
                self.ids.append(ingredient._id)
                self.listbox.insert(idx, ingredient.name)

    def update_buttons(self, event):
        if self.listbox.curselection() or self.listbox.curselection() == 0:
            self.modify_button.configure(state="normal")
            self.delete_button.configure(state="normal")
        else:
            self.modify_button.configure(state="disabled")
            self.delete_button.configure(state="disabled")

    def modify_ingredient(self, event=None):
        selected_index = self.listbox.curselection()[0]

        if selected_index is None:
            return

        _id = self.ids[selected_index]
        if selected_index >= 0:
            ingredient = self.controller.get_by_id(_id)

            # Création popup
            self.popup = ctk.CTkToplevel(self.root, width=400, height=250)
            self.popup.resizable(False, False)
            self.popup.title("Modifier l'ingrédient")

            # Calcul pour centrer la popup
            self.popup.geometry(utils.helpers.center_geometry(300, 200))

            # Champ d'entrée pour la modification
            self.name_label = ctk.CTkLabel(self.popup, text="Nom")
            self.name_label.pack()
            self.entry = ctk.CTkEntry(self.popup, width=250)
            self.entry.pack(padx=20, pady=10, expand=True)
            self.entry.insert(0, ingredient.name)

            categories = IngredientController.get_all_categories()
            ingredient_category_name = IngredientController.get_category_name_by_id(_id)
            self.category_label = ctk.CTkLabel(self.popup, text="Catégorie")
            self.category_label.pack()
            self.category = ctk.CTkComboBox(self.popup, state="readonly", width=250)
            self.category.pack(pady=10)
            self.category.configure(values=categories)
            if ingredient_category_name is not None and ingredient_category_name in categories:
                self.category.set(ingredient_category_name)

            # Bouton de validation
            self.validate_button = ctk.CTkButton(
                self.popup, text="Valider", command=lambda: self.update_ingredient(selected_index, _id)
            )
            self.validate_button.pack(pady=10)

            self.popup.deiconify()
            self.popup.grab_set()

    def update_ingredient(self, index, _id):
        new_name = self.entry.get()
        new_category = IngredientController.get_category_id_by_category_name(self.category.get())
        if not self.controller.update_ingredient(_id, new_name, new_category):
            return

        self.filter_entry.delete(0, ctk.END)
        self.popup.destroy()
        self.populate_listbox()
        listbox_size = self.listbox.size()

        if listbox_size > 0:
            if index + 1 < listbox_size:
                self.listbox.selection_set(index + 1)
                self.listbox.see(index + 1)
            else:
                self.listbox.selection_set(index)
                self.listbox.see(index)
            self.update_buttons(None)

    def delete_ingredient(self):
        selected_index = self.listbox.curselection()[0]
        if selected_index is None:
            return

        selected_ingredient_name = self.listbox.get(selected_index)
        _id = self.ids[selected_index]
        ingredient = self.controller.get_by_id(_id)
        if not ingredient:
            return

        answer = utils.helpers.confirm_deletion_popup(f"Supprimer l'ingrédient {selected_ingredient_name} ?")
        if answer.get() != "Oui":
            return

        if not ingredient.delete():
            return

        self.populate_listbox()
        if self.listbox.size() > 0:
            next_index = selected_index if self.listbox.size() > selected_index else selected_index - 1
            self.listbox.selection_set(next_index)
            self.update_buttons(None)
