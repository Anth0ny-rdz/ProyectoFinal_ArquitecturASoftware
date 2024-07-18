import sqlite3

def delete_all_records():
    # Conectarse a la base de datos reservations.sql
    conn = sqlite3.connect('reservations.sql')
    c = conn.cursor()

    # Eliminar todos los registros de la tabla reservations
    c.execute('DELETE FROM reservations')

    # Confirmar los cambios
    conn.commit()

    # Cerrar la conexión
    conn.close()

    print("Todos los registros han sido eliminados.")

if __name__ == "__main__":
    delete_all_records()
