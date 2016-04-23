# all the imports
import servidorConf
import threading
from flask import Flask, request, session, g, redirect, url_for, \
	 abort, render_template, flash, Response
from contextlib import closing
import serial
import subprocess
import os,sys
import functions as f
		
# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = False
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
# create our little application :)
app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = 'some_really_long_random_string_here'
logged= None

if servidorConf.camera==1:
	print "Camara activa"
	newPid2=os.fork()	
	if newPid2==0:
                f.cameraServer()
                sys.exit()
if servidorConf.board==1:
	ser = serial.Serial('/dev/ttyACM0', 9600)
	t=threading.Thread(target=f.checkRoutine,args=(ser,))
	t.start()

	
	"""newPid2=os.fork()
	if newPid2==0:
                f.checkRoutine(ser)
                sys.exit()"""
	
else:	
	print 'Controller board is not activated'


print "Prueba"
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
	    
