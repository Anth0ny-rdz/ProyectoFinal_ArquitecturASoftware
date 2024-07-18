from flask import Blueprint, request, jsonify
import sqlite3

lugares_api = Blueprint('lugares_api', __name__)

DATABASE = 'reservations.sql'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Obtener filas como diccionarios
    return conn

@lugares_api.route('/api/lugares', methods=['GET'])
def obtener_lugares():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM lugares')
    lugares = c.fetchall()
    conn.close()
    
    lugares = [dict(row) for row in lugares]  # Convertir filas a diccionarios
    return jsonify(lugares)

@lugares_api.route('/api/lugares', methods=['POST'])
def agregar_lugar():
    nuevo_lugar = request.json
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO lugares (nombre, descripcion) VALUES (?, ?)',
              (nuevo_lugar['nombre'], nuevo_lugar['descripcion']))
    conn.commit()
    conn.close()
    return jsonify(nuevo_lugar), 201

@lugares_api.route('/api/lugares/<int:id>', methods=['DELETE'])
def eliminar_lugar(id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM lugares WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return '', 204
