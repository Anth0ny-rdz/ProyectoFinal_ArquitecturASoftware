import sqlite3
import os

# Define the path to the database
DATABASE = os.path.join(os.path.dirname(__file__), 'database', 'reservations.sql')

def verificar_reservas():
    # connect to database reservations.sql
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Look for all reservations
    c.execute('SELECT * FROM reservations')
    reservas = c.fetchall()

    # close conecction
    conn.close()

    return reservas

if __name__ == "__main__":
    reservas = verificar_reservas()
    if reservas:
        for reserva in reservas:
            print(f"ID: {reserva[0]}, Nombre: {reserva[1]}, Fecha: {reserva[3]}, Hora: {reserva[4]}, Tipo: {reserva[5]}")
    else:
        print("No hay reservas almacenadas.")
