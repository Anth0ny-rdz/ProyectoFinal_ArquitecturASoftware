import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__),'..', 'database', 'reservations.sql')

def remove_duplicates():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Obtener todas las filas de la tabla lugares
    c.execute('SELECT id, nombre, descripcion FROM lugares')
    rows = c.fetchall()

    # Crear un diccionario para almacenar los nombres únicos
    unique_lugares = {}
    
    # Iterar sobre las filas y mantener solo la primera aparición de cada nombre
    for row in rows:
        id, nombre, descripcion = row
        if nombre not in unique_lugares:
            unique_lugares[nombre] = (id, descripcion)
        else:
            # delete doubles
            c.execute('DELETE FROM lugares WHERE id = ?', (id,))

    conn.commit()
    conn.close()

def add_cosas():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    
    
    c.execute('INSERT INTO lugares (nombre, descripcion) VALUES (?, ?)', ('Cancha de basket', 'Cancha amplia con todas las comodidades para los usuarios'))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
  
    add_cosas()
    print("Duplicados eliminados y 'Area de cometas' añadido.")
