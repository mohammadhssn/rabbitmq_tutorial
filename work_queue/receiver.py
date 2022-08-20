import time
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='two', durable=True)
print('waiting for message, press ctrl+c to exit.')


def callback(ch, method, properties, body):
    print(f'Received: {body}')
    print(properties.headers)
    print('-' * 20)
    print(method)
    time.sleep(9)
    print('Done')
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='two', on_message_callback=callback)

channel.start_consuming()
