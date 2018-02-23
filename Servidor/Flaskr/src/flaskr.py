#! /usr/bin/env python

# all the imports
import servidorConf as sc
import threading
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
	 abort, render_template, flash, Response
from contextlib import closing
import serial
import subprocess
import os,sys
from functions import system
import json
import time
from tinydb import TinyDB, where,Query
import pika
import rabbitmq_listener
#Importamos el archivo de configuracion

sy=system()

mutex = threading.Lock()

def cola(sy):
        #Establecemos las credenciales
        credentials = pika.PlainCredentials(sc.RABBIT_USER, sc.RABBIT_PASSWD)
        #Establecemos la conexion al servidor a traves del puerto 5672
        connection = pika.BlockingConnection(pika.ConnectionParameters(sc.urlServer, 5672,'/',credentials))
        channel = connection.channel()
        #Declaramos La cola por la que recibiremos (Por si acaso no esta creada aun)
        channel.queue_declare(queue=sc.me, durable=True)
        #Declaramos las colas a las que enviaremos con emitter.py, por si acaso no estan declaradas aun
        for x in sc.list:
            channel.queue_declare(queue=x, durable=True)
        #Hacemos en binding de los exchanges con las colas, teniendo en cuenta el routing key
        for x,y in zip(sc.list,sc.severity):
            channel.exchange_declare(exchange=x,
                                    type='fanout')
            channel.queue_bind(exchange=x,
                               queue=sc.me,
                               routing_key=y)
        def callback(ch, method, properties, body):
                print(" [x] %r" % (body))
                if sy.follow:
                        if 'D' in body:
                                t = threading.Thread(target=sy.goto, args=(body,ser,))
                                t.start()
                                return

        channel.basic_consume(callback,
                                queue=sc.me,
                                no_ack=True)
        channel.start_consuming()
        print 'Receptor cola activado'

# configuration
DEBUG = False
SECRET_KEY = 'development key'

# Starting our application
app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
#Debug var
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = 'some_really_long_random_string_here'

task_id=len(sy.table)+1


logged= None
os.chdir('/home/cupula/CupulaCiclope/Servidor/Flaskr')
sy.empaquetar()

#Launching Camera server if sc.camera variable is active
if sc.camera==1:
	try:
		newPid2=os.fork()
		if newPid2==0:
			print "Launched camera server"
			sy.cameraServer()
			sys.exit()
		else:
			print newPid2
	except:
		print "Error launching the camera"
		sy.log("Error launching the camera")
#Launching Comunication with board if sc.boardPort is active
if sc.board==1:
	try:
		ser = serial.Serial(sc.boardPort, 9600,timeout=3)
                sy.ser=ser
		'''t=threading.Timer(2,sy.checkRoutine,args=(ser,))
		t.daemon=True
		t.start()'''
		#sy.checkRoutine(ser)
		print "Launched comunication with board"
	except:
		print "Error launching the board"
		sy.log("Error launching the board")
else:
	print 'Controller board variable is not activated'
        sy.log('Controller board variable is not activated')
t = threading.Thread(target=cola, args=(sy,))
t.start()


def process_message(message):
	if 'SZ' in message:
		sy.offset==sy.azimut
	elif 'followOn' in message:
		sy.follow=True
	elif 'followOff' in message:
		sy.follow=False
	elif 'H' in message:
		message='D'+str(sc.home)
		t = threading.Thread(target=sy.goto, args=(message,ser,))
 		t.start()
	elif 'D' in message:
		t = threading.Thread(target=sy.goto, args=(message,ser,))
		t.start()
                        
	elif 'ON' in message:
		sy.on=True
		sy._threadStopper_=threading.Event()
		sy._thread_=threading.Timer(2,sy.checkRoutine,args=(ser,))
		sy._thread_.daemon=True
			
			
		sy._thread_.start()
	elif 'OFF' in message:
		sy.on=False
		sy._threadStopper_.set()

	else:
		if logged in 'admin':
			try:
			t = threading.Thread(target=sy.send, args=(message,ser,))
			t.start()
			except:
				print "Error launching thread"

	return sy.task_json


@app.route('/api/cupula/montegancedo/task', methods=['POST'])
def task():
	error=None
	global logged
	print logged
	if ((logged != 'admin') and (logged !='guest')):
		abort(401)
        if request.method == 'POST':
                #cur = get_db().cursor()
                message=request.get_json()
                global task_id
                task_id=task_id+1
                sy.table.all()
                
		sy.table.insert({'id':task_id,'command':message,'time':time.strftime("%H:%M:%S"),'status':'non-completed'})
		
		sy.task_json=json.dumps({'id':task_id,'command':message['command'],'time':time.strftime("%H:%M:%S"), 'status':"non-completed"})
		#print sy.task_json
		message=str(message['command'])
		#print message
		mutex.acquire()
		return_value = process_message(message)
		mutex.release()
@app.route('/api/cupula/montegancedo/', methods=['GET'])
def status():
	response_json=json.dumps({'lat':"40 24 22 N"  ,'long':"3 50 19 O" , 'name':"Observatorio Montegancedo",'status':{'Azimut':sy.azimut,'Laps':sy.vueltas, 'Voltage': sy.voltage, 'Direction':sy.direction}})
	return response_json	
		
@app.route('/api/cupula/montegancedo/tasks/<int:iden>', methods=['GET'])
def returnTask(iden):
	s=Query()
	x=sy.table.get(s.id==iden)
	print x
	if x==None:
		abort(404)
	print x['id']
	sy.task_json=json.dumps({'id':x['id'],'command':x['command']['command'],'time':x['time'],'status':x['status']})
	return sy.task_json

@app.route('/login', methods=['GET', 'POST'])
def login():
        """global sc.USERNAME_ADMIN
        global sc.USERNAME_GUEST
        global sc.PASSWORD_GUEST
        global sc.PASSWORD_ADMIN"""
	error = None
	global logged
	if request.method == 'POST':
		"""if (request.form['username'] not in sc.USERNAME_ADMIN)and (request.form['username'] not in sc.USERNAME_GUEST):
			logged  = ''
                        sy._logged_=""
			error = 'Invalid username'
			print error
                        if (request.form['password'] != sc.PASSWORD_GUEST)and(request.form['password'] != sc.PASSWORD_ADMIN):
                                logged  = ''
                                sy._logged_=""
                                error = 'Invalid password'
                                print error
		else:
                        global logged
                        if request.form['username'] in sc.USERNAME_ADMIN:
                                logged  = 'admin'
                                sy._logged_="admin"
                        if request.form['username'] in sc.USERNAME_GUEST:
                                logged  = 'guest'
                                sy._logged_='guest'
			#session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('command'))"""
#		if (request.form['username'] in sc.USERNAME_ADMIN):
		if (request.form['username'] == sc.USERNAME_ADMIN):
#                        if (request.form['password'] in sc.PASSWORD_ADMIN):
                        if (request.form['password'] == sc.PASSWORD_ADMIN):
                                logged  = 'admin'
                                sy._logged_='admin'
#                elif (request.form['username'] in sc.USERNAME_GUEST):
                elif (request.form['username'] == sc.USERNAME_GUEST):
#                        if (request.form['password'] in sc.PASSWORD_GUEST):
                        if (request.form['password'] == sc.PASSWORD_GUEST):
                                logged  = 'guest'
                                sy._logged_='guest'
                else:
                        error="Invalid username or password"
                        print error
                        logged  = ''
                        sy._logged_=''
                print sy._logged_
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	global logged
	logged = None
	#session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))



#==================================================
#============= Parte del rabbitmq =================
#==================================================

def rmq_consume():
	def callback(severity,message):
		if severity == "info":
			mutex.acquire()
			process_message(message)
			mutex.release()
		else:
			print("Critico")
	t = rabbitmq_listener.rmq_listener(callback)
	t.start()

if __name__ == '__main__':
	print "////////////// Starting Cupula Ciclope's server//////////////"
	app.run(host='0.0.0.0',port=80)
