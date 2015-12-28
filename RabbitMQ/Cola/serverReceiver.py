#!/usr/bin/env python
import pika
import sys
from subprocess import call
import config as c
import threading


def send(routing,message):
    #call(["python","emitter.py", method.routing_key,body])
    propietario=""
    for x in message:
        if x==" ":
            break
        propietario=propietario+x

    for x in c.listaNodos:
        if propietario==x:
            call(["python","serverEmitter.py", x , message])


connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='127.0.0.1'))
channel = connection.channel()

channel.queue_declare(queue='servidor_queue',durable=True)


print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print ("[X]Recibido: %s" %body)
    t=threading.Thread(target=send, kwargs=dict(routing=method.routing_key, message=body))
    t.start()



channel.basic_consume(callback,
                      queue='servidor_queue',
                      no_ack=True)




channel.start_consuming()
