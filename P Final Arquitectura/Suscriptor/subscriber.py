import pika
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ast

def send_email(reservation):
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

def callback(ch, method, properties, body):
    print(f"Received {body}")
    reservation = ast.literal_eval(body.decode())
    send_email(reservation)
    ch.stop_consuming()

def start_consuming():
    credentials = pika.PlainCredentials('admin', '12Didier')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
    channel = connection.channel()
    channel.queue_declare(queue='email_queue')
    channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)
    print('Esperando mensaje, para salir CTRL+C')
    channel.start_consuming()
    connection.close()

if __name__ == '__main__':
    start_consuming()
