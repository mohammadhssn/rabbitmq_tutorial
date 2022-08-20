import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='logs', exchange_type='fanout')
queue_name = channel.queue_declare(queue='', exclusive=True)

channel.queue_bind(queue=queue_name.method.queue, exchange='logs')
print('Waiting for logs...')


def callback(ch, method, properties, body):
    print(f'Received-> {body}')
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue=queue_name.method.queue, on_message_callback=callback)

channel.start_consuming()
