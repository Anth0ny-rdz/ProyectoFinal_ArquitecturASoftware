from flask import Blueprint, request, jsonify
import sqlite3

fechas_api = Blueprint('fechas_api', __name__)

DATABASE = 'reservations.sql'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Obtener filas como diccionarios
    return conn

@fechas_api.route('/api/fechas', methods=['GET'])
def obtener_fechas():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM reservations')
    reservas = c.fetchall()
    conn.close()
    
    reservas = [dict(row) for row in reservas]  # Convertir filas a diccionarios
    return jsonify(reservas)

@fechas_api.route('/api/fechas', methods=['POST'])
def agregar_fecha():
    nueva_reserva = request.json
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO reservations (name, date, time, type) VALUES (?, ?, ?, ?)',
              (nueva_reserva['name'], nueva_reserva['date'], nueva_reserva['time'], nueva_reserva['type']))
    conn.commit()
    conn.close()
    return jsonify(nueva_reserva), 201

@fechas_api.route('/api/fechas/<int:id>', methods=['DELETE'])
def eliminar_fecha(id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM reservations WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return '', 204
