import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'places.db')

def create_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Create table
    c.execute('''
    CREATE TABLE IF NOT EXISTS places (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL
    )
    ''')

    # Insert initial data
    c.execute('INSERT INTO places (name, description) VALUES (?, ?)', ('Gym', 'Gym equipped with weights and machines'))
    c.execute('INSERT INTO places (name, description) VALUES (?, ?)', ('Pool', 'Indoor pool with lanes for swimming'))
    c.execute('INSERT INTO places (name, description) VALUES (?, ?)', ('Conference Room', 'Room equipped for meetings'))
    c.execute('INSERT INTO places (name, description) VALUES (?, ?)', ('Basketball Court', 'Outdoor basketball court'))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        create_db()
    else:
        print(f"Database {DATABASE} already exists.")
