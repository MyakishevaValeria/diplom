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


class Machines(db.Model):
    id_machine = db.Column(db.Integer, primary_key=True)
    id_number = db.Column(db.Integer)
    date_manufacture = db.Column(db.String(50))
    name_factory = db.Column(db.String(50))
    lifetime = db.Column(db.Integer)
    owner = db.Column(db.String(50))
    date_start = db.Column(db.String(50))
    grade = db.Column(db.Float)
    status = db.Column(db.String(10))

    pr = db.relationship('Maintenance', cascade="all,delete", backref='machines', uselist=False)

    def __repr__(self):
        return f"<machines {self.id_machine}>"


class Maintenance(db.Model):
    id_maintenance = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10))
    date_maintenance = db.Column(db.String(50))
    grade_TO = db.Column(db.Float)
    repair = db.Column(db.Text)
    status_TO = db.Column(db.Text)

    id_machine = db.Column(db.Integer, db.ForeignKey('machines.id_machine'))

    d2 = db.relationship('Springs', cascade = "all,delete", backref='maintenance', uselist=False)
    d1 = db.relationship('Wheel', cascade = "all,delete", backref='maintenance', uselist=False)
    d3 = db.relationship('Dvs', cascade = "all,delete", backref='maintenance', uselist=False)
    d4 = db.relationship('Transmission', cascade = "all,delete", backref='maintenance', uselist=False)
    d5 = db.relationship('Pneumatics', cascade = "all,delete", backref='maintenance', uselist=False)
    d6 = db.relationship('Device', cascade = "all,delete", backref='maintenance', uselist=False)
    d7 = db.relationship('Brakes', cascade = "all,delete", backref='maintenance', uselist=False)

    def __repr__(self):
        return f"<maintenance {self.id_maintenance}>"


class Wheel(db.Model):
    id_wheel = db.Column(db.Integer, primary_key=True)
    first_across_rl = db.Column(db.Integer)
    first_across_rr = db.Column(db.Integer)
    first_across_ll = db.Column(db.Integer)
    first_across_lr = db.Column(db.Integer)
    second_across_rl = db.Column(db.Integer)
    second_across_rr = db.Column(db.Integer)
    second_across_ll = db.Column(db.Integer)
    second_across_lr = db.Column(db.Integer)
    first_lateral_r = db.Column(db.Integer)
    first_lateral_l = db.Column(db.Integer)
    second_lateral_r = db.Column(db.Integer)
    second_lateral_l = db.Column(db.Integer)
    grade_wheel = db.Column(db.Float)

    maintenance_id = db.Column(db.Integer, db.ForeignKey('maintenance.id_maintenance'))

    def __repr__(self):
        return f"<wheel {self.id_wheel}>"


class Springs(db.Model):
    id_spring = db.Column(db.Integer, primary_key=True)
    first_r_spring_H1 = db.Column(db.Integer)
    first_r_spring_H2 = db.Column(db.Integer)
    first_l_spring_H1 = db.Column(db.Integer)
    first_l_spring_H2 = db.Column(db.Integer)
    second_r_spring_H1 = db.Column(db.Integer)
    second_r_spring_H2 = db.Column(db.Integer)
    second_l_spring_H1 = db.Column(db.Integer)
    second_l_spring_H2 = db.Column(db.Integer)
    first_r_spring_m = db.Column(db.Integer)
    first_l_spring_m = db.Column(db.Integer)
    second_r_spring_m = db.Column(db.Integer)
    second_l_spring_m = db.Column(db.Integer)
    grade_spring = db.Column(db.Float)

    maintenance_id = db.Column(db.Integer, db.ForeignKey('maintenance.id_maintenance'))

    def __repr__(self):
        return f"<springs {self.id_spring}>"


class Dvs(db.Model):
    id_dvs = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    type_oil = db.Column(db.String(50))
    amount_oil = db.Column(db.Integer)
    pressure_oil = db.Column(db.Float)
    tension = db.Column(db.Float)
    voltage = db.Column(db.Float)
    grade_dvs = db.Column(db.Float)

    maintenance_id = db.Column(db.Integer, db.ForeignKey('maintenance.id_maintenance'))

    def __repr__(self):
        return f"<dvs {self.id_dvs}>"


class Transmission(db.Model):
    id_transmission = db.Column(db.Integer, primary_key=True)
    pressure_oil_p = db.Column(db.Float)
    pressure_oil_t = db.Column(db.Float)
    pressure_oil_s = db.Column(db.Float)
    grade_transmission = db.Column(db.Float)

    maintenance_id = db.Column(db.Integer, db.ForeignKey('maintenance.id_maintenance'))

    def __repr__(self):
        return f"<transmission {self.id_transmission}>"


class Pneumatics(db.Model):
    id_pneumatic = db.Column(db.Integer, primary_key=True)
    compressor = db.Column(db.Float)
    density_PM = db.Column(db.Float)
    density_TM = db.Column(db.Float)
    density_TC = db.Column(db.Float)
    filling_TC = db.Column(db.Float)
    time_TC = db.Column(db.Float)
    density_UR = db.Column(db.Float)
    time_TM = db.Column(db.Float)
    time_UP = db.Column(db.Float)
    reducer = db.Column(db.Float)
    pace_1 = db.Column(db.Float)
    pace_2 = db.Column(db.Float)
    pace_3 = db.Column(db.Float)
    EPK = db.Column(db.Float)
    grade_pneumatics = db.Column(db.Float)

    maintenance_id = db.Column(db.Integer, db.ForeignKey('maintenance.id_maintenance'))

    def __repr__(self):
        return f"<pneumatics {self.id_pneumatic}>"


class Device(db.Model):
    id_device = db.Column(db.Integer, primary_key=True)
    bel = db.Column(db.String(10))
    bil1 = db.Column(db.String(10))
    bil2 = db.Column(db.String(10))
    bkr = db.Column(db.String(10))
    dup = db.Column(db.String(10))
    grade_device = db.Column(db.Float)

    maintenance_id = db.Column(db.Integer, db.ForeignKey('maintenance.id_maintenance'))

    def __repr__(self):
        return f"<device {self.id_device}>"


class Brakes(db.Model):
    id_brakes = db.Column(db.Integer, primary_key=True)
    data_check = db.Column(db.String(50))
    depth = db.Column(db.Integer)
    rod = db.Column(db.Integer)
    grade_brake = db.Column(db.Float)

    maintenance_id = db.Column(db.Integer, db.ForeignKey('maintenance.id_maintenance'))

    def __repr__(self):
        return f"<brakes {self.id_brakes}>"







