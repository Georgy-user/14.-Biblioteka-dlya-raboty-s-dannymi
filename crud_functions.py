import sqlite3

connection = sqlite3.connect("products_data.db")
cursor = connection.cursor()


def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')


connection.commit()

initiate_db()

cursor.execute("DELETE FROM Products")

product_description = ['Астра', 'Амариллис', 'Анемон', 'Алоэ-траски']
for number in range(0, 4):
    cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                   (f'Product{number + 1}', f'Продукт на основе цветка {product_description[number]}',
                    (number + 1) * 100)
                   )
connection.commit()


def get_all_products():
    cursor.execute("SELECT * FROM Products")
    return cursor.fetchall()
