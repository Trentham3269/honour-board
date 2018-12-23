#!/usr/bin/python3
from flask import Flask, jsonify, send_file, send_from_directory
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask'
db = SQLAlchemy(app)


class Winners(db.Model):
    __tablename__ = 'winners'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10))
    first_name = db.Column(db.String(30))
    initials = db.Column(db.String(3))
    last_name = db.Column(db.String(30))

    def __repr__(self):
        return 'id: {0}, first name: {1}, last name: {2} |'.format(self.id, self.first_name, self.last_name)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'first_name': self.first_name,
            'initials': self.initials,
            'last_name': self.last_name,
        }


@app.route('/')
def index():
	return send_file('index.html')


@app.route('/static/<path:path>')
def assets(path):
    return send_from_directory('static', path)


@app.route('/api/winners')
def winners():
    winners = Winners.query.all()
    return jsonify([w.serialize() for w in winners])
	

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)