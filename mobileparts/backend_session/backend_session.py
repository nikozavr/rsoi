from bottle import route, run, template, get, post, request, Bottle
import bottle
import bottle.ext.sqlite
import sqlite3
import json
from bottle import response
import logging
import redis
import hashlib
from datetime import datetime, timedelta

class User_session():
    id = None
    username = None
    password = None

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def as_json(self):
        return dict(id=self.id,
            username=self.username)

    def check_password(self, password):
        return True if self.password==password else False 


def create_session(user):
    now = datetime.utcnow().replace(tzinfo=utc)
    session_key = hashlib.sha224(user.login.encode('utf-8') + user.password.encode('utf-8') + now.strftime(settings.DATE_FORMAT).encode('utf-8')).hexdigest()
    while cache.get(session_key) != None:
        session_key = hashlib.sha224(user.login.encode('utf-8') + user.password.encode('utf-8') + now.strftime(settings.DATE_FORMAT).encode('utf-8')).hexdigest()
    session_key = ("%03d" % user.id) + session_key
    return session_key

@post('/create/session/')
def create_session():
    try:     
        username = request.json["username"]
        password = request.json["password"]
        db = sqlite3.connect('db_session_users.sqlite3')
        user_data = db.execute('SELECT * from users where username = ?', [username]).fetchone()
        db.close()
        if user_data:
            user = User_session(user_data[0], user_data[1], user_data[2])
            if check_password:
                session_key = ""
                if db_session.get(session_key) != None:  
                    db_session.delete(session_key)
                session_key = create_session(user)
                db_session.set(session_key, user.id) 
                json_data = json.dumps({"user_id": user.id, "session_key": session_key})
                return json_data
            else:
                response.status = 404
                return json.dumps({"error_description": "Error username or password"})
        else:
            response.status = 404
            return json.dumps({"error_description": "Error username or password"})
        return user
    except ValueError:
        response.status = 400
        return json.dumps({"error_description": "Error username or password"})

@post('/create/user/')
def create_user():
    try:
        username = request.json["username"]
        password = request.json["password"]
        db = sqlite3.connect('db_session_users.sqlite3')
        db.close("INSERT into users values (NULL, ?, ?)", [username, password])
        user_data = db.execute('SELECT * from users where username = ?', [username]).fetchone()
        db.close()
        if user_data:
            user = User_session(user_data[0], user_data[1], user_data[2])
            response.status = 200
            return json.dumps(user.as_json())
        else:
            response.status = 501
            return json.dumps({"error_description": "Error: User is not created"})
        return username
    except ValueError:
        response.status = 400
        return json.dumps({"error_description": "Error username or password"})

@post('/check/')
def check():
    try:
        session_key = request.json["session_key"]
        user_id = int(session_key[:3])
        s = db_session.get(session_key)
        if s == user_id:
            db = sqlite3.connect('db_session_users.sqlite3')
            user_data = db.execute('SELECT * from users where id = ?', [user_id]).fetchone()
            db.close()
            if user_data:
                response.status = 200
                return json.dumps({"info": "Session key is correct"})
            else:
                response.status = 401
                return json.dumps({"error_description": "Session key is not correct"})

        response.status = 401
        return json.dumps({"error_description": "Session key is not correct"})
    except ValueError:
        response.status = 400
        return json.dumps({"error_description": "Error username or password"})

"""
@get('/info/<no:int>')
def info(no):
    db = sqlite3.connect('db_session_users.sqlite3')
    data = db.execute('SELECT * from manufacturers where id = ?', [no]).fetchone()
    db.close()
    man = Manufacturer(data[0], data[1], data[2], data[3])
    return json.dumps(man.as_json_full())

@route('/show/')
def show():
    db = sqlite3.connect('db.sqlite3')
    data = db.execute('SELECT name from manufacturers_manufacturer').fetchall()
    db.close()
    if data:
        return template('showitem', rows=data)
    return HTTPError(404, "Page not found")
"""

if __name__ == "__main__":
    db_session = redis.StrictRedis(host='localhost', port=6379, db=0)

run(host='127.2.2.2', port=8080)