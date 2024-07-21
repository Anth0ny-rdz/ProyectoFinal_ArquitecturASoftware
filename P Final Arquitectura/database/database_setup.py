import sqlite3
import os

def deletetablecontents(db_path, table_name):
    try:
        # Connect to the database using the complete route
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

#Verify if the connection is correct
        print(f"Conectado a la base de datos en {db_path}")

#Verify if the table exists
        c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        table_exists = c.fetchone()

        if table_exists:
            # Delete all table content
            c.execute(f"DELETE FROM {table_name}")
            conn.commit()
            print(f"Todo el contenido de la tabla '{table_name}' ha sido eliminado.")

##Verify all the content after the table deleted
            c.execute(f"SELECT COUNT(*) FROM {table_name}")
            count_after = c.fetchone()[0]
            print(f'Número de registros después de eliminar: {count_after}')
        else:
            print(f"La tabla '{table_name}' no existe.")

    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e}")
    finally:
        conn.close()

##Build the rout to the folfer of the databse
DATABASE = os.path.join(os.path.dirname(__file__), 'reservations.sql')

##Call to the function to delete the content of 'reservations'
deletetablecontents(DATABASE, 'reservations')