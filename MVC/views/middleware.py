import logging
import time
from logging.handlers import RotatingFileHandler

class WSGIMiddleware:
    def __init__(self, app):
        self.app = app
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = RotatingFileHandler('middleware.log', maxBytes=10000, backupCount=1)
        self.logger.addHandler(handler)

    def __call__(self, environ, start_response):
        request_method = environ['REQUEST_METHOD']
        request_path = environ['PATH_INFO']
        headers = {key: value for key, value in environ.items() if key.startswith('HTTP')}
        content_length = environ.get('CONTENT_LENGTH')
        request_data = environ['wsgi.input'].read(int(content_length)) if content_length else None

        start_time = time.time()

        try:
            self.logger.info(f"Received {request_method} request to {request_path} with headers: {headers} and data: {request_data}")

            response = self.app(environ, start_response)

            status_code = environ.get('HTTP_STATUS', '200 OK')  # Typically, the status is passed to start_response
            end_time = time.time()
            duration = end_time - start_time
            self.logger.info(f"Response status: {status_code}, duration: {duration:.4f} seconds")

            return response
        except Exception as e:
            self.logger.error(f"Error processing request to {request_path}: {e}")
            raise
