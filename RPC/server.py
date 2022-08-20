import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')


def callback(ch, method, properties, body):
    number = int(body)
    print('processing message!')
    time.sleep(5)
    response = number + 1
    ch.basic_publish(
        exchange='', routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=str(response)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=callback)
print('Waiting for message...')
channel.start_consuming()
