#!/usr/bin/env python
import pika
import sys
from subprocess import call
import config as c
import threading
import time

#------Fincion para enviar a otros nodos-------
def send(routing,message):
    #call(["python","emitter.py", method.routing_key,body])
    propietario=routing
    call(["python","serverEmitter.py", propietario , message])
#-----Funcion para incluir un nuevo nodo------
def newNode(routing,message):
    call(["python","newNode.py", routing, message])
#-----Funcion para modificar un nodo------
def modNode(routing,message):
    call(["python","modNode.py", routing, message])
#-----Funcion para modificar un nodo------
def delNode(routing,message):
    call(["python","delNode.py", routing, message])
#------Funcion para escribir en el log-----
def log(message):
    outfile = open('log.txt', 'a') # Indicamos el valor 'w'.
    outfile.write("\n")
    outfile.write(message)
    outfile.close()

#------------INICIO DE APLICACION---------

#-------------Credenciales de grupo-------
credentials = pika.PlainCredentials('cupula', '1234')
#----------Conectarse al vhost Cupula que esta alojado en la misma maquina------------
connection = pika.BlockingConnection(pika.ConnectionParameters(
        '127.0.0.1',
        5672,
        'Cupula',
        credentials))
channel = connection.channel()
#-----------Declaracion de la cola en la que publican todos los nodos----------------
channel.queue_declare(queue='servidor_queue',durable=True)

print "******************************************************************************************************"
print "**********************************Ciclope Server Initiated********************************************"
print "******************************************************************************************************"
print ' [*] Server started. Waiting for new messages'
#----------Callback cuando llega algun mensaje---------
def callback(ch, method, properties, body):
    reload(c)
    words = body.split()
    node=words[0]
    rest=" ".join(words[1:])
    print "[x] Received from " +node+ " :" +rest
    if(rest.find("-newNode")!=-1):
        #---------Se verifica que el nodo no esta incluido en listaNodos------------
        for x in c.listaNodos:
            if x.find(node)!=-1:
                return
        outfile = open('log.txt', 'a')
        logMessage="[X] New node called "+node + " joined on " + time.strftime("%H:%M:%S")+" " + time.strftime("%d/%m/%Y")
        log(logMessage)
        #--------Se lanza proceso para anhadir nodo-----------
        t=threading.Thread(target=newNode, kwargs=dict(routing=node, message=rest))
        t.start()
    elif rest.find("-modNode")!=-1:
        #---------Se verifica que el nodo esta incluido en listaNodos------------
        finded=0
        for x in c.listaNodos:
            if x.find(node)!=-1:
                finded=1
        if finded==0:
            t=threading.Thread(target=send, kwargs=dict(routing=node, message=body))
            t.start()
        rest=" ".join(words[2:])
        outfile = open('log.txt', 'a')
        logMessage="[X] Modifying node "+node + " at " + time.strftime("%H:%M:%S")+" " + time.strftime("%d/%m/%Y")
        log(logMessage)
        #--------Se lanza proceso para anhadir nodo-----------
        t=threading.Thread(target=modNode, kwargs=dict(routing=node, message=rest))
        t.start()
    elif rest.find("-delNode")!=-1:
        #---------Se verifica que el nodo no esta incluido en listaNodos------------
        finded=0
        for x in c.listaNodos:
            if x.find(node)!=-1:
                finded=1
        if finded==0:
            t=threading.Thread(target=send, kwargs=dict(routing=node, message=body))
            t.start()
        rest=" ".join(words[2:])
        outfile = open('log.txt', 'a')
        logMessage="[X] Deleting node "+node + " at " + time.strftime("%H:%M:%S")+" " + time.strftime("%d/%m/%Y")
        log(logMessage)
        #--------Se lanza proceso para anhadir nodo-----------
        t=threading.Thread(target=delNode, kwargs=dict(routing=node, message=rest))
        t.start()

    else:

        logMessage="[X] "+node + " published: "+ rest +" on " + time.strftime("%H:%M:%S")+" " + time.strftime("%d/%m/%Y")
        log(logMessage)
        t=threading.Thread(target=send, kwargs=dict(routing=node, message=body))
        t.start()



channel.basic_consume(callback,
                      queue='servidor_queue',
                      no_ack=True)




channel.start_consuming()
