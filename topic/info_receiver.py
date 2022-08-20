import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

binding_key = '#.notimportant'  # '*.*.notimportant'
channel.queue_bind(queue=queue_name, exchange='topic_logs', routing_key=binding_key)

print('Waiting for message...')


def callback(ch, method, properties, body):
    print(body)


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
