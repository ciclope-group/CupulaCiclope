import os
import servidorConf as sc
import time
import threading
import subprocess
import shutil
import struct

class messageObject():
	azimut=""
	message=""
	response=""
	ser=""
	sArduino=""
	voltage=""
	def __init__(self,ser, message=None):
		if message is None:
			self.ser=ser
		else:
			self.ser=ser
			self.message=message
	def logMessage(self):
		with open(sc.logDir, 'a') as file_:
			 file_.write(self.message+" Response: "+self.sArduino+" Azimut: "+str(self.azimut) +" Voltage: "+self.voltage + " at "+time.strftime("%H:%M:%S")+" "+ time.strftime("%d/%m/%Y") + "\n")
                         file_.close()
	def alarma(self):
		print "Alarma"
	def getStatus(self):
		self.message="G"
		self.send()


	def send(self,mess=None):
		if self.message != 'G' and self.message != 'V':
                	self.response = "&#"
        	if self.message == 'G':
                	self.response=="&G"
	        if 'D' == self.message[0]:
	                s=int(self.message[1:])
	                s=190967*s/360
	                print s
	                #message=message
	                s=hex(s)
	                s=str(s)
	                s=s[2:]
	                s=s.upper()
	                while len(s)<5:
	                        s="0"+s[0:]
	                chrmap = {'A': '\x3a', 'B': '\x3b', 'C': '\x3c', 'D': '\x3d', 'E': '\x3e', 'F': '\x3f'}
	                s=''.join(chrmap.get(c, c) for c in s)
	                self.message='Z'+s

	                '''message[1]=hex(ord(message[1])+48)[2:]
	                message[2]=hex(ord(message[2])+48)[2:]
	                message[3]=hex(ord(message[3])+48)[2:]
	                message[4]=hex(ord(message[4])+48)[2:]
	                message[5]=hex(ord(message[4])+48)[2:]'''

	                print self.message
		self.message='&'+self.message+'#'
            	self.ser.write(self.message)
	        print self.message
	        t2 = threading.Timer(4, self.alarma)
        	t2.daemon=True
	        t2.start()
    		#sArduino =str(ser.readline())
            	time.sleep(1)
            	sArduino=""
           	while self.ser.inWaiting() > 0:
                	sArduino += self.ser.read(1)
            	sArduino=str(sArduino)
            	print sArduino
		self.sArduino=sArduino
		if self.response in sArduino:
			t2.cancel()
            	if self.message == '&G#':
                	var=bin(ord(sArduino[10] ))[2:].zfill(8)
                	print "A: " + str(var)
                	var=bin(ord(sArduino[11] ))[2:].zfill(8)
	                print "B: " + str(var)
	                a2=sArduino[10]
	                a2=ord(a2)-int('80',16)
	                a2=format(a2, '08b')
        	        a2=a2[1:]
                 	b2=sArduino[11]
                	b2=ord(b2)-int('80',16)
	                b2=format(b2, '08b')
	                b2=b2[1:]
        	        c2=a2+b2
                	c2=(int(c2,2)*15)/1024
			self.voltage=str(c2)
                	print "Tension: "+self.voltage
	                var=bytes(sArduino[2:5])
	                #var=var.decode('utf-16')
  	                var=bin(ord(sArduino[2] ))[2:].zfill(8)
	                #print "A: " + str(var)
	                var=bin(ord(sArduino[3] ))[2:].zfill(8)
	                #print "B: " + str(var)
	                var=bin(ord(sArduino[4] ))[2:].zfill(8)
	                #print "C: " + str(var)
        	        a=sArduino[4]
			#print "Ord A: "  + str(ord(a))
            		#a=int(a,16:)-int('80',16)
                	a=ord(a)-int('80',16)
        	        #a=struct.unpack("h", str(a))[0]- struct.unpack('h', '80')[0]
	                a=format(a, '08b')
            		a=a[1:]
	                b=sArduino[5]
	                b=ord(b)-int('80',16)
	                b=format(b, '08b')
	                b=b[1:]
	                c=sArduino[6]
	                c=ord(c)-int('80',16)
	                c=format(c, '08b')
	                c=c[1:]
	                d=a+b+c
	                d=int(d,2)
			self.azimut=(d*360)/sc.totalticks

                    	print "ticks: "+ str(d)
                    	sc.acimut=(d*360)/sc.totalticks
			print "Acimut: "+str(sc.acimut)
        	        sc.ticks=d
