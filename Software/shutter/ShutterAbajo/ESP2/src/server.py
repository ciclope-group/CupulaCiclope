from flask import Flask
app = Flask(__name__)

@app.route('/Parar')
def hello_world():
    print "Hola"
    return 'Hola amigos de Geeky Theory!'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
