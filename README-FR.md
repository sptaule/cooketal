# Cooketal

Cette application desktop pour Windows, réalisée en Python, permet de gérer ses ingrédients, ses recettes, générer un menu pour une période donnée puis générer la liste d'ingrédients à acheter en fonction du menu.  
En résumé, cela aide à faire sa liste de courses.

<img src="https://res.cloudinary.com/dvie2gv2x/image/upload/v1721207836/Cooketal/history_view_menu_qa1fks.png" width="30%"></img>
<img src="https://res.cloudinary.com/dvie2gv2x/image/upload/v1721207835/Cooketal/history_view_ingredients_a0zyki.png" width="30%"></img>
<img src="https://res.cloudinary.com/dvie2gv2x/image/upload/v1721207840/Cooketal/menus_list_zzgmzy.png" width="30%"></img>
<img src="https://res.cloudinary.com/dvie2gv2x/image/upload/v1721207839/Cooketal/menus_generate_tineld.png" width="30%"></img>
<img src="https://res.cloudinary.com/dvie2gv2x/image/upload/v1721207846/Cooketal/recipes_list_n27aqy.png" width="30%"></img>
<img src="https://res.cloudinary.com/dvie2gv2x/image/upload/v1721207845/Cooketal/recipes_edit_czxlsa.png" width="30%"></img>
<img src="https://res.cloudinary.com/dvie2gv2x/image/upload/v1721207844/Cooketal/recipes_add_e4lapi.png" width="30%"></img>
<img src="https://res.cloudinary.com/dvie2gv2x/image/upload/v1721207838/Cooketal/ingredients_list_zzjiwg.png" width="30%"></img>
<img src="https://res.cloudinary.com/dvie2gv2x/image/upload/v1721207836/Cooketal/ingredients_add_iassij.png" width="30%"></img>

## Fonctionnalités générales

- **Génération de menus** : Générer un menu pour une période donnée avec des recettes aléatoires parmi celles enregistrées en base de données.
- **Gestion des recettes** : Ajouter, consulter, modifier et supprimer des recettes.
- **Gestion des ingrédients** : Ajouter, consulter, modifier et supprimer des ingrédients.
- **Historique des menus** : Consulter les menus générés précédemment et voir les recettes et ingrédients associés.
- **Options d'import/export** : Exporter et importer des ingrédients pour les partager avec d'autres utilisateurs.

## Onglets et détails des fonctionnalités

1. **Menus** :
    - **Générer un menu** : Permet de générer un menu pour une période donnée. Les recettes sont choisies de manière aléatoire parmi celles enregistrées. Possibilité de modifier les plats en double-cliquant sur leur nom. Sauvegarder le menu pour le retrouver dans l'historique.
    - **Historique des menus** : Voir tous les menus générés. Consulter les recettes et les ingrédients nécessaires pour chaque menu.

2. **Recettes** :
    - **Liste des recettes** : Consulter toutes les recettes enregistrées. Filtrer les recettes grâce à un champ de recherche full-text. Modifier ou supprimer des recettes.
    - **Ajouter une recette** : Ajouter une nouvelle recette avec un nom, type de repas, nombre de repas, instructions (optionnel) et ingrédients. Les ingrédients peuvent être ajoutés via une recherche full-text et sélectionnés dans une liste déroulante.

3. **Ingrédients** :
    - **Liste des ingrédients** : Consulter tous les ingrédients enregistrés. Filtrer les ingrédients grâce à un champ de recherche full-text. Modifier ou supprimer des ingrédients.
    - **Ajouter un ingrédient** : Ajouter un nouvel ingrédient avec son nom et sa catégorie.

4. **Options** :
    - **Exporter** : Exporter la liste des ingrédients dans un fichier texte.
    - **Importer** : Importer des ingrédients depuis un fichier texte. Les doublons ne seront pas importés. (Note : évitez les accents dans la liste des ingrédients à importer).

## Technologies et modules utilisés

- Python
- Tkinter
- Tkcalendar
- Customtkinter
- CTkMessagebox
- SQLite3
- Pillow

## Télécharger

Disponible sur [lucaschaplain.design/creations](https://www.lucaschaplain.design/creations)

## Build

1. Clôner le dépôt
2. Installer les requirements dans un environnement virtuel
3. Exécuter `pyinstaller ./cooketal.spec` (pour générer le .exe) ou exécuter `python ./main.py` (pour lancer l'application)

Si la base de données n'est pas présente, elle sera alors créée lors du premier lancement.

## Améliorations à venir

- Importer des ingrédients avec des caractères accentués.
- Ajouter, modifier et supprimer des catégories d'ingrédients et changer leur ordre d'affichage.
- Possibilité de ne pas insérer de recette pour un jour ou moment spécifié lors de la génération d'un menu.
- Relier les recettes à des saisons (été, hiver, etc.).
- Importer et exporter des recettes, des menus et autres entités nécessaires.

## Contribuer

Les contributions sont les bienvenues !  
Veuillez soumettre une pull request ou ouvrir une issue pour discuter des changements que vous souhaitez apporter.

## License

Ce projet est sous licence MIT. [Voir la license](LICENSE) pour plus de détails.
