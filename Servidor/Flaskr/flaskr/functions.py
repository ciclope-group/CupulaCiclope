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
        os.system('./mjpg_streamer -i "./input_uvc.so -d /dev/video0 -r 320x240" -o "./output_http.so -w ./www" ')	
	#os.system('./mjpg_streamer -i "./input_uvc.so -d /dev/video0 -r 160x120 -y" -o "./output_http.so -w ./www"')
	#os.system('./mjpg_streamer -i "./input_uvc.so -r 320x240 -y" -o "./output_http.so -w ./www"')

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
		with open('log.txt', 'a') as file_:
    			file_.write(sArduino+" "+time.strftime("%H:%M:%S") + "\n")
			file_.close()
					
		t2.cancel()
	
def alarma():
	with open('log.txt', 'a') as file_:
        	file_.write("Alarma"+" "+time.strftime("%H:%M:%S") + "\n")
        	file_.close()
	
	


