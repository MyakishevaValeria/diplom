from flask_login import UserMixin

from sweater import db, manager
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class To(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    type_TO = db.Column(db.String(50), nullable=False)
    date_TO = db.Column(db.DateTime, default=datetime.utcnow)
    grade = db.Column(db.Float)
    repair = db.Column(db.Text)

    tr = db.relationship('Transmission', backref='to', uselist=False)
    dvs = db.relationship('Dvs', backref='to', uselist=False)

    def __repr__(self):
        return f"<to {self.id}>"


class Transmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pressure1 = db.Column(db.Float)
    pressure2 = db.Column(db.Float)
    pressure3 = db.Column(db.Float)
    mark_transmission = db.Column(db.Integer)

    machine_id = db.Column(db.Integer, db.ForeignKey('to.id'))

    def __repr__(self):
        return f"<transmission {self.id}>"


class Dvs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pressure_dvs = db.Column(db.Float)
    hours = db.Column(db.Integer)
    mark_dvs = db.Column(db.Integer)

    machine1_id = db.Column(db.Integer, db.ForeignKey('to.id'))

    def __repr__(self):
        return f"<dvs {self.id}>"