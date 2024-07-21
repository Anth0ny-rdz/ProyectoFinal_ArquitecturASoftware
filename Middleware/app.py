import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request
import requests

app = Flask(__name__)
log_handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
log_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)
app.logger.addHandler(log_handler)
# Define the logging for the API URL
@app.route('/log', methods=['POST'])
def log_message():
    data = request.get_json()
    level = data['level']
    message = data['message']
    if level == 'INFO':
        app.logger.info(message)
    elif level == 'ERROR':
        app.logger.error(message)
    elif level == 'WARNING':
        app.logger.warning(message)
    else:
        return 'Invalid log level', 400
    return 'Log created', 201

if __name__ == '__main__':
    app.run(debug=True, port=5003)