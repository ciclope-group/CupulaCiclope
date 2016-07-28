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



sy=system()
# configuration
DEBUG = False
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
# Starting our application
app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
#Debug var
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = 'some_really_long_random_string_here'


#db=TinyDB('/home/cupula/CupulaCiclope/Servidor/Flaskr/flaskr/database.json')
#table=db.table('history')

task_id=len(sy.table)+1


logged= None
os.chdir('/home/cupula/CupulaCiclope/Servidor/Flaskr/flaskr')
sy.empaquetar()
#def initServer():
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
#Launching Comunication with board if sc.boardPort is active
if sc.board==1:
	try:
		ser = serial.Serial(sc.boardPort, 9600,timeout=3)
		t=threading.Timer(2,sy.checkRoutine,args=(ser,))
		t.daemon=True
		t.start()
		print "Launched comunication with board"
	except:
		print "Error launching the board"
else:
	print 'Controller board variable is not activated'



@app.route('/api/cupula/montegancedo/task', methods=['POST'])
def task():
	error=None
	"""global logged
	if not logged:
		abort(401)"""
	if request.method == 'POST':
		#cur = get_db().cursor()
		message=request.get_json()
		global task_id
		task_id=task_id+1
		sy.table.all()

		sy.table.insert({'id':task_id,'command':message,'time':time.strftime("%H:%M:%S"),'status':'non-completed'})
		
		sy.task_json=json.dumps({'id':task_id,'command':message['command'],'time':time.strftime("%H:%M:%S"), 'status':"non-completed"})
		print sy.task_json
		message=str(message['command'])
		print message
		if 'H' in message:
			message='D'+str(sc.home)
		if 'D' in message:
			print "Hay una D"
			t = threading.Thread(target=sy.goto, args=(message,ser,))
                        t.start()
			
		else:
			try:
				t = threading.Thread(target=sy.send, args=(message,ser,))
				t.start()
			except:
				print "no lanza proceso"
		#ser.write(message)
		return sy.task_json
@app.route('/api/cupula/montegancedo/', methods=['GET'])
def status():
	response_json=json.dumps({'lat':"40 24 22 N"  ,'long':"3 50 19 O" , 'name':"Observatorio Montegancedo",'status':{'Azimut':sy.azimut,'Laps':sy.vueltas, 'Voltage': sy.voltage, 'Direction':sy.direction}})
	return response_json	
		
@app.route('/api/cupula/montegancedo/tasks/<int:iden>', methods=['GET'])
def returnTask(iden):
	s=Query()
	print "Query si"
	x=sy.table.get(s.id==iden)
	print x
	if x==None:
		abort(404)
	print "Busqueda:"
	print x['id']
	sy.task_json=json.dumps({'id':x['id'],'command':x['command']['command'],'time':x['time'],'status':x['status']})
	return sy.task_json

@app.route('/status', methods=['GET'])
def status2():
	print "OK-NODE"
        return jsonify(tick='155')
@app.route('/rderecha', methods=['GET'])
def rderecha():
        error=None
	global logged
        if not logged:
                abort(401)
        if request.method == 'GET':
                print message
                #print 'Enviado'
                t.start()
                t = threading.Thread(target=sy.send, args=(ser,"R",))
                t.start()
                #ser.write(message)
        return str("OK")

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != USERNAME:
			str(request.form['username'])
			error = 'Invalid username'
		elif request.form['password'] != PASSWORD:
			error = 'Invalid password'
		else:
			global logged
			logged  = True
			#session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('command'))
	return render_template('login.html', error=error)

@app.route('/azimut', methods=['GET'])
def azimut():
	import servidorConf as sc
	return str(sc.acimut)
@app.route('/logout')
def logout():
	global logged
	logged = None
	#session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))
@app.route('/ticks')
def ticks():
        t="Ticks: " + str(sc.ticks)
        return t



if __name__ == '__main__':
	print "////////////// Starting Cupula Ciclope's server//////////////"
	#initServer()
	app.run(host='0.0.0.0',port=80)
