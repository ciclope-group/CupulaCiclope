#! /usr/bin/env python

# all the imports
import servidorConf as sc
import threading
from flask import Flask, request, session, g, redirect, url_for, \
	 abort, render_template, flash, Response
from contextlib import closing
import serial
import subprocess
import os,sys
from functions import system

sy=system()
# configuration
DATABASE = '/tmp/flaskr.db'
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



@app.route('/command', methods=['GET','POST'])
def command():
	error=None
	global logged
	if not logged:
		abort(401)
	if request.method == 'POST':
		message=request.form['command']
		print message
		#print 'Enviado'
		if 'D' in message:
			t = threading.Thread(target=sy.goto, args=(message,ser,))
                        t.start()
		else:
			t = threading.Thread(target=sy.send, args=(message,ser,))
			t.start()
		#ser.write(message)
	return render_template('command.html', error=error)

@app.route('/status', methods=['GET'])
def status():
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