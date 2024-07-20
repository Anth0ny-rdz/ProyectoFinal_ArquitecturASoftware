from flask import Blueprint, jsonify
import sqlite3
import os

api_places = Blueprint('api_places', __name__)

DATABASE = os.path.join(os.path.dirname(__file__), 'places.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@api_places.route('/api/places', methods=['GET'])
def get_places():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT name, description FROM places')
    places = c.fetchall()
    conn.close()

    return jsonify([dict(place) for place in places])
