import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), '..', 'database', 'reservations.db')

def verify_db():
    if not os.path.exists(DATABASE):
        print("Database file does not exist.")
        return
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reservations';")
    table_exists = c.fetchone()
    conn.close()

    if table_exists:
        print("Table 'reservations' exists.")
    else:
        print("Table 'reservations' does not exist.")

if __name__ == '__main__':
    verify_db()
