from flask import Flask, request
import pika

import time

time.sleep(20)

app = Flask(__name__)

# Set up connection to RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('172.17.0.1',
                                   5672,
                                   '/',
                                   credentials)

connection = pika.BlockingConnection(parameters)





channel = connection.channel()
"""
# Create an exchange named "microservices-exchange" with direct type
#channel.exchange_declare(exchange='microservices-exchange', exchange_type='direct')

# Create queues for each consumer with binding keys
#channel.queue_declare(queue='health_check')
#channel.queue_bind(exchange='microservices-exchange', queue='health_check', routing_key='health_check')

channel.queue_declare(queue='insert_record')
channel.queue_bind(exchange='microservices-exchange', queue='insert_record', routing_key='insert_record')

channel.queue_declare(queue='read_database')
channel.queue_bind(exchange='microservices-exchange', queue='read_database', routing_key='read_database')

channel.queue_declare(queue='delete_record')
channel.queue_bind(exchange='microservices-exchange', queue='delete_record', routing_key='delete_record')
"""
channel.queue_declare(queue = "insert_queue")
@app.route('/health_check', methods=['GET'])
def health_check():
    # Send a message to "health_check" queue with routing key "health_check"
    channel.basic_publish(exchange='microservices-exchange', routing_key='health_check', body="Checking RabbitMQ connection...")
    return "Health check message sent!"

@app.route('/insert_record', methods=['POST'])
def insert_record():
    # Send a message to "insert_record" queue with routing key "insert_record"
    name = request.form['Name']
    srn = request.form['SRN']
    section = request.form['Section']
    message = "{" + f'"Name":"{name}", "SRN":"{srn}", "Section":"{section}"' + "}"
    channel.basic_publish(exchange='', routing_key='insert_record', body=message)
    return "Record inserted!"
    

@app.route('/delete_record', methods=['POST'])
def delete_record():
    # Send a message to "delete_record" queue with routing key "delete_record"
    srn = request.form['SRN']
    message = "{" + f'"SRN":"{srn}"' + "}"
    channel.basic_publish(exchange='', routing_key='delete_record', body=message)
    return "Record deleted!"

    
@app.route('/read_record', methods=['GET'])
def read_record():
    # Send a message to "insert_record" queue with routing key "insert_record"
    message = ""
    channel.basic_publish(exchange='', routing_key='read_record', body=message)
    return "Record !"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

