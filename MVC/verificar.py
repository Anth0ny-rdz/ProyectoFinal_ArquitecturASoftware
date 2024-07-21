import sqlite3
import os

# Define the database directory
DATABASE = os.path.join(os.path.dirname(__file__), 'database', 'reservations.sql')

def verificar_base_datos():
    if not os.path.exists(DATABASE):
        print(f"Database file {DATABASE} does not exist!")
        return False

    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        
        # Verify existence of reservations table
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reservations'")
        reservations_table = c.fetchone()
        
        if reservations_table:
            print("Tabla 'reservations' encontrada.")
        else:
            print("Tabla 'reservations' no encontrada.")
        
        # Verify existence of places table
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='lugares'")
        lugares_table = c.fetchone()
        
        if lugares_table:
            print("Tabla 'lugares' encontrada.")
        else:
            print("Tabla 'lugares' no encontrada.")
        
        conn.close()
        return True

    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
        return False

if __name__ == "__main__":
    if verificar_base_datos():
        print("La base de datos está configurada correctamente.")
    else:
        print("La base de datos no está configurada correctamente o no se pudo conectar.")
