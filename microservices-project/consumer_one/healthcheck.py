import pika
import time

time.sleep(35)

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('172.17.0.1',
                                   5672,
                                   '/',
                                   credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='health_check')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    ch.basic_ack(delivery_tag=method.delivery_tag) # acknowledge the message

channel.basic_consume(queue='health_check', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

