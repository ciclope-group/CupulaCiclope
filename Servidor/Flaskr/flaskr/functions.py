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
	azimut=0
	direction=""
	voltage=""
	vueltas=-3
	objective=None
	nextObjective=None

	def empaquetar(self):
		tamLog = os.path.getsize(sc.logDir)
		print "Tamanio log "+ str(tamLog)
		if tamLog > 1000000:
			os.system('tar czvf log.tar.gz '+sc.logDir)
			print "Empaquetado"
			os.system('rm '+ sc.logDir)
	def goto(self,message,ser):
		if 'D' == message[0]:
	                s=int(message[1:])
	                if ((s-self.azimut)<180)or ((s-self.azimut)<-180):
				if self.vueltas<=1:
					self.send(message,ser)
				else:
					self.objective=(self.azimut+181)
					self.nextObjective=s
					print "Objetive: "+str(self.objective)+ "nextObjetive: "+str(self.nextObjective)
					self.send('D'+str(self.objective),ser)
			if ((s-self.azimut)>180)or (((s-self.azimut)>-180)and (s-self.azimut)< 0):
                                if self.vueltas>=-1:
                                        self.send(message,ser)
                                else:
                                        self.objective=(170-(360-self.azimut))
                                        self.nextObjective=s
                                        print "Objetive: "+str(self.objective)+ "nextObjetive: "+str(self.nextObjective)
                                        self.send('D'+str(self.objective),ser)

	def send(self,message,ser):
		if sc.board==1:
			self.mutex.acquire()
			x=messageObject(ser,message)
			x.send()
			self.mutex.release()
			if message == 'G':
				self.refreshStatus(x,ser)
			x.logMessage()
			del x


	def cameraServer(self):
		os.chdir(sc.mjpgDir)
	        print('Video streaming starting on pid ',  os.getpid())
	        os.system('./mjpg_streamer -i "./input_uvc.so -d /dev/video0 -r 320x240" -o "./output_http.so -w ./www" ')
		#os.system('./mjpg_streamer -i "./input_uvc.so -d /dev/video0 -r 160x120 -y" -o "./output_http.so -w ./www"')
		#os.system('./mjpg_streamer -i "./input_uvc.so -r 320x240 -y" -o "./output_http.so -w ./www"')
	def refreshStatus(self,x,ser):
		self.voltage=x.voltage
		if ((int(x.azimut)-int(self.azimut))>0) or ((int(x.azimut)-int(self.azimut))<-300) :
			self.direction = 1
		elif ((int(x.azimut)-int(self.azimut))<0) or ((int(x.azimut)-int(self.azimut))>300):
			self.direction = -1
		elif (int(x.azimut)-int(self.azimut))== 0 :
			self.direction = 0
		if ((int(self.azimut)>=0 and  (int(self.azimut)<20) and int(x.azimut)>330)):
			self.vueltas=self.vueltas-2
		if (int(self.azimut)>330 and (int(x.azimut)>=0 and int(x.azimut)<20) ):
			self.vueltas=self.vueltas+2
		if self.nextObjective!=None:
			if ((self.objective-x.azimut)<=2)and((self.objective-x.azimut)>=-2):
				self.send('D'+str(self.nextObjective),ser)
				self.objective=None
				self.nextObjective=None
		print "Vueltas: "+ str(self.vueltas)		
		self.azimut=x.azimut
		print "Direccion: " + str(self.direction)
	def checkRoutine(self,ser):
		self.send('G',ser)
		t = threading.Timer(1.0, self.checkRoutine, [ser])
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
