import logging
import time
from logging.handlers import RotatingFileHandler


class WSGIMiddleware:
    def init(self, app):
        self.app = app
        self.app.wsgiapp = self.middleware(self.app.wsgiapp)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = RotatingFileHandler('middleware.log', maxBytes=10000, backupCount=1)

    def middleware(self, app):
        def middleware_func(environ, start_response):
            request_method = environ['REQUEST_METHOD']
            request_path = environ['PATH_INFO']
            headers = {key: value for key, value in environ.items() if key.startswith('HTTP')}
            content_length = environ.get('CONTENT_LENGTH')
            request_data = environ['wsgi.input'].read(int(content_length)) if content_length else None

            start_time = time.time()

            try:
                self.logger.info(
                    f"Received {request_method} request to {request_path} with headers: {headers} and data: {request_data}")

                response = app(environ, start_response)

                status_code = environ['status']
                end_time = time.time()
                duration = end_time - start_time
                self.logger.info(f"Response status: {status_code}, duration: {duration:.4f} seconds")

                return response
            except Exception as e:
                self.logger.error(f"Error processing request to {request_path}: {e}")
                raise

        return middleware_func