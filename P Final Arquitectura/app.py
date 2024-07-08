import sqlite3
from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

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
    name = request.form['name']
    date = request.form['date']
    time = request.form['time']
    type = request.form['type']

    conn = sqlite3.connect('reservations.sql')
    c = conn.cursor()
    c.execute('INSERT INTO reservations (name, date, time, type) VALUES (?, ?, ?, ?)',
              (name, date, time, type))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
