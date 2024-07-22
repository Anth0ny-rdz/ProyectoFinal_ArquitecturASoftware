import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify
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
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON payload provided'}), 400

        level = data.get('level')
        message = data.get('message')
        headers = dict(request.headers)

        if not level or not message:
            return jsonify({'error': 'Both level and message fields are required'}), 400

        log_message = f"Message: {message} | Headers: {headers}"

        if level == 'INFO':
            app.logger.info(log_message)
        elif level == 'ERROR':
            app.logger.error(log_message)
        elif level == 'WARNING':
            app.logger.warning(log_message)
        else:
            return jsonify({'error': 'Invalid log level'}), 400

        return jsonify({'status': 'Log created'}), 201
    except Exception as e:
        app.logger.error(f'Error logging message: {e}')
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5003)