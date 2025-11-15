from flask import Flask, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

# Metrics
REQUEST_COUNT = Counter(
    'flask_request_count', 
    'Total request count of the Flask app',
    ['method', 'endpoint']
)

REQUEST_LATENCY = Histogram(
    'flask_request_latency_seconds', 
    'Latency of requests in seconds', 
    ['endpoint']
)

# Home route
@app.route('/')
def home():
    start_time = time.time()

    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()

    latency = time.time() - start_time
    REQUEST_LATENCY.labels(endpoint='/').observe(latency)

    return "Hello from Flask App with Prometheus Metrics!"

# Metrics endpoint for Prometheus
@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
