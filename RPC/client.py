import uuid

import pika


class Sender:

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.on_response, auto_ack=True)

    def on_response(self, ch, method, properties, body):
        if self.corr_id == properties.correlation_id:
            self.response = body

    def call(self, number):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='', routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.queue_name,
                correlation_id=self.corr_id
            ),
            body=str(number)
        )
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


send = Sender()
response = send.call(30)
print(f'response: {response}')
