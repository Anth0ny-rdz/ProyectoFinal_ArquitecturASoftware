import sqlite3
import os
from flask import Flask, request, redirect, url_for, render_template, flash
from controllers.controller_shurima import ControllerShurima
from API_Fechas.fechas_api import fechas_api
from api_lugares.lugares_api import lugares_api

app = Flask(__name__)
app.secret_key = 'your_secret_key'
controller = ControllerShurima()

# Definir el directorio de la base de datos
DATABASE = os.path.join(os.path.dirname(__file__), 'database', 'reservations.sql')

def get_db_connection():
    try:
        if not os.path.exists(DATABASE):
            print(f"Database file {DATABASE} does not exist!")
            raise FileNotFoundError(f"Database file {DATABASE} not found.")
        else:
            print(f"Database file {DATABASE} found.")
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM reservations')
        reservations = c.fetchall()

        c.execute('SELECT * FROM lugares')
        lugares = c.fetchall()

        conn.close()

        reservations = [dict(row) for row in reservations]
        lugares = [dict(row) for row in lugares]

        print(f"Reservations fetched: {reservations}")
        print(f"Lugares fetched: {lugares}")

        return render_template('index.html', reservations=reservations, lugares=lugares)
    except Exception as e:
        print(f"Error: {e}")
        return f"An error occurred while fetching data from the database: {e}"

@app.route('/reserve', methods=['POST'])
def reserve():
    name = request.form['name']
    email = request.form['email']
    date = request.form['date']
    time = request.form['time']
    type = request.form['type']

    try:
        conn = get_db_connection()
        c = conn.cursor()

        # Verificar si ya existe una reserva para la misma fecha, hora y tipo
        c.execute('SELECT * FROM reservations WHERE date = ? AND time = ? AND type = ?', (date, time, type))
        existing_reservation = c.fetchone()

        if existing_reservation:
            flash('La reserva ya existe para la fecha y hora especificadas.', 'error')
            conn.close()
            return redirect(url_for('index'))

        # Si no existe, realizar la inserción
        c.execute('INSERT INTO reservations (name, email, date, time, type) VALUES (?, ?, ?, ?, ?)', (name, email, date, time, type))
        conn.commit()
        flash('Reserva realizada con éxito.', 'success')

        # Obtener la ID de la reserva recién creada
        reservation_id = c.lastrowid
        conn.close()

        # Crear el diccionario de reserva
        reservation = {
            'id': reservation_id,
            'name': name,
            'email': email,
            'date': date,
            'time': time,
            'type': type
        }

        # Enviar la reserva a RabbitMQ y comenzar a consumir
        controller.add_reservation(reservation)

        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error: {e}")
        flash('Ocurrió un error al realizar la reserva.', 'error')
        return redirect(url_for('index'))

@app.route('/check_availability', methods=['GET'])
def check_availability():
    date = request.args.get('date')
    time = request.args.get('time')
    type = request.args.get('type')

    print(f"Checking availability for date: {date}, time: {time}, type: {type}")

    try:
        conn = get_db_connection()
        c = conn.cursor()

        query = 'SELECT * FROM reservations WHERE date = ? AND time = ? AND type = ?'
        print(f"Executing query: {query} with values ({date}, {time}, {type})")
        c.execute(query, (date, time, type))
        reservation = c.fetchone()

        print(f"Reservation found: {reservation}")

        conn.close()

        if reservation:
            return {"available": False}
        else:
            return {"available": True}
    except Exception as e:
        print(f"Error: {e}")
        return {"available": False, "error": str(e)}

app.register_blueprint(fechas_api)
app.register_blueprint(lugares_api)

if __name__ == '__main__':
    app.run(debug=True)
