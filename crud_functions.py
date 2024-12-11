import sqlite3


def initiate_db():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()

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
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON Users (email)")
    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Products WHERE id > ?', (0,))
    connection.commit()
    connection.close()
    return cursor.fetchall()

def add_user(username, email, age):
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                   (f'{username}', f'{email}', age, 1000))
    connection.commit()
    connection.close()
def is_included(username):
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    check_user = cursor.execute('SELECT * FROM Users WHERE username = ?', (username, ))
    is_inc = True
    if check_user.fetchone() is None:
        is_inc = False
    connection.commit()
    connection.close()
    return is_inc

initiate_db()
