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
	ser.write("&G#")
	t2 = threading.Timer(0.5, alarma)
	t2.daemon=True
	t2.start()	
	sArduino =str(ser.readline())
	sArduino = sArduino[1:-3]
	if 'GLS' in sArduino:
		print sArduino
		t2.cancel()
	
	
def alarma():
	print "Alarma"
	


