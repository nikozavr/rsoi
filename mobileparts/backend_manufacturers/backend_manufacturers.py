from bottle import route, run, template, get, post, request
import bottle
import bottle.ext.sqlite
import sqlite3
import json
from bottle import response

class Manufacturer():
    id = None
    name = None
    established = None
    country = None
    info = None

    def __init__(self, id, name, year, country):
        self.id = id
        self.name = name
        self.established = year
        self.country = country

    def as_json(self):
        return dict(id=self.id,
        	name=self.name, 
            established =self.established,
            country=self.country)

    def as_json_full(self):
        return dict(id=self.id,
        	name=self.name, 
            established =self.established,
            country=self.country,
            info=self.info)


@get('/list/')
def list():
    mans = []
    db = sqlite3.connect('db_manufacturers.sqlite3')
    data = db.execute('SELECT * from manufacturers').fetchall()
    db.close()
    if data:
        for row in data:
           man = Manufacturer(row[0], row[1], row[2], row[3])
           mans.append(man)
        results = [ob.as_json() for ob in mans]
        result = {"count": len(data), "manufacturers":results}
        response.content_type = "application/json"
        return json.dumps(result)
    else:
        response.status = 404
        return json.dumps({"error_description": "No manufacturer found"})


@get('/info/<no:int>')
def info(no):
    db = sqlite3.connect('db_manufacturers.sqlite3')
    data = db.execute('SELECT * from manufacturers where id = ?', [no]).fetchone()
    db.close()
    if data:
        man = Manufacturer(data[0], data[1], data[2], data[3])
        return json.dumps(man.as_json_full())
    else:
        response.status = 404
        return json.dumps({"error_description": "No manufacturer found"})

@route('/show/')
def show():
    db = sqlite3.connect('db.sqlite3')
    data = db.execute('SELECT name from manufacturers_manufacturer').fetchall()
    
    if data:
        return template('showitem', rows=data)
    return HTTPError(404, "Page not found")

run(host='127.2.2.2', port=8080)