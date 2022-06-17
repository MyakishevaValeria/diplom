import compare
from sweater.models import User, Machines, Maintenance, Transmission, Dvs, Wheel, Springs, Device, Brakes, Pneumatics
from sweater import app, db

class Train(object):
    id_m: int
    wheels: [int]
    springs: [int]
    dvs: []
    transmission: [float]
    pneumatics: [float]
    device: [str]
    brake: [int]
    markM: float
    repair: str
    type_oil: str
    data_check: str
    type: str
    date_maintenance: str
    info: []

    def __init__(self, id_m, info, wheels, springs, dvs, transmission, pneumatics, device, brake, type_oil, data_check, type, date_maintenance):
        self.id_m = id_m
        self.info = info
        self.wheels = wheels
        self.springs = springs
        self.dvs = dvs
        self.transmission = transmission
        self.pneumatics = pneumatics
        self.device = device
        self.brake = brake
        self.type_oil = type_oil
        self.data_check = data_check
        self.type = type
        self.date_maintenance = date_maintenance
        self.maintenance = compare.Train_maintenance()

    def make_maintenance(self):
        # все методы тех обслуживания
        self.maintenance.grade_wheels(self.wheels)
        self.maintenance.grade_springs(self.springs)
        self.maintenance.grade_dvs(self.dvs)
        self.maintenance.grade_transmissions(self.transmission)
        self.maintenance.grade_pneumatics(self.pneumatics)
        self.maintenance.grade_device(self.device)
        self.maintenance.grade_brake(self.brake)
        self.markM = self.maintenance.complete_grade()
        self.maintenance.statusM()
        self.maintenance.safeMaintenance(self.wheels, self.springs, self.dvs, self.transmission,self.pneumatics,
                                                     self.device, self.brake, self.type_oil,
                                                     self.data_check, self.type, self.date_maintenance, self.id_m)
        self.maintenance.change(self.info)


    @staticmethod
    def create_train(data: []):
        try:
            m = Machines(id_number=data[0], date_manufacture=data[1], name_factory=data[2],
                         lifetime=data[3], owner=data[4], date_start=data[5])

            db.session.add(m)
            db.session.commit()

        except:
            print("ошибка")

