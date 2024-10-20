import sqlite3


connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON Users (email)")
# for i in range(10):
#     cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)",
#                    (f"User{i+1}", f'example{i+1}@gmail.com', 10 * (i+1), 1000))

# for i in range(1, 11, 2):
#     cursor.execute("UPDATE Users SET balance=? WHERE id=?", (500, i))

# for i in range(1, 11, 3):
#     cursor.execute("DELETE FROM Users WHERE id=?", (i,))

cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != ?", (60,))
select_users = cursor.fetchall()
# for user in select_users:
#     print(f'Имя: {user[0]} | Почта: {user[1]} |Возраст: {user[2]} |Баланс: {user[3]}')

connection.commit()
connection.close()