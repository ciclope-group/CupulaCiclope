import os
import servidorConf as sc
import time
import threading
import subprocess
import shutil
import struct
from messageObject import messageObject


class system:
	mutex = threading.Lock()
	direction=""
	azimut=""
	direction=""
	voltage=""

	def empaquetar(self):
		tamLog = os.path.getsize(sc.logDir)
		print "Tamanio log "+ str(tamLog)
		if tamLog > 1000000:
			os.system('tar czvf log.tar.gz '+sc.logDir)
			print "Empaquetado"
			os.system('rm '+ sc.logDir)

	def send(self,message,ser):

		if sc.board==1:
			self.mutex.acquire()
			x=messageObject(ser,message)
			x.send()
			self.mutex.release()
			if message == 'G':
				self.refreshStatus(x)
			x.logMessage()
			del x


	def cameraServer(self):
		os.chdir(sc.mjpgDir)
	        print('Video streaming starting on pid ',  os.getpid())
	        os.system('./mjpg_streamer -i "./input_uvc.so -d /dev/video0 -r 320x240" -o "./output_http.so -w ./www" ')
		#os.system('./mjpg_streamer -i "./input_uvc.so -d /dev/video0 -r 160x120 -y" -o "./output_http.so -w ./www"')
		#os.system('./mjpg_streamer -i "./input_uvc.so -r 320x240 -y" -o "./output_http.so -w ./www"')
	def refreshStatus(self,x):
		self.voltage=x.voltage
		if ((x.azimut-self.azimut)>0) or ((x.azimut-self.azimut)<-300) :
			self.direction = 1
		else if	if ((x.azimut-self.azimut)<0) or ((x.azimut-self.azimut)>300)
			self.direction = -1
		self.azimut=x.azimut
		print "Direccion: " + str(self.direction)
	def checkRoutine(self,ser):
		self.send('G',ser)
		t = threading.Timer(1.0, checkRoutine, [ser])S
		t.daemon = True
		t.start()




	def test(self,ser):
		ser.write("&G#")
		t2 = threading.Timer(0.5, alarma)
		t2.daemon=True
		t2.start()
		sArduino =str(ser.readline())
		sArduino = sArduino[1:-3]
		if 'GLS' in sArduino:
			with open(sc.logDir, 'a') as file_:
	    			file_.write(sArduino+" "+time.strftime("%H:%M:%S") + "\n")
				file_.close()

			t2.cancel()

	def alarma(self,):
		print "Alarma"
		with open(sc.logDir, 'a') as file_:
	        	file_.write("Alarma"+" "+time.strftime("%H:%M:%S") + "\n")
	        	file_.close()
