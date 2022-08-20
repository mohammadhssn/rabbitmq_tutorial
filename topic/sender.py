import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

messages = {
    'error.warning.important': b'This is an important messages',
    'info.warning.notimportant': b'This is not an important messages',
}

for key, value in messages.items():
    channel.basic_publish(exchange='topic_logs', routing_key=key, body=value)

print('Message Send')
connection.close()
