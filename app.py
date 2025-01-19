from flask import Flask
from prometheus_client import Counter, Gauge, Histogram, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

# Flask-приложение
app = Flask(__name__)

# Метрики Prometheus
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Request latency')
ACTIVE_REQUESTS = Gauge('active_requests', 'Number of active requests')

@app.route("/")
def hello():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()  # Считаем запросы
    with REQUEST_LATENCY.time():  # Засекаем время выполнения
        return "Hello, Jenkins!"

# Создаем комбинированное WSGI-приложение
application = DispatcherMiddleware(app, {
    '/metrics': make_wsgi_app()  # Добавляем метрики на /metrics
})

# Запуск приложения
if __name__ == "__main__":
    # run_simple гарантированно использует DispatcherMiddleware
    run_simple("0.0.0.0", 5000, application)