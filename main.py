import pika
import config
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(config.SERVER_IP))
channel = connection.channel()

test_payload = {
    'id': 123,
    'message': 'test'
}

def send_request():
    channel.basic_publish(
        exchange=config.EXCHANGE,
        routing_key=config.ROUTING_KEY,
        body=json.dumps(test_payload))


def send_requests(times: int):
    for _ in range(times):
        send_request()


send_requests(1000)

