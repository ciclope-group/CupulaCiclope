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
import functions as f


print "////////////// Starting Cupula Ciclope's server //////////////"		

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

#Launching Camera server if sc.camera variable is active
if sc.camera==1:
	newPid2=os.fork()	
	if newPid2==0:
		print "Launched camera server"
        f.cameraServer()
        sys.exit()

#Launching Comunication with board if sc.boardPort is active                
if sc.board==1:
	ser = serial.Serial(sc.boardPort, 9600,timeout=3)
	t=threading.Timer(2,f.checkRoutine,args=(ser,))
	t.daemon=True
	t.start()
	print "Launched comunication with board"

	
	"""newPid2=os.fork()
	if newPid2==0:
                f.checkRoutine(ser)
                sys.exit()"""
	
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
		t = threading.Thread(target=f.send, args=(message,ser,))
    	t.start()
		#ser.write(message)
	return render_template('command.html', error=error)	

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


@app.route('/logout')
def logout():
	global logged 
	logged = None
	#session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))
  

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=4000)
	    
