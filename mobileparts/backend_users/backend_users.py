from bottle import route, run, template, get, post, request
import bottle
import bottle.ext.sqlite
import sqlite3
import json
from bottle import response

class User():
    id = None
    first_name = None
    second_name = None
    email = None
    phone = None

    def __init__(self, id, first_name, second_name, email, phone):
        self.id = id
        self.first_name = first_name
        self.second_name = second_name
        self.email = email
        self.phone = phone

    def __init__(self, id, first_name, second_name):
        self.id = id
        self.first_name = first_name
        self.second_name = second_name   

    def as_json(self):
        return dict(id=self.id,
        	first_name=self.first_name, 
            second_name=self.second_name)

    def as_json_full(self):
        return dict(id=self.id,
        	first_name=self.first_name, 
            second_name=self.second_name,
            email=self.email,
            phone=self.phone)


@get('/list/')
def list():
    mans = []
    db = sqlite3.connect('db.sqlite3')
    data = db.execute('SELECT * from manufacturers').fetchall()
    db.close()
    for row in data:
       man = Manufacturer(row[0], row[1], row[2], row[3])
       mans.append(man)
    results = [ob.as_json() for ob in mans]
    result = {"count": len(data), "manufacturers":results}
    response.content_type = "application/json"
    return json.dumps(result)

@get('/info/<no:int>')
def info(no):
    db = sqlite3.connect('db_users.sqlite3')
    data = db.execute('SELECT id,first_name,second_name from users where id = ?', [no]).fetchone()
    if data:
        user = User(data[0], data[1], data[2])
        return json.dumps(man.as_json())
    else:
        response.status = 404
        return json.dumps({"error_description": "No user found"})

@get('/info/all/<no:int>')
def info(no):
    db = sqlite3.connect('db_users.sqlite3')
    data = db.execute('SELECT * from users where id = ?', [no]).fetchone()
    if data:
        user = User(data[0], data[1], data[2], data[3], data[4], data[5])
        return json.dumps(man.as_json_full())
    else:
        response.status = 404
        return json.dumps({"error_description": "No user found"})

@post('/create/')
def create():
    first_name = request.json["first_name"]
    second_name = request.json["second_name"]
    email = request.json["email"]
    phone = request.json["phone"]

run(host='127.2.2.2', port=8080)