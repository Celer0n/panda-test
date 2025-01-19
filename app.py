from flask import Flask
from prometheus_client import Counter, Gauge, Histogram, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

app = Flask(__name__)

# Метрики
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Request latency')
ACTIVE_REQUESTS = Gauge('active_requests', 'Number of active requests')

@app.route("/")
def hello():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()  # Увеличиваем счетчик запросов
    with REQUEST_LATENCY.time():  # Засекаем время выполнения
        return "Hello, World!"

# WSGI-приложение с маршрутом /metrics
application = DispatcherMiddleware(app, {
    '/metrics': make_wsgi_app()  # Подключаем метрики Prometheus
})

if __name__ == "__main__":
    # Используем run_simple для запуска приложения с DispatcherMiddleware
    run_simple("0.0.0.0", 5000, application)