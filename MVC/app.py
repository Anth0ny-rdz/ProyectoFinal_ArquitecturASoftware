import sqlite3
import os
from flask import Flask, request, redirect, url_for, render_template, flash, jsonify
import requests
import sys

# Add QueueManager directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.controller_shurima import ControllerShurima  # Import the controller

controller = ControllerShurima()

app = Flask(__name__)
app.secret_key = b'\x8c\x88\x17O\xd2\xfdx\xa6\xb6\x9e\x15\xdfS\x980\xe8\xf4\x19\x80\xb3H\xa6\xf83'

# URL of the new time API
TIME_API_URL = 'http://localhost:5001/api/times'
# URL of the new places API
PLACES_API_URL = 'http://localhost:5002/api/places'
# URL of the new logging API
LOGGING_API_URL = 'http://localhost:5003/log'

@app.route('/')
def index():
    log_middleware('INFO', 'Starting App')
    try:
        log_middleware('INFO', 'Fetching Api_Reservations')
        # Fetch reservations from the local database
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM reservations')
        reservations = c.fetchall()

        log_middleware('INFO', 'Fetching Api_Times')
        # Fetch available times from the API
        response = requests.get(TIME_API_URL)
        response.raise_for_status()
        available_times = response.json()

        log_middleware('INFO', 'Fetching Api_Places')
         # Fetch available places from the API
        response = requests.get(PLACES_API_URL)
        response.raise_for_status()
        available_places = response.json()

        # Fetch space types from the APIPlaces database
        conn_space_types = get_space_types_connection()
        c = conn_space_types.cursor()
        c.execute('SELECT DISTINCT name FROM places')
        space_types = [row['name'] for row in c.fetchall()]
        
        conn.close()
        log_middleware('INFO', 'All data fetched successfully')

        reservations = [dict(row) for row in reservations]

        log_middleware('INFO', f"Reservations fetched from DB: {reservations}")

        return render_template('index.html', reservations=reservations, available_times=available_times, space_types=space_types)
    except Exception as e:
        log_middleware('ERROR', f"Error: {e}")
        return f"An error occurred while fetching data: {e}"

@app.route('/reserve', methods=['POST'])
def reserve():
    name = request.form['name']
    email = request.form['email']
    date = request.form['date']
    time = request.form['time']
    type = request.form['type']

    try:
        # Check availability with the API Time
        response = requests.get(f'{TIME_API_URL}/availability', params={'date': date, 'time': time, 'type': type})
        response.raise_for_status()
        availability = response.json()

        if not availability.get('available'):
            flash('The selected time is not available.', 'error')
            return redirect(url_for('index'))

        # Book the time with the API Time
        response = requests.post(f'{TIME_API_URL}/book', json={'date': date, 'time': time, 'type': type})
        response.raise_for_status()
        booking_result = response.json()

        if not booking_result.get('success'):
            flash('Failed to book the time slot.', 'error')
            return redirect(url_for('index'))

        # Add reservation to the local database
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('INSERT INTO reservations (name, email, date, time, type) VALUES (?, ?, ?, ?, ?)',
                  (name, email, date, time, type))
        conn.commit()

        # Get the ID of the newly created reservation
        reservation_id = c.lastrowid
        conn.close()

        # Create the backup dictionary
        reservation = {
            'id': reservation_id,
            'name': name,
            'email': email,
            'date': date,
            'time': time,
            'type': type
        }

        # Send the reservation to RabbitMQ and start consuming
        print("se envió")
        controller.add_reservation(reservation)

        flash('Reserva realizada con éxito.', 'success')

        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error: {e}")
        flash('An error occurred while making the reservation.', 'error')
        return redirect(url_for('index'))

@app.route('/check_availability', methods=['GET'])
def check_availability():
    date = request.args.get('date')
    time = request.args.get('time')
    type = request.args.get('type')

    try:
        response = requests.get(f'{TIME_API_URL}/availability', params={'date': date, 'time': time, 'type': type})
        response.raise_for_status()
        availability = response.json()

        return {"available": availability.get('available', False)}
    except Exception as e:
        print(f"Error: {e}")
        return {"available": False, "error": str(e)}

# Define the database directory
DATABASE = os.path.join(os.path.dirname(__file__), 'database', 'reservations.sql')
# Define the database directory for space types
SPACE_TYPES_DATABASE = os.path.join(os.path.dirname(__file__), '..', 'APIPlaces', 'places.db')


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

def get_space_types_connection():
    try:
        if not os.path.exists(SPACE_TYPES_DATABASE):
            print(f"Database file {SPACE_TYPES_DATABASE} does not exist!")
            raise FileNotFoundError(f"Database file {SPACE_TYPES_DATABASE} not found.")
        else:
            print(f"Database file {SPACE_TYPES_DATABASE} found.")
        conn = sqlite3.connect(SPACE_TYPES_DATABASE)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Error connecting to the space types database: {e}")
        raise

def log_middleware(level, message):
    try:
        response = requests.post(LOGGING_API_URL, json={'level': level, 'message': message})
        response.raise_for_status()
    except Exception as e:
        print(f"Error: {e}")



if __name__ == '__main__':
    app.run(debug=True)