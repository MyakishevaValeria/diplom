from sweater.models import Maintenance, Transmission, Dvs, Wheel, Springs, Device, Brakes, Pneumatics
from sweater import app, db

class Train_maintenance(object):
    wheels: int
    springs: int
    repair: str
    transmissions: float
    dvs: float
    pneumatics: float
    brake: float
    device: int
    markM: float

    def grade_wheels(self, wheels: [int]):
        if all(item == 3 for item in wheels):
            self.wheels = 10
        elif any(item == 4 for item in wheels) or any(item == 2 for item in wheels):
            self.wheels = 3
        else:
            self.wheels = 0

    def grade_springs(self, springs: [int]):
        if all(item == 68 for item in springs):
            self.springs = 10
        elif any(item == 69 for item in springs) or any(item == 67 for item in springs):
            self.springs = 3
        else:
            self.springs = 0

    def grade_transmissions(self, oils: [float]):
        if 1.20 < oils[0] < 1.25:
            result_a = 10
        elif 1.15 < oils[0] < 1.20 or 1.25 < oils[0] < 1.30:
            result_a = 3
        else:
            result_a = 0
            #self.repair += "Замените масло в двигателе"
        if 0.35 < oils[1] < 0.4:
            result_b = 10
        elif 0.3 < oils[1] < 0.35 or 0.4 < oils[1] < 0.45:
            result_b = 3
        else:
            result_b = 0
            #self.repair += "Замените охлаждающую жидкость"
        if 0.08 < oils[2] < 0.12:
            result_c = 10
        elif 0.05 < oils[2] < 0.08 or 0.12 < oils[2] < 0.15:
            result_c = 3
        else:
            result_c = 0
            #self.repair += "Проверить давление"
        self.transmissions = (result_a + result_b + result_c) / 3

    def grade_dvs(self, dvs: [float]):
        if 1.20 < dvs[0] < 1.25:
            result_a = 10
        elif 1.15 < dvs[0] < 1.20 or 1.25 < dvs[0] < 1.30:
            result_a = 3
        else:
            result_a = 0
            #self.repair += "Замените масло в двигателе"
        if 0.35 < dvs[1] < 0.4:
            result_b = 10
        elif 0.3 < dvs[1] < 0.35 or 0.4 < dvs[1] < 0.45:
            result_b = 3
        else:
            result_b = 0
            #self.repair += "Замените охлаждающую жидкость"
        if 0.08 < dvs[2] < 0.12:
            result_c = 10
        elif 0.05 < dvs[2] < 0.08 or 0.12 < dvs[2] < 0.15:
            result_c = 3
        else:
            result_c = 0
            #self.repair += "Проверить давление"
        if 0.35 < dvs[3] < 0.4:
            result_d = 10
        elif 0.3 < dvs[3] < 0.35 or 0.4 < dvs[3] < 0.45:
            result_d = 3
        else:
            result_d = 0
            #self.repair += "Замените охлаждающую жидкость"
        if 0.08 < dvs[4] < 0.12:
            result_e = 10
        elif 0.05 < dvs[4] < 0.08 or 0.12 < dvs[4] < 0.15:
            result_e = 3
        else:
            result_e = 0
            #self.repair += "Проверить давление"
        self.dvs = (result_a + result_b + result_c + result_d + result_e) / 5

    def grade_device(self, device: [str]):
        if all(item == 'Исправен' for item in device):
            self.device = 10
        else:
            self.device = 0

    def grade_brake(self, brake: [float]):
        if 1.20 < brake[0] < 1.25:
            result_a = 10
        elif 1.15 < brake[0] < 1.20 or 1.25 < brake[0] < 1.30:
            result_a = 3
        else:
            result_a = 0
            #self.repair += "Замените масло в двигателе"
        if 0.35 < brake[1] < 0.4:
            result_b = 10
        elif 0.3 < brake[1] < 0.35 or 0.4 < brake[1] < 0.45:
            result_b = 3
        else:
            result_b = 0
            #self.repair += "Замените охлаждающую жидкость"
        self.brake = (result_a + result_b) / 2

    def complete_grade(self):
        self.markM = (self.wheels + self.springs + self.transmissions +
                      self.brake + self.device + self.dvs )/7

    def status(self):
        if (self.wheels == self.springs == self.dvs == self.transmissions ==
                 self.device == self.brake == 10.0):
            self.status = "Допущен"
        else:
            self.status = "Не Допущен"
        #elif self.repair != "":
         #   self.status = "Недопущен"

    def safeMaintenance(self, wheels: [int], springs: [int], dvs: [float], transmission: [float],
                                             device: [str], brake: [int], type_oil,
                                                     data_check, type, date_maintenance, id_m):
        # положить данныые тех обслуживания в sql
        try:
            m = Maintenance(type=type, date_maintenance=date_maintenance, grade_TO=self.markM,
                            id_machine=id_m)
            db.session.add(m)
            db.session.flush()
            w = Wheel(first_across_rl=wheels[0], first_across_rr=wheels[1], first_across_ll=wheels[2],
                      first_across_lr=wheels[3], second_across_rl=wheels[4], second_across_rr=wheels[5],
                      second_across_ll=wheels[6], second_across_lr=wheels[7], first_lateral_r=wheels[8],
                      first_lateral_l=wheels[9], second_lateral_r=wheels[10], second_lateral_l=wheels[11],
                      grade_wheel=self.wheels, maintenance_id=m.id_maintenance)
            db.session.add(w)
            db.session.commit()

            s = Springs(first_r_spring_H1=springs[0], first_r_spring_H2=springs[1],
                        first_l_spring_H1=springs[2], first_l_spring_H2=springs[3], second_r_spring_H1=springs[4],
                        second_r_spring_H2=springs[5], second_l_spring_H1=springs[6], second_l_spring_H2=springs[7],
                        first_r_spring_m=springs[8], first_l_spring_m=springs[9], second_r_spring_m=springs[10],
                        second_l_spring_m=springs[11], grade_spring=self.springs, maintenance_id=m.id_maintenance)
            db.session.add(s)
            db.session.commit()

            d = Dvs(time=dvs[0], type_oil=type_oil, amount_oil=dvs[1], pressure_oil=dvs[2], tension=dvs[3],
                    voltage=dvs[4], grade_dvs=self.dvs, maintenance_id=m.id_maintenance)
            db.session.add(d)
            db.session.commit()

            t = Transmission(pressure_oil_p=transmission[0], pressure_oil_t=transmission[1],
                             pressure_oil_s=transmission[2],
                             grade_transmission=self.transmissions, maintenance_id=m.id_maintenance)
            db.session.add(t)
            db.session.commit()
            '''
            p = Pneumatics(compressor=pneumatics[0], density_PM=pneumatics[1], density_TM=pneumatics[2], density_TC=pneumatics[3],
                           time_TC=pneumatics[4], density_UR=pneumatics[5], time_TM=pneumatics[6], time_UP=pneumatics[7],
                           reducer=pneumatics[8], pace_1=pneumatics[9], pace_2=pneumatics[10], pace_3=pneumatics[11],
                           EPK=pneumatics[12], grade_pneumatics=self.pneumatics, maintenance_id=m.id_maintenance)
            db.session.add(p)
            db.session.commit()
            '''
            de = Device(bel=device[0], bil1=device[1], bil2=device[2], bkr=device[3], dup=device[4],
                        grade_device=self.device, maintenance_id=m.id_maintenance)
            db.session.add(de)
            db.session.commit()

            b = Brakes(data_check=data_check, depth=brake[0], rod=brake[1], grade_brake=self.brake,
                       maintenance_id=m.id_maintenance)
            db.session.add(b)
            db.session.commit()
        except:
            print("ошибка")

    def grade_pneumatics(self, pneumatics: [float]):
        if 1.20 < pneumatics[0] < 1.25:
            result_a = 10
        elif 1.15 < pneumatics[0] < 1.20 or 1.25 < pneumatics[0] < 1.30:
            result_a = 3
        else:
            result_a = 0
            #self.repair += "Замените масло в двигателе"
        if 0.35 < pneumatics[1] < 0.4:
            result_b = 10
        elif 0.3 < pneumatics[1] < 0.35 or 0.4 < pneumatics[1] < 0.45:
            result_b = 3
        else:
            result_b = 0
            #self.repair += "Замените охлаждающую жидкость"
        if 0.08 < pneumatics[2] < 0.12:
            result_c = 10
        elif 0.05 < pneumatics[2] < 0.08 or 0.12 < pneumatics[2] < 0.15:
            result_c = 3
        else:
            result_c = 0
            #self.repair += "Проверить давление"
        if 0.35 < pneumatics[3] < 0.4:
            result_d = 10
        elif 0.3 < pneumatics[3] < 0.35 or 0.4 < pneumatics[3] < 0.45:
            result_d = 3
        else:
            result_d = 0
            #self.repair += "Замените охлаждающую жидкость"
        if 0.08 < pneumatics[4] < 0.12:
            result_e = 10
        elif 0.05 < pneumatics[4] < 0.08 or 0.12 < pneumatics[4] < 0.15:
            result_e = 3
        else:
            result_e = 0
            #self.repair += "Проверить давление"
        if 1.20 < pneumatics[5] < 1.25:
            result_f = 10
        elif 1.15 < pneumatics[5] < 1.20 or 1.25 < pneumatics[5] < 1.30:
            result_f = 3
        else:
            result_f = 0
            #self.repair += "Замените масло в двигателе"
        if 0.35 < pneumatics[6] < 0.4:
            result_g = 10
        elif 0.3 < pneumatics[6] < 0.35 or 0.4 < pneumatics[6] < 0.45:
            result_g = 3
        else:
            result_g = 0
            #self.repair += "Замените охлаждающую жидкость"
        if 0.08 < pneumatics[7] < 0.12:
            result_h = 10
        elif 0.05 < pneumatics[7] < 0.08 or 0.12 < pneumatics[7] < 0.15:
            result_h = 3
        else:
            result_h = 0
            #self.repair += "Проверить давление"
        if 0.35 < pneumatics[8] < 0.4:
            result_i = 10
        elif 0.3 < pneumatics[8] < 0.35 or 0.4 < pneumatics[8] < 0.45:
            result_i = 3
        else:
            result_i = 0
            #self.repair += "Замените охлаждающую жидкость"
        if 0.08 < pneumatics[9] < 0.12:
            result_j = 10
        elif 0.05 < pneumatics[9] < 0.08 or 0.12 < pneumatics[9] < 0.15:
            result_j = 3
        else:
            result_j = 0
            #self.repair += "Проверить давление"
        if 1.20 < pneumatics[10] < 1.25:
            result_k = 10
        elif 1.15 < pneumatics[10] < 1.20 or 1.25 < pneumatics[10] < 1.30:
            result_k = 3
        else:
            result_k = 0
            #self.repair += "Замените масло в двигателе"
        if 0.35 < pneumatics[11] < 0.4:
            result_l = 10
        elif 0.3 < pneumatics[11] < 0.35 or 0.4 < pneumatics[11] < 0.45:
            result_l = 3
        else:
            result_l = 0
            #self.repair += "Замените охлаждающую жидкость"
        if 0.08 < pneumatics[12] < 0.12:
            result_m = 10
        elif 0.05 < pneumatics[12] < 0.08 or 0.12 < pneumatics[12] < 0.15:
            result_m = 3
        else:
            result_m = 0
           # self.repair += "Проверить давление"
        self.pneumatics = (result_a + result_b + result_c + result_d + result_e + result_f + result_g +
                           result_h + result_i + result_j + result_k + result_l + result_m) / 13





