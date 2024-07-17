# Cooketal

This desktop application for Windows, written in Python, lets you manage your ingredients and recipes, generate a menu for a given period and then generate a list of ingredients to buy according to the menu.  
In short, it helps you make your shopping list.

<img src="https://res.cloudinary.com/dvie2gv2x/image/upload/v1721207836/Cooketal/history_view_menu_qa1fks.png" width="30%"></img>
<img src="https://res.cloudinary.com/dvie2gv2x/image/upload/v1721207835/Cooketal/history_view_ingredients_a0zyki.png" width="30%"></img>
<img src="https://res.cloudinary.com/dvie2gv2x/image/upload/v1721207840/Cooketal/menus_list_zzgmzy.png" width="30%"></img>
<img src="https://res.cloudinary.com/dvie2gv2x/image/upload/v1721207839/Cooketal/menus_generate_tineld.png" width="30%"></img>
<img src="https://res.cloudinary.com/dvie2gv2x/image/upload/v1721207846/Cooketal/recipes_list_n27aqy.png" width="30%"></img>
<img src="https://res.cloudinary.com/dvie2gv2x/image/upload/v1721207845/Cooketal/recipes_edit_czxlsa.png" width="30%"></img>
<img src="https://res.cloudinary.com/dvie2gv2x/image/upload/v1721207844/Cooketal/recipes_add_e4lapi.png" width="30%"></img>
<img src="https://res.cloudinary.com/dvie2gv2x/image/upload/v1721207838/Cooketal/ingredients_list_zzjiwg.png" width="30%"></img>
<img src="https://res.cloudinary.com/dvie2gv2x/image/upload/v1721207836/Cooketal/ingredients_add_iassij.png" width="30%"></img>

## General features

- **Menu generation**: Generate a menu for a given period using random recipes from the database.
- **Recipe management**: Add, consult, modify and delete recipes.
- **Ingredients management**: Add, consult, modify and delete ingredients.
- **Menu history**: Consult previously generated menus and view associated recipes and ingredients.
- **Import/export options**: Export and import ingredients to share with other users.

## Tabs and feature details

1. **Menus** :
    - **Generate menu**: Generates a menu for a given period. Recipes are randomly selected from those already saved. Dishes can be modified by double-clicking on their name. Save the menu for retrieval in the menu history.
    - **Menu history**: View all generated menus. View recipes and ingredients required for each menu.

2. **Recipes** :
    - **Recipe list**: View all recipes saved. Filter recipes using a full-text search field. Modify or delete recipes.
    - **Add a recipe**: Add a new recipe with name, meal type, number of meals, instructions (optional) and ingredients. Ingredients can be added via a full-text search and selected from a drop-down list.

3. **Ingredients** :
    - **Ingredient list**: View all registered ingredients. Filter ingredients using a full-text search field. Modify or delete ingredients.
    - **Add a new ingredient** : Add a new ingredient with its name and category.

4. **Options** :
    - **Export**: Export the ingredient list to a text file.
    - **Import** : Import ingredients from a text file. Duplicates will not be imported. (Note: avoid using accents in the list of ingredients to be imported).

## Technologies and modules used

- Python
- Tkinter
- Tkcalendar
- Customtkinter
- CTkMessagebox
- SQLite3
- Pillow

## Download

Available at [lucaschaplain.design/creations](https://www.lucaschaplain.design/creations)

## Build

1. Close repository
2. Install requirements in a virtual environment
3. Run `pyinstaller ./cooketal.spec` (to generate the .exe) or run `python ./main.py` (to launch the application).

If the database is not present, it will be created on the first launch.

## Upcoming improvements

- Import ingredients with accented characters.
- Add, modify and delete ingredient categories and change their display order.
- Option not to insert a recipe for a specified day or time when generating a menu.
- Link recipes to seasons (summer, winter, etc.).
- Import and export recipes, menus and other necessary entities.

## Side note

This is my first Python GUI app, made in about a week, so you can find mistakes.  
Also, this was meant to be a personal app only but as a matter of fact I thought this could be useful to somebody else.

## Contribute

Contributions are welcome!  
Please submit a pull request or open an issue to discuss the changes you would like to make.

## License

This project is licensed under the MIT license. [See license](LICENSE) for more details.
