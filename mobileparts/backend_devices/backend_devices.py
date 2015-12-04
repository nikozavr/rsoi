from bottle import route, run, template, get, post, request
import bottle
import bottle.ext.sqlite
import sqlite3
import json
from bottle import response

class Device():
    id = None
    manufacturer_id = None
    model_name = None
    model_number = None
    prod_data = None
    char_id = None

    def __init__(self, id, manufacturer_id, model_name, model_number, prod_data, char_id):
        self.id = id
        self.manufacturer_id = manufacturer_id
        self.model_name = model_name
        self.model_number = model_number
        self.prod_data= prod_data
        self.char_id = char_id

    def as_json(self):
        return dict(id=self.id,
        	manufacturer_id=self.manufacturer_id, 
            model_name =self.model_name,
            model_number=self.model_number,
            prod_data=self.prod_data)

    def as_json_full(self):
        db = sqlite3.connect('db_devices.sqlite3')
        data = db.execute('SELECT * from characteristic where id = ?', [self.char_id]).fetchone()
        db.close()
        if data:
            dev_char = Device_Characteristics(data[0],data[1],data[2],data[3],data[4],data[5],data[6])
            d = self.as_json()
            d.update(dev_char.as_json())
            return d
        else:
            return self.as_json()
        
class Device_Characteristics():
    id = None
    device_type = None
    dig_disp = None
    resolution = None
    memory = None
    sd_card = None
    camera = None

    def __init__(self, id, device_type, dig_disp,resolution, memory, sd_card, camera):
        self.id = id
        self.device_type = device_type
        self.dig_disp = dig_disp
        self.resolution = resolution
        self.memory = memory 
        self.sd_card = sd_card
        self.camera = camera

    def as_json(self):
        return dict(device_type=self.device_type, 
            dig_disp =self.dig_disp,
            resolution=self.resolution,
            memory = self.memory, 
            sd_card = self.sd_card,
            camera = self.camera)

@get('/list/<no:int>')
def list(no):
    db = sqlite3.connect('db_devices.sqlite3')
    data = db.execute('SELECT * from devices where id = ?', [no]).fetchone()
    db.close()
    if data:
        device = Device(data[0],data[1],data[2],data[3],data[4],data[5])
        return json.dumps(man.as_json())
    else:
        response.status = 404
        return json.dumps({"error_description": "No device found"})

@get('/info/<no:int>')
def info(no):
    db = sqlite3.connect('db_devices.sqlite3')
    data = db.execute('SELECT * from devices where id = ?', [no]).fetchone()
    db.close()
    if data:
        device = Device(data[0],data[1],data[2],data[3],data[4],data[5])
        return json.dumps(man.as_json_full())
    else:
        response.status = 404
        return json.dumps({"error_description": "No device found"})

@get('/list/')
def list():
    db = sqlite3.connect('db_devices.sqlite3')
    data = db.execute('SELECT * from devices').fetchall()
    db.close()
    if data:
        device = Device(data[0],data[1],data[2],data[3],data[4],data[5])
        return json.dumps(man.as_json())
    else:
        response.status = 404
        return json.dumps({"error_description": "No device found"})


run(host='127.2.2.2', port=8080)