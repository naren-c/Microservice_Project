import pika
import json
import pymongo
import time
import os

time.sleep(35)

rabbitmq_host = os.getenv('RABBITMQ_HOST', '0.0.0.0:5672')
rabbitmq_user = os.getenv('RABBITMQ_USER', 'guest')
rabbitmq_pass = os.getenv('RABBITMQ_PASS', 'guest')
rabbitmq_queue = os.getenv('RABBITMQ_QUEUE_DELETE', 'delete_record')
# Establishing connection to MongoDB
client = pymongo.MongoClient("mongodb://172.17.0.1:27017/")
db = client["mydatabase"]
collection = db["students"]

# Callback function to process incoming messages
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    srn = json.loads(body.decode('utf-8'))
    print(srn)
    collection.delete_one({"SRN": srn["SRN"]})
    print("Deleted record with SRN:", srn)
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Establishing connection to RabbitMQ


credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('172.17.0.1',
                                   5672,
                                   '/',
                                   credentials)

connection = pika.BlockingConnection(parameters)


# connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.1:5672'))
channel = connection.channel()

# Declaring the queue
channel.queue_declare(queue='delete_record')

# Listening for incoming messages
channel.basic_consume(queue='delete_record', on_message_callback=callback)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

