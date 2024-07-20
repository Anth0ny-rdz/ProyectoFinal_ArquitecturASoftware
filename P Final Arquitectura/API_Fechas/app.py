from flask import Flask
from fechas_api import fechas_api

app = Flask(__name__)
app.register_blueprint(fechas_api)

if __name__ == '__main__':
    app.run(debug=True)
