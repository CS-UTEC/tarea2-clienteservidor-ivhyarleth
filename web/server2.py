from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import json
import time

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

#CRUD users
#1. create

@app.route('/users', methods=['POST'])
def create_user():
    body = json.loads(request.data)
    user = entities.User(
        username = body['username'],
        name = body['name'],
        fullname = body['fullname'],
        password = body['password']
    )
#2. Create user objet

    db_session = db.getSession(engine)
    db_session.add(user)
    db_session.commit()
#3 Response client

    message = {'msg':'User Created!'}
    json_message = json.dumps(message, cls= connector.AlchemyEncoder)
    res = Response(json_message, status=201, mimetype='appication/json')
    return res

@app.route('/users', methods = ['GET'])
def read_users():
    #1. Consultar todos los usuarios
    db_session = db.getSession(engine)
    response = db_session.query(entities.User)
    #2 Convertor los usuarios a JSON
    users = response[:]
    json_message = json.dumps(users , cls=connector.AlchemyEncoder)
    #3 Responder al cliente
    return Response(json_message, status=200, mimetype='appication/json')



if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
