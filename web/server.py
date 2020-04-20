from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import json
import time

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)

@app.route('/espar/<numero>')
def espar(numero):
    return str( int(numero)%2 == 0)

@app.route('/esprimo/<numero>')
def esprimo(numero):
    if (int(numero) < 1):
        return str(False)
    elif numero == 2:
        return str(True)
    else:
        for i in range(2, int(numero)):
            if int(numero) % i == 0:
                return str(False)
        return str(True)

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

##TAREA
@app.route('/palindrome/<palabra>')
def espalindrome(palabra):
    palindromo = palabra[::-1]
    if palindromo==palabra:
        return str("Es un palindromo")
    else:
        return str("No es un palindromo")

@app.route('/multiplo/<num1>/<num2>')
def esmultiplo(num1,num2):
    if int(num1)%int(num2) == 0:
        return str("Si son multiplos")
    else:
        return str("No son multiplos")
#-----------------

if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
