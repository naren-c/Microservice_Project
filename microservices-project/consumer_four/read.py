import pika
import pymongo
from pymongo import MongoClient
import time
import os
import json

time.sleep(35)

# connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.1:5672'))
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('172.17.0.1',
                                   5672,
                                   '/',
                                   credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='read_record')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://172.17.0.1:27017/")
    db = client["mydatabase"]
    collection = db["students"]


    # Get all records from the database
    records = collection.find()

    # Print all records
    for record in records:
        print(record)


channel.basic_consume(queue='read_record', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

