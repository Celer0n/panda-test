from flask import Flask
from prometheus_client import Counter, Gauge, Histogram, Summary, generate_latest
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

# Метрики
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Request latency')
ACTIVE_REQUESTS = Gauge('active_requests', 'Number of active requests')

@app.route("/")
def hello():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    with REQUEST_LATENCY.time():
        return "Hello, World!"

@app.route("/metrics")
def metrics():
    # Экспорт метрик для Prometheus
    return generate_latest()

# Подключение метрик в качестве отдельного маршрута
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)