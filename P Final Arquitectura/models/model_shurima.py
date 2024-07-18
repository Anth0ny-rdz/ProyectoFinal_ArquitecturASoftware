import sqlite3
import os

class ModelShurima:
    def __init__(self):
        # Definir el directorio de la base de datos
        self.database_path = os.path.join(os.path.dirname(__file__), 'database', 'reservations.sql')
        self.conn = sqlite3.connect(self.database_path)
        self.c = self.conn.cursor()

    def add_reservation(self, name, email, date, time, type):
        self.c.execute('''
            INSERT INTO reservations (name, email, date, time, type) VALUES (?, ?, ?, ?, ?)
        ''', (name, email, date, time, type))
        self.conn.commit()

    def get_reservations(self):
        self.c.execute('SELECT name, email, date, time, type FROM reservations')
        return self.c.fetchall()

    def __del__(self):
        self.conn.close()
