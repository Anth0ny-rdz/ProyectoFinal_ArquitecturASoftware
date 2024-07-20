import pika
import threading
from QueueManager.Suscriptor.Subscriber import Subscriber

class Publisher:
    def __init__(self, queue_name='email_queue'):
        # Conexión a RabbitMQ
        self.credentials = pika.PlainCredentials('admin', '12Didier')
        self.parameters = pika.ConnectionParameters('localhost', 5672, '/', self.credentials)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.queue_name = queue_name
        self.channel.queue_declare(queue=queue_name, durable=False)

    def add_reservation(self, reservation):
        # Publicar mensaje en RabbitMQ
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=str(reservation),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        print(f" [x] Sent reservation: {reservation}")
        self.start_single_consuming()

    def start_single_consuming(self):
        # Consumir en un solo hilo de procesamiento
        subscriber = Subscriber(queue_name=self.queue_name)
        consume_thread = threading.Thread(target=subscriber.start_consuming)
        consume_thread.start()

    def close_connection(self):
        self.connection.close()
