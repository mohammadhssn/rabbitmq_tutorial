import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()
channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    print(f'Received  {body}')


channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print('Waiting for message, to exit press ctrl+c')

channel.start_consuming()
