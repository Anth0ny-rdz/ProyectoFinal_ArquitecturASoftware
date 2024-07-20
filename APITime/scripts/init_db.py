import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'scripts', 'database', 'availability.sql')

def create_db():
    if not os.path.exists(os.path.dirname(DATABASE)):
        os.makedirs(os.path.dirname(DATABASE))

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Crear la tabla availability
    c.execute('''
        CREATE TABLE IF NOT EXISTS availability (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            type TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
    print(f"Database created at {DATABASE}")
