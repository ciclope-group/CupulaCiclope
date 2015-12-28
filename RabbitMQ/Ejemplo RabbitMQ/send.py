#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()
channel.queue_declare(queue='Cola')
message=' '.join(sys.argv[1:])
channel.basic_publish(exchange='',
                      routing_key='Cola',
                      body=message)
print " [x] sent %r" %(message,)

connection.close()
