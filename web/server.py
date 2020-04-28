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
#---------------------------
#CRUD USER
@app.route('/create_users/<uname>/<ufullname>/<upassword>/<uusername>')
def create_users(uname,ufullname,upassword,uusername):
    user = entities.User(
        name = uname,
        fullname = ufullname,
        password = upassword,
        username = uusername
    )

    #Persistir objeto
    db_session = db.getSession(engine)
    db_session.add(user)
    db_session.commit()

    return("User created")

@app.route('/read_users')
def read_users():
    db_session = db.getSession(engine)
    respuesta = db_session.query(entities.User)
    users = respuesta[:]

    mostrar = '<table> <tr> <th> Nombre </th><th> Apellido </th><th> Usuario </th><th> Contraseña </th> </tr>'

    for i in range(len(users)):
        usuarios = '<tr><td>'+str(users[i].name)+'</td><td>'+str(users[i].fullname)+'</td><td>'+str(users[i].username)+'</td><td>'+str(users[i].password)+'</td></tr>'
        mostrar = mostrar + usuarios
    mostrar = mostrar + '</table>'

    return "All users read!" + mostrar

if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
