import webbrowser
from threading import Timer
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from app import app, controller

middleware = DispatcherMiddleware(app)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == "__main__":
    try:
        from werkzeug.serving import run_simple
        # Use the middleware with your app
        run_simple('localhost', 5000, middleware, use_debugger=True)
    finally:
        controller.close_connection()
