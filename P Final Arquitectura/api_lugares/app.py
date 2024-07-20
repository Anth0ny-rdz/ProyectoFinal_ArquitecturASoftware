from flask import Flask
from lugares_api import lugares_api

app = Flask(__name__)
app.register_blueprint(lugares_api)

if __name__ == '__main__':
    app.run(debug=True)
