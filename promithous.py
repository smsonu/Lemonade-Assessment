#Write a Prometheus exporter in Python/Golang that connects to a specified RabbitMQ HTTP API (management plugin) and exports queue metrics.

from prometheus_client import start_http_server, Gauge
import requests
import os
import time

# Environment variables
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'http://localhost:15672')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')

# Prometheus metrics
messages_gauge = Gauge('rabbitmq_individual_queue_messages', 'Total messages in the queue', ['host', 'vhost', 'name'])
messages_ready_gauge = Gauge('rabbitmq_individual_queue_messages_ready', 'Messages ready to be delivered', ['host', 'vhost', 'name'])
messages_unacked_gauge = Gauge('rabbitmq_individual_queue_messages_unacknowledged', 'Messages unacknowledged', ['host', 'vhost', 'name'])

def fetch_queue_metrics():
    url = f"{RABBITMQ_HOST}/api/queues"
    response = requests.get(url, auth=(RABBITMQ_USER, RABBITMQ_PASSWORD))
    response.raise_for_status()  # Raise exception for HTTP errors
    return response.json()

def update_metrics():
    queues = fetch_queue_metrics()
    for queue in queues:
        host = RABBITMQ_HOST
        vhost = queue['vhost']
        name = queue['name']
        messages_gauge.labels(host=host, vhost=vhost, name=name).set(queue['messages'])
        messages_ready_gauge.labels(host=host, vhost=vhost, name=name).set(queue['messages_ready'])
        messages_unacked_gauge.labels(host=host, vhost=vhost, name=name).set(queue['messages_unacknowledged'])

if __name__ == '__main__':
    start_http_server(8000)  # Expose metrics on port 8000
    while True:
        update_metrics()
        time.sleep(15)  # Fetch metrics every 15 seconds

