from sweater.models import Maintenance, Transmission, Dvs, Wheel, Springs, Device, Brakes, Pneumatics
from sweater import app, db

class Train_maintenance(object):
    repair: str
    status: str
    wheels: float
    springs: float
    transmissions: float
    dvs: float
    pneumatics: float
    brake: float
    device: int
    markM: float

    def __init__(self, repair="", status=""):
        self.repair = repair
        self.status = status

    def grade_wheels(self, wheels: [int]):
        if all(item < 3 for item in wheels):
            self.wheels = 10
        elif any(item == 3 for item in wheels) or any(item == 4 for item in wheels):
            self.wheels = 3
            self.repair += "Проверить разбег колесных пар. "
        else:
            self.wheels = 0
            self.repair += "Требуется ремонт колесных пар. "
            self.status += "Не допущен"

    def grade_springs(self, springs: [int]):
        if all(item < 68 for item in springs):
            self.springs = 10
        elif any(item == 68 for item in springs):
            self.springs = 3
            self.repair += "Проверить рессорное подвешивание. "
        else:
            self.springs = 0
            self.repair += "Требуется ремонт рессорного подвешивания. "
            self.status += "Не допущен"

    def grade_transmissions(self, oils: [float]):
        if 1.20 < oils[0] < 1.25:
            result_a = 10
        elif oils[0] == 1.20 or oils[0] == 1.25:
            result_a = 3
            self.repair += "Проверить давление масла питательного насоса. "
        else:
            result_a = 0
            self.repair += "Замените масло питательного насоса в гидропередаче. "
            self.status += "Не допущен"
        if 0.35 < oils[1] < 0.45:
            result_b = 10
        elif oils[1] == 0.35 or oils[1] == 0.45:
            result_b = 3
            self.repair += "Проверить давление масла на выходе из гидротрансформатора. "
        else:
            result_b = 0
            self.repair += "Замените масло в гидротрансформаторе. "
            self.status += "Не допущен"
        if 0.08 < oils[2] < 0.12:
            result_c = 10
        elif oils[2] == 0.08 or oils[2] < 0.12:
            result_c = 3
            self.repair += "Проверить давление в системе смазки. "
        else:
            result_c = 0
            self.repair += "Заменить смазку в гидропередаче. "
            self.status += "Не допущен"
        self.transmissions = round(((result_a + result_b + result_c) / 3),2)
        print(self.status)

    def grade_dvs(self, dvs: [float]):
        if dvs[0] < 35:
            result_a = 10
        elif dvs[0] == 35:
            result_a = 3
        else:
            result_a = 0
            self.repair += "Замените масло в двигателе, наработка свыше 35 м.ч. "
            self.status += "Не допущен"
        if dvs[1] == 32:
            result_b = 10
        elif dvs[1] == 31 or dvs[1] == 33:
            result_b = 3
            self.repair += "Проверить количество смазки в двигателе. "
        else:
            result_b = 0
            self.repair += "Добавить смазку в двигатель. "
            self.status += "Не допущен"
        if 4 < dvs[2] < 7:
            result_c = 10
        elif dvs[2] == 4 or dvs[2] == 7:
            result_c = 3
            self.repair += "Проверить давление масла при холостом пуске. "
        else:
            result_c = 0
            self.repair += "Заменить масло в двигателе. "
            self.status += "Не допущен"
        if 7 < dvs[3] < 11:
            result_d = 10
        elif dvs[3] == 7 or dvs[3] == 11:
            result_d = 3
            self.repair += "Проверить натяжение ремней привода генератора. "
        else:
            result_d = 0
            self.repair += "Заменить ремни привода генератора. "
            self.status += "Не допущен"
        if 12 < dvs[4] < 12.8:
            result_e = 10
        elif dvs[4] == 12 or dvs[4] == 12.8:
            result_e = 3
            self.repair += "Проверить напряжение генератора. "
        else:
            result_e = 0
            self.repair += "Заменить генератор. "
            self.status += "Не допущен"
        self.dvs = round(((result_a + result_b + result_c + result_d + result_e) / 5),2)
        print(self.status)

    def grade_device(self, device: [str]):
        if all(item == 'Исправен' for item in device):
            self.device = 10
        else:
            self.device = 0
            self.repair += "Заменить приборы безопасности. "
            self.status += "Не допущен"
        print(self.status)

    def grade_brake(self, brake: [float]):
        if brake[0] == 20:
            result_a = 10
        elif brake[0] == 19 or brake[0] == 21:
            result_a = 3
            self.repair += "Проверить толщину тормозных колодок. "
        else:
            result_a = 0
            self.repair += "Заменить тормозные колодки. "
            self.status += "Не допущен"
        if 40 < brake[1] < 71:
            result_b = 10
        elif 70 < brake[1] < 101:
            result_b = 3
            self.repair += "Проверить выход штока тормозного цилиндра. "
        else:
            result_b = 0
            self.repair += "Заменить шток тормозного цилиндра. "
            self.status += "Не допущен"
        self.brake = round(((result_a + result_b) / 2),2)
        print(self.status)

    def complete_grade(self):
        self.markM = round(((self.wheels + self.springs + self.transmissions +
                      self.brake + self.device + self.dvs +self.pneumatics)/7), 2)
        if self.repair == '':
            self.repair = "Ремонт не требуется"

    def statusM(self):
        if (self.wheels == self.springs == self.dvs == self.transmissions ==
                 self.device == self.brake == 10.0):
            self.status = "Допущен"
        elif self.status.count("Не допущен") != 0:
            self.status = "Не допущен"
        else:
            self.status = "Допущен c ограничениями"

    def change(self, info: []):
        info.grade = self.markM
        info.status = self.status
        try:
            db.session.commit()
        except:
            print("ошибка")

    def safeMaintenance(self, wheels: [int], springs: [int], dvs: [float], transmission: [float], pneumatics: [float],
                                             device: [str], brake: [int], type_oil,
                                                     data_check, type, date_maintenance, id_m):
        # положить данныые тех обслуживания в sql
        try:
            m = Maintenance(type=type, date_maintenance=date_maintenance, grade_TO=self.markM, repair=self.repair,
                            status_TO=self.status, id_machine=id_m)
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

            p = Pneumatics(compressor=pneumatics[0], density_PM=pneumatics[1], density_TM=pneumatics[2], density_TC=pneumatics[3],
                           filling_TC=pneumatics[4],
                           time_TC=pneumatics[5], density_UR=pneumatics[6], time_TM=pneumatics[7], time_UP=pneumatics[8],
                           reducer=pneumatics[9], pace_1=pneumatics[10], pace_2=pneumatics[11], pace_3=pneumatics[12],
                           EPK=pneumatics[13], grade_pneumatics=self.pneumatics, maintenance_id=m.id_maintenance)
            db.session.add(p)
            db.session.commit()

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
        print(pneumatics)
        if 7.2 < pneumatics[0] < 8.2:
            result_a = 10
        elif pneumatics[0] == 7.2 or pneumatics[0] == 8.2:
            result_a = 3
            self.repair += "Проверить компрессор. "
        else:
            result_a = 0
            self.repair += "Отремонтировать компрессор. "
            self.status += "Не допущен"
        if pneumatics[1] < 0.5:
            result_b = 10
        elif pneumatics[1] == 0.5:
            result_b = 3
        else:
            result_b = 0
            self.repair += "Проверить утечки питательной магистрали. "
            self.status += "Не допущен"
        if pneumatics[2] < 0.5:
            result_c = 10
        elif pneumatics[2] == 0.5:
            result_c = 3
        else:
            result_c = 0
            self.repair += "Проверить утечки тормозной магистрали. "
            self.status += "Не допущен"
        if pneumatics[3] < 0.3:
            result_d = 10
        elif pneumatics[3] == 0.3:
            result_d = 3
        else:
            result_d = 0
            self.repair += "Проверить колодки и выход штока тормозного цилиндра. "
            self.status += "Не допущен"
        if  pneumatics[4]<4:
            result_n = 10
        elif pneumatics[4] == 4:
            result_n = 3
        else:
            result_n = 0
            self.repair += "Отрегулировать кран тормозного цилиндра. "
            self.status += "Не допущен"
        if 13 < pneumatics[5]:
            result_e = 10
        elif pneumatics[5] == 13:
            result_e = 3
        else:
            result_e = 0
            self.repair += "Вывернуть пробку на крышке тормозного цилиндра. "
            self.status += "Не допущен"
        if pneumatics[6] < 0.2:
            result_f = 10
        elif pneumatics[6] == 0.2:
            result_f = 3
        else:
            result_f = 0
            self.repair += "Нарушение уплотнение по штуцерам трубки уравнительного резервуара. "
            self.status += "Не допущен"
        if pneumatics[7] < 4:
            result_g = 10
        elif pneumatics[7] == 4:
            result_g = 3
        else:
            result_g = 0
            self.repair += "Компенсировать повышенное давление в ТМ постановкой ручки крана в 5А. "
            self.status += "Не допущен"
        if 30 < pneumatics[8] < 40:
            result_h = 10
        elif pneumatics[8] == 30 or pneumatics[8] == 40:
            result_h = 3
        else:
            result_h = 0
            self.repair += "Почистить фильтр и открыть двухседельчатый клапан. "
            self.status += "Не допущен"
        if 5.0 < pneumatics[9] < 5.3:
            result_i = 10
        elif pneumatics[9] == 5.0 or pneumatics[9] == 5.3:
            result_i = 3
        else:
            result_i = 0
            self.repair += "Отрегулировать редуктор давления. "
            self.status += "Не допущен"
        if pneumatics[10] < 5:
            result_j = 10
        elif pneumatics[10] == 5:
            result_j = 3
        else:
            result_j = 0
            self.repair += "Заменить манжету уравнительного поршня. "
            self.status += "Не допущен"
        if 80 < pneumatics[11] < 110:
            result_k = 10
        elif pneumatics[11] == 110:
            result_k = 3
        else:
            result_k = 0
            self.repair += "При помощи регулировочной гайки отрегулировать темп понижения. "
            self.status += "Не допущен"
        if pneumatics[12] < 3:
            result_l = 10
        elif pneumatics[12] == 3:
            result_l = 3
        else:
            result_l = 0
            self.repair += "Сделать рахрядку тормозной магистрали. "
            self.status += "Не допущен"
        if pneumatics[13] == 7:
            result_m = 10
        elif pneumatics[13] == 7.1 or pneumatics[13] == 6.9:
            result_m = 3
        else:
            result_m = 0
            self.repair += "Отремонтировать электропневматический клапан. "
            self.status += "Не допущен"
        self.pneumatics = round(((result_a + result_b + result_c + result_d + result_e + result_f + result_g +
                           result_h + result_i + result_j + result_k + result_l + result_m + result_n) / 14),2)




