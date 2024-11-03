import sqlite3

connection = sqlite3.connect("products_users_data.db")
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
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    )
    ''')
    connection.commit()


initiate_db()

cursor.execute("DELETE FROM Products")
cursor.execute("DELETE FROM Users")

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


def add_user(username, email, age):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, 1000)",
                   (username, email, age)
                   )
    connection.commit()


def is_included(username):
    check_username = False
    cursor.execute("SELECT * FROM Users")
    select_user = cursor.fetchall()
    for user in select_user:
        if user[1] == username:
            check_username = True
    connection.commit()
    return check_username


def is_all_db():
    print()
    cursor.execute("SELECT * FROM Users")
    select_user = cursor.fetchall()
    for user in select_user:
        print(f'Имя: {user[1]} | Почта: {user[2]} |Возраст: {user[3]} |Баланс: {user[4]}')
    print()
    connection.commit()


connection.commit()

# connection.close()
