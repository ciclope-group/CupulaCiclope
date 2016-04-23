import os
import servidorConf
import time
import threading
import subprocess
def send(message,ser):
	if servidorConf.board==1:
		message='&'+message+'#'
		ser.write(message)


def cameraServer():
	os.chdir("/home/trex/TFG/CupulaCiclope/Servidor/mjpg/mjpg-streamer/")
        print('Video streaming starting on pid',  os.getpid())
        os.system('./mjpg_streamer -i "./input_uvc.so -d /dev/video0" -o "./output_http.so -w ./www" ')	

def checkRoutine(ser):
	test(ser)
	t = threading.Timer(5.0, checkRoutine, [ser])
	t.daemon = True
        t.start()
        
	

def test(ser):     
	ser.write('&R#')
	time.sleep(5)
	ser.write('&I#')
	


