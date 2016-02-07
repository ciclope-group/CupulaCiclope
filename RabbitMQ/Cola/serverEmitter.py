#!/usr/bin/env python
import pika
import sys
import config as c
#!/usr/bin/env python
import pika
import sys


credentials = pika.PlainCredentials('cupula', '1234')
connection = pika.BlockingConnection(pika.ConnectionParameters(
        c.dictIP['servidorIP'],
        5672,
        'Cupula',
        credentials))
channel = connection.channel()
targ=sys.argv[1]
rest=sys.argv[2]
if rest.find("-direct")!=-1:
    channel.queue_declare(queue=targ+"_queue",durable=True)
    rest=rest.split()
    rest.remove("-direct")
    rest=' '.join(rest)
    channel.basic_publish(exchange='',routing_key=targ+"_queue",body=rest)

else:
    my_dict={}
    d={}
    for x in c.listaNodos:
        n='c.lista'+x
        my_dict[x]=n

    for x in eval(my_dict[targ]):
        channel.queue_declare(queue=x+"_queue",durable=True)
        message = ' '.join(sys.argv[2:])
        channel.basic_publish(exchange='',routing_key=x+"_queue",body=message)

print " [x] Sent "+ rest
connection.close()
