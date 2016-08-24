#!/usr/bin/env python
import pika
import sys
import config as c
import pika
import socket

credentials = pika.PlainCredentials('cupula', '1234')
connection = pika.BlockingConnection(pika.ConnectionParameters(
        c.dictIP['servidorIP'],
        5672,
        'Cupula',
        credentials))
channel = connection.channel()

channel.queue_declare(queue=("servidor_queue"),durable=True)
message =" ".join(sys.argv[1:])
if (message.find("-newNode")!=-1):
    message= c.myIP +" "+ message
    print message
channel.basic_publish(exchange='',routing_key=("servidor_queue"),body=c.me+" "+ message)
print " [x] Sent "+ message
connection.close()
