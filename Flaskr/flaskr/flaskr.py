# all the imports
import threading
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
	 abort, render_template, flash, Response
from contextlib import closing
import serial

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
ser = serial.Serial('/dev/ttyACM0', 9600)
logged= None
	
@app.route('/command', methods=['GET','POST'])
def command():
	error=None
	global logged
	if not logged:
		abort(401)
	if request.method == 'POST':
		message=request.form['command']
		message = '&'+str(message)+ '#'
		print message
		print 'Enviado'
		ser.write(message)
		#return redirect(url_for('command'))
	return render_template('command.html', error=error)	

@app.route('/camera', methods=['GET','POST'])
def camera():
	return render_template('camera.html')


def gen(camara):
	while True:
                frame = camara.get_frame()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')		
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
@app.route('/video_feed')
def video_feed():
	return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=4000)    
