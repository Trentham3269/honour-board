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
    wins = db.relationship('Competitions', backref='winners', lazy=True)

    def __repr__(self):
        return 'id: {0}, first name: {1}, last name: {2}, wins: {3}'.format(self.id, self.first_name, self.last_name, self.wins)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'first_name': self.first_name,
            'initials': self.initials,
            'last_name': self.last_name,
            'wins': ([w.serialize() for w in self.wins])
        }


class Competitions(db.Model):
    __tablename__ = 'competitions'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    location = db.Column(db.String(3))
    winner_id = db.Column(db.Integer, db.ForeignKey('winners.id'))
    
    def __repr__(self):
        return 'id: {0}, year: {1}, location: {2}, winner: {3}'.format(self.id, self.year, self.location, self.winner_id)

    def serialize(self):
        return {
            'id': self.id, 
            'year': self.year,
            'location': self.location,
            'winner': self.winner_id,
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


@app.route('/api/winner/<int:id>')
def winner(id):
    winner = Winners.query.filter_by(id=id).all()
    return jsonify([w.serialize() for w in winner])


@app.route('/api/competitions')
def competitions():
    competitions = Competitions.query.all()
    return jsonify([c.serialize() for c in competitions])
	

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)