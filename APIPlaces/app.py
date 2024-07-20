from flask import Flask
from api_places import api_places

app = Flask(__name__)
app.register_blueprint(api_places)

@app.route('/')
def index():
    return 'API Places is running. Use /api/places to access the endpoints.'

if __name__ == '__main__':
    app.run(debug=True, port=5002)  
