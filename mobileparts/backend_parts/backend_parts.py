from bottle import route, run, template, get, post, request
import bottle
import bottle.ext.sqlite
import sqlite3
import json
from bottle import response

class Part():
    id = None
    device_id = None
    part = None
    part_number = None
    manufacturer_id = None
    type = None
    rating = None
    info = None

    def __init__(self, id, device_id, part, part_number, manufacturer_id, type, rating, info):
        self.id = id
        self.device_id = device_id
        self.part = part
        self.part_number = part_number
        self.manufacturer_id = manufacturer_id
        self.type = type
        self.rating = rating
        self.info = info

    def as_json(self):
        return dict(id=self.id,
            device_id=self.device_id,
        	part=self.part, 
            part_number =self.part_number,
            manufacturer_id=self.manufacturer_id,
            type=self.type,
            rating=self.rating,
            info=self.info)



@get('/list/')
def list():
    parts = []
    db = sqlite3.connect('db_parts.sqlite3')
    data = db.execute('SELECT * from parts').fetchall()
    db.close()
    for row in data:
       part = Part(row[1], row[2], row[3], row[0], row[4], row[5], row[6], row[7])
       parts.append(part)
    results = [ob.as_json() for ob in parts]
    result = {"count": len(data), "parts":results}
    response.content_type = "application/json"
    return json.dumps(result)

@get('/info/<no:int>')
def info(no):
    db = sqlite3.connect('db_parts.sqlite3')
    row = db.execute('SELECT * from parts where id = ?', [no]).fetchone()
    db.close()
    part = Part(row[1], row[2], row[3], row[0], row[4], row[5], row[6], row[7])
    return json.dumps(part.as_json())

@route('/show/')
def show():
    db = sqlite3.connect('db_parts.sqlite3')
    data = db.execute('SELECT name from manufacturers').fetchall()

    if data:
        return template('showitem', rows=data)
    return HTTPError(404, "Page not found")

run(host='0.0.0.0', port=80)