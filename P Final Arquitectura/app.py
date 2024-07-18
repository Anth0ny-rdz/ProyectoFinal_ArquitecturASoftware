import sqlite3
from flask import Flask, request, redirect, url_for, render_template
from controllers.controller_shurima import ControllerShurima
import urllib.parse  # Importa urllib.parse para la decodificación manual si es necesario

app = Flask(__name__)
controller = ControllerShurima()

# Ruta para la página principal
@app.route('/')
def index():
    conn = sqlite3.connect('reservations.sql')
    c = conn.cursor()
    c.execute('SELECT * FROM reservations')
    reservations = c.fetchall()
    conn.close()
    return render_template('index.html', reservations=reservations)

# Ruta para manejar la reserva
@app.route('/reserve', methods=['POST'])
def reserve():
    try:
        # Imprimir el formulario recibido
        print(f"Received POST request to /reserve with data: {request.form}")

        # Verificar la presencia de cada campo en el formulario
        if 'name' in request.form and 'date' in request.form and 'time' in request.form and 'type' in request.form and 'email' in request.form:
            name = request.form['name']
            date = request.form['date']
            time = request.form['time']
            type = request.form['type']
            email = request.form['email']

            # Decodificar manualmente el email si es necesario
            email_decoded = urllib.parse.unquote(email)

            # Imprimir todos los valores recibidos
            print(f"Recibido: Nombre: {name}, Fecha: {date}, Hora: {time}, Tipo: {type}, Email: {email}, Email Decoded: {email_decoded}")

            conn = sqlite3.connect('reservations.sql')
            c = conn.cursor()
            c.execute('INSERT INTO reservations (name, date, time, type, email) VALUES (?, ?, ?, ?, ?)',
                      (name, date, time, type, email_decoded))
            conn.commit()
            conn.close()

            # Publicar mensaje en RabbitMQ utilizando el controlador
            reservation = {
                'name': name,
                'date': date,
                'time': time,
                'type': type,
                'email': email_decoded
            }
            controller.add_reservation(reservation)

            return redirect(url_for('index'))
        else:
            # Si falta algún campo, imprimir un mensaje de error
            print("Error: Faltan campos en el formulario")
            print(f"Campos recibidos: {list(request.form.keys())}")
            return "Error: Faltan campos en el formulario", 400
    except Exception as e:
        print(f"Error al procesar la reserva: {e}")
        return "Error al procesar la reserva", 400

if __name__ == '__main__':
    app.run(debug=True)
