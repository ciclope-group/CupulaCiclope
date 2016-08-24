#!/usr/bin/env python
import pika
import sys
#Importamos el archivo de configuracion
import config as c

#Establecemos las credenciales
credentials = pika.PlainCredentials('cupula', 'informaticaciclope')
#Establecemos la conexion al servidor a traves del puerto 5672
connection = pika.BlockingConnection(pika.ConnectionParameters(c.urlServer, 5672,'/',credentials))
channel = connection.channel()
#Declaramos La cola por la que recibiremos (Por si acaso no esta creada aun)
channel.queue_declare(queue=c.me, durable=True)
#Declaramos las colas a las que enviaremos con emitter.py, por si acaso no estan declaradas aun
for x in c.list:
    channel.queue_declare(queue=x, durable=True)
#Hacemos en binding de los exchanges con las colas, teniendo en cuenta el routing key
for x,y in zip(c.list,c.severity):
    channel.exchange_declare(exchange=x,
                            type='direct')
    channel.queue_bind(exchange=x,
                       queue=c.me,
                       routing_key=y)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % (body))

channel.basic_consume(callback,
                        queue=c.me,
                        no_ack=True)
channel.start_consuming()
