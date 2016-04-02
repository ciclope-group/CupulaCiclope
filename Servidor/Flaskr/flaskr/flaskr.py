# all the imports
import threading
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
	 abort, render_template, flash, Response
from contextlib import closing
import serial
import subprocess

from camera import VideoCamera
# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
# create our little application :)
app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'some_really_long_random_string_here'
logged= None
ser = serial.Serial('/dev/ttyACM0', 9600)
def send(message,ser):
	message='&'+message+'#'
	ser.write(message)

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
		t = threading.Thread(target=send, args=(message,ser,))
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
