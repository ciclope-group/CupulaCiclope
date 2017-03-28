#!/usr/bin/env python
import pika
import sys
#Importamos el archivo de configuracion
import config as c
#Establecemos las credenciales
credentials = pika.PlainCredentials('xxx', 'xxx')
#Establecemos la conexion al servidor a traves del puerto 5672
connection = pika.BlockingConnection(pika.ConnectionParameters(c.urlServer, 5672,'/',credentials))
channel = connection.channel()
#Declaramos La cola por la que recibiremos (Por si acaso no esta creada aun)
channel.queue_declare(queue=c.me, durable=True)
#Declaramos el exchange de tipo direct
channel.exchange_declare(exchange=c.me,
                         type='direct')
#Si no se ha especificado la severidad, se establece por defecto "info"
if len(sys.argv) > 2:
	severity = sys.argv[1]
	message = ''.join(sys.argv[2:])
else:
	severity = "info"
        message = ''.join(sys.argv[1:])
#Publicamos en el exchange
channel.basic_publish(exchange=c.me,
                      routing_key=severity,
                      body=message)
print(" [x] Sent %r " % (message))
print("Severity: " + severity)
connection.close()
