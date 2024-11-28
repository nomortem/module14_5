import sqlite3


def initiate_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL DEFAULT 1000
    )
    ''')

    connection.commit()
    connection.close()


def add_user(username, email, age):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('''
    INSERT INTO Users (username, email, age) VALUES (?, ?, ?)
    ''', (username, email, age))

    connection.commit()
    connection.close()


def is_included(username):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT username FROM Users WHERE username = ?', (username,))
    user = cursor.fetchone()

    connection.close()
    return user is not None

initiate_db()

