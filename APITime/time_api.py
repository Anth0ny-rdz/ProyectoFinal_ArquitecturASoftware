from flask import Blueprint, request, jsonify
import sqlite3
import os

time_api = Blueprint('time_api', __name__)

DATABASE = os.path.join(os.path.dirname(__file__), 'scripts', 'database', 'availability.sql')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Get rows as dictionaries
    return conn

@time_api.route('/api/times', methods=['GET'])
def get_times():
    date = request.args.get('date')
    time = request.args.get('time')
    type = request.args.get('type')

    conn = get_db_connection()
    c = conn.cursor()

    query = 'SELECT * FROM availability WHERE 1=1'
    params = []

    if date:
        query += ' AND date = ?'
        params.append(date)
    if time:
        query += ' AND time = ?'
        params.append(time)
    if type:
        query += ' AND type = ?'
        params.append(type)

    c.execute(query, params)
    available_times = c.fetchall()
    conn.close()

    available_times = [dict(row) for row in available_times]  # Convert rows to dictionaries
    return jsonify(available_times)

@time_api.route('/api/times', methods=['POST'])
def add_time():
    new_availability = request.json
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO availability (name, date, time, type) VALUES (?, ?, ?, ?)',
              (new_availability['name'], new_availability['date'], new_availability['time'], new_availability['type']))
    conn.commit()
    conn.close()
    return jsonify(new_availability), 201

@time_api.route('/api/times/<int:id>', methods=['DELETE'])
def delete_time(id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM availability WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return '', 204

@time_api.route('/api/times/availability', methods=['GET'])
def check_availability():
    date = request.args.get('date')
    time = request.args.get('time')
    type = request.args.get('type')

    if not date or not time or not type:
        return jsonify({"error": "Please provide date, time, and type"}), 400

    conn = get_db_connection()
    c = conn.cursor()

    query = 'SELECT COUNT(*) as count FROM availability WHERE date = ? AND time = ? AND type = ?'
    c.execute(query, (date, time, type))
    result = c.fetchone()
    conn.close()

    if result['count'] > 0:
        return jsonify({"available": True})
    else:
        return jsonify({"available": False})
    
@time_api.route('/api/times/book', methods=['POST'])
def book_time():
    data = request.json
    date = data['date']
    time = data['time']
    type = data['type']

    conn = get_db_connection()
    c = conn.cursor()

    # Check if the time is available
    query = 'SELECT COUNT(*) as count FROM availability WHERE date = ? AND time = ? AND type = ?'
    c.execute(query, (date, time, type))
    result = c.fetchone()

    if result['count'] > 0:
        # Mark the time as booked
        c.execute('DELETE FROM availability WHERE date = ? AND time = ? AND type = ?', (date, time, type))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    else:
        conn.close()
        return jsonify({"success": False, "error": "Time slot not available"}), 400
