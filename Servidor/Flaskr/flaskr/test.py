from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/cupula/CupulaCiclope/Servidor/Flaskr/flaskr/flaskr.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.String(80), unique=True)
    time = db.Column(db.String(120), unique=True)

    def __init__(self, command,id,time):
        self.command = command
        self.id = id
	self.time=time

    def __repr__(self):
        return '<User %r>' % self.command
