import sqlite3
import bcrypt

DATABASE = 'users.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def create_table():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    db.commit()
    cursor.close()
    db.close()

def create_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    db = connect_db()
    cursor = db.cursor()
    
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        db.commit()
        print(f"User {username} created successfully.")
    except sqlite3.IntegrityError as e:
        print(f"Error creating user {username}: {e}")
    finally:
        cursor.close()
        db.close()

if __name__ == '__main__':
    create_table()
    
    users = [
        ('user1', 'pass1'),
        ('user2', 'pass2')
    ]
    
    for username, password in users:
        create_user(username, password)

    # Uncomment to add a user interactively
    # username = input("Enter username: ")
    # password = input("Enter password: ")
    # create_user(username, password)
