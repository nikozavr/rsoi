from bottle import route, run, template, get, post, request
import bottle
import bottle.ext.sqlite
import sqlite3
import json
from bottle import response

class Review():
    id = None
    user_id = None
    part_id = None
    rating = None
    review = None

    def __init__(self, id, user_id, part_id, rating, review):
        self.id = id
        self.user_id = user_id
        self.part_id = part_id
        self.rating = rating
        self.review = review

    def as_json(self):
        return dict(id=self.id,
            user_id=self.user_id, 
            part_id=self.part_id,
            rating=self.rating,
             review=self.review)


@get('/list/device/<no:int>')
def list(no):
    reviews = []
    db = sqlite3.connect('db_reviews.sqlite3')
    data = db.execute('SELECT * from reviews where part_id = ?').fetchall()
    db.close()
    for row in data:
       rev = Review(row[4], row[3], row[2], row[0], row[1])
       reviews.append(rev)
    results = [ob.as_json() for ob in reviews]
    result = {"count": len(data), "reviews":results}
    response.content_type = "application/json"
    return json.dumps(result)

@get('/list/user/<no:int>')
def info(no):
    reviews = []
    db = sqlite3.connect('db_reviews.sqlite3')
    data = db.execute('SELECT * from reviews where user_id = ?').fetchall()
    db.close()
    for row in data:
       rev = Review(row[4], row[3], row[2], row[0], row[1])
       reviews.append(rev)
    results = [ob.as_json() for ob in reviews]
    result = {"count": len(data), "reviews":results}
    response.content_type = "application/json"
    return json.dumps(result)

@route('/show/')
def show():
    db = sqlite3.connect('db.sqlite3')
    data = db.execute('SELECT name from manufacturers_manufacturer').fetchall()

    if data:
        return template('showitem', rows=data)
    return HTTPError(404, "Page not found")

run(host='127.2.2.2', port=8080)