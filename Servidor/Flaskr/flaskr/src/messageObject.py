import os
import servidorConf as sc
import time
import threading
import subprocess
import shutil
import struct
mutex = threading.Lock()

class message:
	self.azimut=""
	self.message""
	self.response=""
	self.ser=""
	
	def __init__(self,ser, message):
		self.message=message
		self.ser=ser
	"""def logMessage(self):
		with open(sc.logDir, 'a') as file_:
                                file_.write(message+" Response: "+sArduino+" "+time.strftime("%H:%M:%S")+" "+ time.strftime("%d/%m/%Y") + "\n")
                                file_.close()"""
	def send(self):
		if self.message != 'G' and self.message != 'V':
                	self.response = "&#"
        	if self.message == 'G':
                	self.response=="&G"
	        if self.message == 'R' or self.message=='I' or self.message=='L':
        	        self.response="&#"
	        if 'D' == self.message[0]:
	                print "Entro"
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
                ser.write(self.message)
                print self.message
                t2 = threading.Timer(4, alarma)
                t2.daemon=True
                t2.start()
                #sArduino =str(ser.readline())
                time.sleep(1)
                sArduino=""
                while ser.inWaiting() > 0:
                        sArduino += ser.read(1)
                sArduino=str(sArduino)
                print sArduino
                if message == '&G#':
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
                        print "Tension: "+str(c2)
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
			self.azimut=d;
                        print "ticks: "+ str(d)
                        sc.acimut=(d*360)/190967
			print "Acimut: "+str(sc.acimut)
                        sc.ticks=d
