# P Final Arquitectura/controller.py

from QueueManager.Publisher.Publisher import Publisher

class ControllerShurima:
    def __init__(self):
        self.Publisher = Publisher()

    def add_reservation(self, reservation):
        self.Publisher.add_reservation(reservation)

    def close_connection(self):
        self.Publisher.close_connection()


