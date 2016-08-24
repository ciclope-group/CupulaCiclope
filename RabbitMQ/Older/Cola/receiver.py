#!/usr/bin/env python
import pika
import time
import config as c

credentials = pika.PlainCredentials('cupula', '1234')
connection = pika.BlockingConnection(pika.ConnectionParameters(
        c.dictIP['servidorIP'],
        5672,
        'Cupula',
        credentials))
channel = connection.channel()

channel.queue_declare(queue=c.me+"_queue",durable=True)
print ' [*] Waiting for messages. To exit press CTRL+C'
print c.me+"_queue"

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)

channel.basic_consume(callback, queue=c.me+"_queue",no_ack=True)

channel.start_consuming()
