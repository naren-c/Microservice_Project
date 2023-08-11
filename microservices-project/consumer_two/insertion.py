import pika
import os
import json
import pymongo
import time

time.sleep(2)

# Get the environment variables
rabbitmq_host = os.getenv('RABBITMQ_HOST', '0.0.0.0:5672')
rabbitmq_user = os.getenv('RABBITMQ_USER', 'guest')
rabbitmq_pass = os.getenv('RABBITMQ_PASS', 'guest')
rabbitmq_queue = os.getenv('RABBITMQ_QUEUE_INSERT', 'insert_record')

client = pymongo.MongoClient("mongodb://172.17.0.1:27017/")
db = client["mydatabase"]
collection = db["students"]

# Define the callback function for the consumer
def callback(ch, method, properties, body):
    print(" [x] Received ", body.decode())
    try:
        # Parse the message from the queue
        message = json.loads(body.decode())
        
        # Insert the record to the database
        data = {"name": message['Name'], "SRN": message['SRN'], "Section": message['Section']}
        insert_result = collection.insert_one(data)
        print(insert_result.inserted_id)
    except Exception as e:
        print(f"Error: {e}")

# Set up the connection and channel to RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('172.17.0.1',
                                   5672,
                                   '/',
                                   credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue="insert_record")

# Set the prefetch count to 1 to ensure that the consumer receives only one message at a time
# channel.basic_qos(prefetch_count=1)

# Start consuming the messages from the queue
channel.basic_consume(queue="insert_record", on_message_callback=callback,auto_ack=True)

# Start the consumer
print('Insert Record Consumer started...')
channel.start_consuming()

