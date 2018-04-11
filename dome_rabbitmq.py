import rabbitmq_listener as rl
import json
import dome_communication_dummy as d


dome = d.Dome()

def callback(s,m):
    body = json.loads(m)
    if "azimuth" in body:
        dome.goto(body["azimuth"])

consumer = rl.rmq_listener(callback)
consumer.start()
while True:
    _=1
