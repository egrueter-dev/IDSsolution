#!/usr/bin/env python
import pika
import json
import os
import time
import datetime
import sys # imported this..

# from utils import parse_log, is_get_request

## <TODO: Fix this module import error!> ##
# I know this is bad, sorry ;(
def parse_log(msg):
    # Retrieves relevant information from GET request
    decomposed_message = msg.split(" ")
    source = decomposed_message[0]
    status = decomposed_message[-2]
    time = decomposed_message[3][1:]
    day = datetime.datetime.strptime(time, "%d/%b/%Y:%X").date()
    return day, status, source

def is_get_request(msg):
    # Determines is msg is a GET request
    decomposed_message = msg.split(" ")
    return len(decomposed_message) >= 6 and decomposed_message[5] == "\"GET"
## </TODO> ##

#Connect to RabbitMQ
credentials = pika.PlainCredentials(os.environ['RABBITMQ_DEFAULT_USER'], os.environ['RABBITMQ_DEFAULT_PASS'])
parameters = pika.ConnectionParameters(host='rabbit', port=5672, credentials=credentials)

while True:
    try:
        connection = pika.BlockingConnection(parameters)
        break
    except pika.exceptions.ConnectionClosed:
        print('Ingestion: RabbitMQ not up yet.')
        time.sleep(2)

print('Ingestion: Connection to RabbitMQ established')

# Start queue
channel = connection.channel()
channel.queue_declare(queue='log-analysis')

f = open('weblogs.log', 'r', errors='ignore') # ignore bad data

while True:
    try:
        msg = f.readline()

        if not msg: 
            break

        #If message is GET request, ingest it into the queue
        if is_get_request(msg):
            # Parse GET request for relevant information
            day, status, source = parse_log(msg)

            # Store in RabbitMQ
            body = json.dumps({'day': str(day), 'status': status})
            channel.basic_publish(exchange='', routing_key='log-analysis', body=body)
        
    except:
        print("Unexpected error:" +  sys.exc_info()[0])
    
connection.close()
