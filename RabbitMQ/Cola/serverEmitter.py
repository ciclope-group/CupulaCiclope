#!/usr/bin/env python
import pika
import sys
import config as c
#!/usr/bin/env python
import pika
import sys


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
targ=sys.argv[1]

my_dict={'meteor': c.listaMeteor,'cupula': c.listaCupula}
for x in my_dict[targ]:
    channel.queue_declare(queue=x+"_queue",durable=True)
    message = ' '.join(sys.argv[2:])
    channel.basic_publish(exchange='',routing_key=x+"_queue",body=message)

print " [x] Sent "+ message
connection.close()
