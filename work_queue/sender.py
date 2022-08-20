import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='two', durable=True)  # persistent queue (chanel)

message = b'This is testing message'

channel.basic_publish(exchange='', routing_key='two', body=message,
                      properties=pika.BasicProperties(delivery_mode=2, headers={
                          'name': 'mohammadhssn'}))  # delivery_mode=2 -> persistent messages

print('Send Message.')
connection.close()
