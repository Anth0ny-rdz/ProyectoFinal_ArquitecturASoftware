from flask import Flask
from time_api import time_api

app = Flask(__name__)
app.register_blueprint(time_api)

@app.route('/')
def index():
    return 'API Time is running. Use /api/times to access the endpoints.'

if __name__ == '__main__':
    app.run(debug=True, port=5001)
