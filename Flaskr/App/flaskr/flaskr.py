# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
	 abort, render_template, flash
from contextlib import closing
import serial

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
# create our little application :)
app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
ser = serial.Serial('/dev/ttyACM0', 9600)

	
@app.route('/command', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	if request.method == 'POST':
		
		message=request.form['comando']
		message = '&'+str(message)+'#'
		print message
		print 'Enviado'
		ser.write(message)
	
	return redirect(url_for('command'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('command'))
	return render_template('login.html', error=error)


@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))


if __name__ == '__main__':
	app.run()    