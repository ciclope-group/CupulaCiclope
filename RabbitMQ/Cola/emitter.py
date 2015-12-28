#!/usr/bin/env python
import pika
import sys
import config as c
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host=c.servidorIP))
channel = connection.channel()

channel.queue_declare(queue=("servidor_queue"),durable=True)
message ="".join(sys.argv[1:])
channel.basic_publish(exchange='',routing_key=("servidor_queue"),body=c.me+" "+ message)
print " [x] Sent "+ message
connection.close()
