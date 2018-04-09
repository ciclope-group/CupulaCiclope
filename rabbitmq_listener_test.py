import rabbitmq_listener as r
import time
def callback(s,m):
    print("[Cola] %s"%m)

th = r.rmq_listener(callback)

th.start()


# mostrar algo para ver que sigue haciendo cosas
i=0
while True:
   try:
      print(i)
      time.sleep(2);
   except KeyboardInterrupt:
      exit(-1)
