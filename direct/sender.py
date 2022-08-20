import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

messages = {
    'info': b'this is INFO message',
    'error': b'this is ERROR message',
    'warning': b'this is WARNING message',
}

for key, value in messages.items():
    channel.basic_publish(exchange='direct_logs', routing_key=key, body=value)

print('Sending Message.')
connection.close()
