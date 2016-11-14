import os
import servidorConf as sc
import time
import threading
import subprocess
import shutil
import struct
from messageObject import messageObject
from tinydb import TinyDB, where,Query
import json
class system:
        _logged_=""
        _threadStopper_=""
        _thread_=""
	task_json=""
	mutex = threading.Lock()
	direction=""
	azimut=0
	offset=0
	direction=""
	voltage=""
	vueltas=1
	objective=None
	nextObjective=None
	on=False
	follow=False
	ser=""
	db=TinyDB('/home/cupula/CupulaCiclope/Servidor/Flaskr/flaskr/database.json')
	table=db.table('history')


	def empaquetar(self):
		tamLog = os.path.getsize(sc.logDir)
		print "Tamanio log "+ str(tamLog)
		if tamLog > 10000000:
			os.system('tar czvf log.tar.gz '+sc.logDir)
			print "Empaquetado"
			os.system('rm '+ sc.logDir)
	def goto(self,message,ser):
		if 'D' == str(message[0]):
	               	''' s=int(message[1:])
	                if ((s-self.azimut)<180)or ((s-self.azimut)<-180):
				if self.vueltas<=1:
					self.send(message,ser)
					self.objective=s
				else:
					self.objective=(self.azimut+181)
					self.nextObjective=s
					print "Objetive: "+str(self.objective)+ "nextObjetive: "+str(self.nextObjective)
					self.send('D'+str(self.objective),ser)
			if ((s-self.azimut)>180)or (((s-self.azimut)>-180)and (s-self.azimut)< 0):
                                if self.vueltas>=-1:
                                        self.send(message,ser)
					self.objective=s
                                else:
                                        self.objective=(170-(360-self.azimut))
                                        self.nextObjective=s
                                        print "Objetive: "+str(self.objective)+ "nextObjetive: "+str(self.nextObjective)
                                        self.send('D'+str(self.objective),ser)'''
			   
			s=int(message[1:])
			if s<5:
				print "S:" +str(s)
				s=5
				message='D5'
                                self.objective=s
                        if s>355:
				print "S:" +str(s)
				s=355
				message='D355'
                                self.objective=s
			if (s>=5 and s<=355):
				if (s>self.azimut):
					if (self.azimut-s<=-179):
						print "Going in 2 steps CW"	
						self.objective=(self.azimut+179)
                                        	self.nextObjective=s
                                        	print "Objetive: "+str(self.objective)+ "nextObjetive: "+str(self.nextObjective)
                                        	self.send('D'+str(self.objective+self.offset),ser)
					else:	
						print "Going in 1 step CW"
						self.objective=s
						self.send('D'+str(self.objective+self.offset),ser)
                		if (s<self.azimut):
                                        if ((self.azimut-s)>=179):
						print "Going in 2 steps CCW"
                                                self.objective=(self.azimut-179)
                                                self.nextObjective=s
                                                print "Objetive: "+str(self.objective)+ "nextObjetive: "+str(self.nextObjective)
                                                self.send('D'+str(self.objective+self.offset),ser)
                                        else:
                                                self.objective=s
                                                self.send('D'+str(self.objective+self.offset),ser)
                                                print "Going in 1 step CCW"
                                                
				                   

	def send(self,message,ser):
		if sc.board==1:
                        if (self._logged_ in 'admin') or (self._logged_ in 'guest'):
                                if self.on==True:
                                        self.log("Sended "+message)
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
		if x.azimut<self.offset:
                        aux=1
                else:
                        aux=0
		x.azimut=x.azimut-self.offset
		if ((int(x.azimut)-int(self.azimut))>0) or ((int(x.azimut)-int(self.azimut))<-300) :
			self.direction = 1
		elif ((int(x.azimut)-int(self.azimut))<0) or ((int(x.azimut)-int(self.azimut))>300):
			self.direction = -1
		elif (int(x.azimut)-int(self.azimut))== 0 :
			self.direction = 0
		'''if ((int(self.azimut)>=0 and  (int(self.azimut)<20) and int(x.azimut)>330)):
			self.vueltas=self.vueltas-2
		if (int(self.azimut)>330 and (int(x.azimut)>=0 and int(x.azimut)<20) ):
			self.vueltas=self.vueltas+2'''
		print "Objetive: "+str(self.objective)+ "nextObjetive: "+str(self.nextObjective)
		if self.nextObjective==None:	
			if self.objective!=None and self.objective!=x.azimut:		
                		if ((self.objective-x.azimut)<=2)and((self.objective-x.azimut)>=-2):
					print "Completo 1"
        	                	component=Query()
					data=json.loads(self.task_json)
					print data
					try:
	                        		self.table.update({'status':'completed'},component.id==int(data['id']))
					except:
						print "Cant update table"
						self.log("Cant update table")
					self.Objective=None
		if self.nextObjective!=None:
			if ((self.objective-x.azimut)<=2)and((self.objective-x.azimut)>=-2):
				self.send('D'+str(self.nextObjective+self.offset),ser)
				self.objective=self.nextObjective
				self.nextObjective=None
									
                print "Vueltas: "+ str(self.vueltas)
                if aux:
                        x.azimut=360+x.azimut        
		self.azimut=x.azimut
		print "Direccion: " + str(self.direction)
	def checkRoutine(self,ser):
            while (not self._threadStopper_.isSet()):
		self.send('G',ser)
                time.sleep(1)
		'''t = threading.Timer(1.0, self.checkRoutine, [ser])
		t.daemon = True
		t.start()'''




	def test(self,ser):
		ser.write("&G#")
		t2 = threading.Timer(0.5, alarma,args=(ser,))
		t2.daemon=True
		t2.start()
		sArduino =str(ser.readline())
		sArduino = sArduino[1:-3]
		if 'GLS' in sArduino:
			self.log(sArduino)
                        t2.cancel()

	def alarma(self,):
		print "Alarma"
		self.senf("I",ser)
		self.log("Alarma")
	def log(selg, message):
                with open(sc.logDir, 'a') as file_:
	        	file_.write(message+" "+time.strftime("%H:%M:%S") + "\n")
	        	file_.close()
