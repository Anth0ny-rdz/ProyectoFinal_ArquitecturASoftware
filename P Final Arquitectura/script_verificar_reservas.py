import sqlite3

def verificar_reservas():
    # Conectarse a la base de datos reservations.sql
    conn = sqlite3.connect('reservations.sql')
    c = conn.cursor()

    # Consultar todas las reservas
    c.execute('SELECT * FROM reservations')
    reservas = c.fetchall()

    # Cerrar la conexión
    conn.close()

    return reservas

if __name__ == "__main__":
    reservas = verificar_reservas()
    if reservas:
        for reserva in reservas:
            print(f"ID: {reserva[0]}, Nombre: {reserva[1]}, Fecha: {reserva[2]}, Hora: {reserva[3]}, Tipo: {reserva[4]}")
    else:
        print("No hay reservas almacenadas.")
