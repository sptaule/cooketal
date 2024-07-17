import sqlite3


def get_connection():
    return sqlite3.connect('cooketal.db')


def export_ingredients():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT name FROM ingredients ORDER BY name ASC")
    ingredients = [row[0] for row in c.fetchall()]
    with open('assets/data/ingredients.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(ingredients))
    conn.close()
    print("Les ingrédients ont été exportés dans le fichier 'ingredients.txt'.")


def insert_ingredients(ingredients):
    conn = get_connection()
    c = conn.cursor()
    c.executemany("INSERT INTO ingredients (ingredient) VALUES (?)", [(i,) for i in ingredients])
    conn.commit()
    conn.close()
    return len(ingredients)


def create_tables():
    create_script = '''
        CREATE TABLE IF NOT EXISTS ingredients_units (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
    
        INSERT INTO ingredients_units (name)
        SELECT * FROM (
            VALUES ('U'), ('g'), ('c.a.c'), ('c.a.s')
        ) AS tmp
        WHERE (SELECT COUNT(*) FROM ingredients_units) = 0;
        
        CREATE TABLE IF NOT EXISTS ingredients_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            bg_color TEXT NOT NULL,
            text_color TEXT NOT NULL
        );

        INSERT INTO ingredients_categories (name, bg_color, text_color)
        SELECT * FROM (
            VALUES
                ('Bio', '7D3C98', 'FFFFFF'),
                ('Huiles et condiments', 'F1C40F', 'FFFFFF'),
                ('Conserves', '2980B9', 'FFFFFF'),
                ('Produits du monde', '8E44AD', 'FFFFFF'),
                ('Pâtes riz et sauces', 'E74C3C', 'FFFFFF'),
                ('Farines et levures', '16A085', 'FFFFFF'),
                ('Alcools', '27AE60', 'FFFFFF'),
                ('Boulangerie', '2C3E50', 'FFFFFF'),
                ('Fruits et légumes', 'F39C12', 'FFFFFF'),
                ('Fromages et similis', 'D35400', 'FFFFFF'),
                ('Surgelés et laits', 'C0392B', 'FFFFFF')
        ) AS tmp
        WHERE (SELECT COUNT(*) FROM ingredients_categories) = 0;
        
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            category_id INTEGER,
            FOREIGN KEY(category_id) REFERENCES ingredients_categories(id)
        );

        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            meal_type TEXT NOT NULL,
            meal_count INTEGER NOT NULL,
            instructions TEXT DEFAULT NULL
        );

        CREATE TABLE IF NOT EXISTS recipe_ingredients (
            recipe_id INTEGER,
            ingredient_id INTEGER,
            quantity REAL NOT NULL,
            unit TEXT NOT NULL,
            FOREIGN KEY(recipe_id) REFERENCES recipes(id),
            FOREIGN KEY(ingredient_id) REFERENCES ingredients(id)
        );
        
        CREATE TABLE IF NOT EXISTS menus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS menu_recipes (
            menu_id INTEGER,
            recipe_id INTEGER,
            meal_date DATE NOT NULL,
            meal_time TEXT NOT NULL,
            FOREIGN KEY(menu_id) REFERENCES menus(id),
            FOREIGN KEY(recipe_id) REFERENCES recipes(id)
        );
    '''

    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript(create_script)
    conn.commit()
    conn.close()
