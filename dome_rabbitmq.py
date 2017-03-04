import rabbitmq_listener as rl
import rabbitmq_device as rd #TODO hacer sender separado
import json
import dome_communication as d
import time

def send_status(dome,sender):
    status = dome.get_status()
    sender.send_message("info",json.dumps(status))


dome = d.Dome()

def callback(s,m):
    body = json.loads(m)
    if "azimuth" in body:
        print(type(body["azimuth"]))
        dome.goto(body["azimuth"])
sender = rd.RabbitMQ_sender("cupula",server_ip="192.168.1.5")
consumer = rl.rmq_listener(callback)

consumer.start()
while True:
    send_status(dome,sender)
    time.sleep(20)
