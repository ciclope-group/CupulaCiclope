#/bin/env python
# coding:utf-8

import rabbitmq_device as rmq

import threading

class rmq_listener(threading.Thread):
# Escuchar a la montura
    def __init__(self,callback):
        self.callback = callback
        super().__init__() 
    def run(self):
        subscription = rmq.Subscription("montura:info")

        l = rmq.RabbitMQ_receiver(subscription,self.callback,ip_server="localhost")

        l.start_consuming()

