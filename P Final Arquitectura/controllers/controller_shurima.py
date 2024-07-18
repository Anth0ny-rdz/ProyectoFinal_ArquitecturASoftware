import pika
from Suscriptor.subscriber import start_consuming



class ControllerShurima:
    def __init__(self):
        # Conexión a RabbitMQ
        self.credentials = pika.PlainCredentials('admin', '12Didier')
        self.parameters = pika.ConnectionParameters('localhost', 5672, '/', self.credentials)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='email_queue')

    def add_reservation(self, reservation):
        # Publicar mensaje en RabbitMQ
        self.channel.basic_publish(
            exchange='',
            routing_key='email_queue',
            body=str(reservation)
        )
        print(f" [x] Sent reservation: {reservation}")
        start_consuming()

    def close_connection(self):
        self.connection.close()
