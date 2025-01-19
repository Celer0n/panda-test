from flask import Flask
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

# Create a DispatcherMiddleware to combine Flask and Prometheus apps
application = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple("0.0.0.0", 5000, application)