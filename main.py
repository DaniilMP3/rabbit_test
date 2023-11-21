import pika
import config
import json
import time

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('10.62.0.152', 5672,'/', credentials))
channel = connection.channel()

channel.queue_declare(queue = "test", durable = True)

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
        time.sleep(2)


send_requests(10)

channel_consume = connection.channel()
def callback(channel, method, properties, body):
    print(f"Recieved: {body}")


channel_consume.basic_consume(queue='test', on_message_callback=callback, auto_ack=True)
channel_consume.start_consuming()


connection.close()

