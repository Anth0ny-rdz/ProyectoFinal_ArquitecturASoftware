import webbrowser
from threading import Timer
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from app import app
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from QueueManager.Publisher.Publisher import Publisher

publisher = Publisher()

middleware = DispatcherMiddleware(app)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == "__main__":
    try:
        from werkzeug.serving import run_simple
        Timer(1, open_browser).start()  # Open navigator automatically
        # Use the middleware with your app
        run_simple('localhost', 5000, middleware, use_debugger=True)
    finally:
        Publisher.close_connection()
