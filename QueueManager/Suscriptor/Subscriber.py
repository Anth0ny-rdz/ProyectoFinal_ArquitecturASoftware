import pika
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ast

class Subscriber:
    def __init__(self, queue_name='email_queue'):
        self.queue_name = queue_name
        self.credentials = pika.PlainCredentials('admin', '12Didier')
        self.parameters = pika.ConnectionParameters('localhost', 5672, '/', self.credentials)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=False)

    def send_email(self, reservation):
        sender_email = "didierguerrero70@gmail.com"
        receiver_email = reservation['email']
        password = "arfg qgqp flsy sfqp"

        message = MIMEMultipart("alternative")
        message["Subject"] = "Reserva realizada con éxito"
        message["From"] = sender_email
        message["To"] = receiver_email

        text = f"""\
        Detalles de la Reserva:
        Nombre: {reservation['name']}
        Fecha: {reservation['date']}
        Hora: {reservation['time']}
        Tipo de Espacio: {reservation['type']}
        
        **Modificaciones a la reservas comunicarse con el servicio técnico.
        **Recuerde que si requiere cancelar la reserva se deberá realizar con 48 horas de anticipación, contactando con servicio técnico.
        """

        part = MIMEText(text, "plain")
        message.attach(part)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print(f"Mail enviado a {receiver_email}")

    def callback(self, ch, method, properties, body):
        print(f"Received {body}")
        reservation = ast.literal_eval(body.decode())
        self.send_email(reservation)
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Use basic_ack instead of stop_consuming

    def start_consuming(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)
        print('Esperando mensaje, para salir CTRL+C')
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
        finally:
            self.connection.close()

if __name__ == '__main__':
    Subscriber = Subscriber()
    Subscriber.start_consuming()
