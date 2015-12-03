from bottle import route, run, template, get, post, request
import bottle
import bottle.ext.sqlite
import sqlite3
import json
from bottle import response


@post('/create/')
def create():
    data = request.body
    data1 = json.loads(data.decode('utf8'))
#    print("Ok")
    login = data["login"]
#    login = request.json["login"]
    return login

@get('/info/<no:int>')
def info(no):
    db = sqlite3.connect('db.sqlite3')
    data = db.execute('SELECT * from manufacturers where id = ?', [no]).fetchone()
    man = Manufacturer(data[0], data[1], data[2], data[3])
    return json.dumps(man.as_json_full())

@route('/show/')
def show():
    db = sqlite3.connect('db.sqlite3')
    data = db.execute('SELECT name from manufacturers_manufacturer').fetchall()

    if data:
        return template('showitem', rows=data)
    return HTTPError(404, "Page not found")

run(host='127.2.2.2', port=8080)