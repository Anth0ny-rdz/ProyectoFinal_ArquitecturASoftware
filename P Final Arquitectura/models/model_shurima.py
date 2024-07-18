import sqlite3

class ModelShurima:
    def __init__(self):
        self.conn = sqlite3.connect('reservations.sql')
        self.c = self.conn.cursor()

    def add_reservation(self, name, date, time, type, email):
        self.c.execute('''
            INSERT INTO reservations (name, date, time, type, email) VALUES (?, ?, ?, ?, ?)
        ''', (name, date, time, type, email))
        self.conn.commit()

    def get_reservations(self):
        self.c.execute('SELECT name, date, time, type, email FROM reservations')
        return self.c.fetchall()

    def __del__(self):
        self.conn.close()
