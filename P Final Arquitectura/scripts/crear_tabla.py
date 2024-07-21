import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__),'..', 'database', 'reservations.sql')

def remove_duplicates():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Obatin all colums from the table lugares
    c.execute('SELECT id, nombre, descripcion FROM lugares')
    rows = c.fetchall()

    #Create a dictionary to redact terms
    unique_lugares = {}
    
    ## Iterate over the rows and keep only the first occurrence of each name
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
