import sqlite3
import os

# Define the path to the database
DATABASE = os.path.join(os.path.dirname(__file__), '..', 'database', 'reservations.sql')


# Function to get the connection to the database
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    return conn

# Function to delete the 'places' table
def borrar_tabla_lugares():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS lugares')
    conn.commit()
    conn.close()
    print("Tabla 'lugares' eliminada con éxito.")

if __name__ == '_main_':
    borrar_tabla_lugares()