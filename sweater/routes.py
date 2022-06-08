from flask import render_template, url_for, request, redirect, flash, session
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
import pandas as pd   #  pip install pandas
import sqlite3

import compare

from sweater import app, db
from sweater.models import User, Machines, Maintenance, Transmission, Dvs, Wheel, Springs, Device, Brakes, Pneumatics


@app.route("/create", methods=("POST", "GET"))
@login_required
def create():
    if request.method == "POST":
        id_number = request.form['id_number']
        date_manufacture = request.form['date_manufacture']
        name_factory = request.form['name_factory']
        lifetime = request.form['lifetime']
        owner = request.form['owner']
        date_start = request.form['date_start']

        try:
            m = Machines(id_number=id_number, date_manufacture=date_manufacture, name_factory=name_factory,
                         lifetime=lifetime, date_start=date_start, owner=owner)

            db.session.add(m)
            db.session.commit()

        except:
            print("ошибка")

    return render_template("create.html", title="Провести оценку")


@app.route("/grade/<int:id>", methods=("POST", "GET"))
@login_required
def grade(id):
    info = Machines.query.get(id)
    if request.method == "POST":

        type = request.form['type']
        date_maintenance = request.form['date_maintenance']


        first_across_rl = request.form.get('first_across_rl', type=int)
        first_across_rr = request.form.get('first_across_rr', type=int)
        first_across_ll = request.form.get('first_across_ll', type=int)
        first_across_lr = request.form.get('first_across_lr', type=int)
        second_across_rl = request.form.get('second_across_rl', type=int)
        second_across_rr = request.form.get('second_across_rr', type=int)
        second_across_ll = request.form.get('second_across_ll', type=int)
        second_across_lr = request.form.get('second_across_lr', type=int)
        first_lateral_r = request.form.get('first_lateral_r', type=int)
        first_lateral_l = request.form.get('first_lateral_l', type=int)
        second_lateral_r = request.form.get('second_lateral_r', type=int)
        second_lateral_l = request.form.get('second_lateral_l', type=int)

        grade_wheel = compare.grade_wheel(first_across_rl, first_across_rr, first_across_ll, first_across_lr,
second_across_rl, second_across_rr, second_across_ll, second_across_lr,
first_lateral_r, first_lateral_l, second_lateral_r, second_lateral_l)


        first_r_spring_H1 = request.form.get('first_r_spring_H1', type=int)
        first_r_spring_H2 = request.form.get('first_r_spring_H2', type=int)
        first_l_spring_H1 = request.form.get('first_l_spring_H1', type=int)
        first_l_spring_H2 = request.form.get('first_l_spring_H2', type=int)
        second_r_spring_H1 = request.form.get('second_r_spring_H1', type=int)
        second_r_spring_H2 = request.form.get('second_r_spring_H2', type=int)
        second_l_spring_H1 = request.form.get('second_l_spring_H1', type=int)
        second_l_spring_H2 = request.form.get('second_l_spring_H2', type=int)
        first_r_spring_m = request.form.get('first_r_spring_m', type=int)
        first_l_spring_m = request.form.get('first_l_spring_m', type=int)
        second_r_spring_m = request.form.get('second_r_spring_m', type=int)
        second_l_spring_m = request.form.get('second_l_spring_m', type=int)
        grade_spring = compare.grade_spring(first_r_spring_H1, first_r_spring_H2, first_l_spring_H1, first_l_spring_H2,
second_r_spring_H1, second_r_spring_H2, second_l_spring_H1, second_l_spring_H2,
first_r_spring_m, first_l_spring_m, second_r_spring_m, second_l_spring_m)

        time = request.form.get('time', type=int)
        type_oil = request.form['type_oil']
        amount_oil = request.form.get('amount_oil', type=int)
        pressure_oil = request.form.get('pressure_oil', type=float)
        tension = request.form.get('tension', type=float)
        voltage = request.form.get('voltage', type=float)
        grade_dvs = compare.grade_dvs(time, amount_oil, pressure_oil, tension, voltage)

        pressure_oil_p = request.form.get('pressure_oil_p', type=float)
        pressure_oil_t = request.form.get('pressure_oil_t', type=float)
        pressure_oil_s = request.form.get('pressure_oil_s', type=float)
        grade_transmission = compare.grade_transmission(pressure_oil_p, pressure_oil_t, pressure_oil_s)

        compressor = request.form.get('compressor', type=float)
        density_PM = request.form.get('density_PM', type=float)
        density_TM = request.form.get('density_TM', type=float)
        density_TC = request.form.get('density_TC', type=float)
        time_TC = request.form.get('time_TC', type=float)
        density_UR = request.form.get('density_UR', type=float)
        time_TM = request.form.get('time_TM', type=float)
        time_UP = request.form.get('time_UP', type=float)
        reducer = request.form.get('reducer', type=float)
        pace_1 = request.form.get('pace_1', type=float)
        pace_2 = request.form.get('pace_2', type=float)
        pace_3 = request.form.get('pace_3', type=float)
        EPK = request.form.get('EPK', type=float)
        grade_pneumatics = compare.grade_pneumatics(compressor, density_PM, density_TM, density_TC,
                                                    time_TC, density_UR, time_TM, time_UP,
                                                    reducer, pace_1, pace_2, pace_3, EPK)

        bel = request.form['bel']
        bil1 = request.form['bil1']
        bil2 = request.form['bil2']
        bkr = request.form['bkr']
        dup = request.form['dup']
        grade_device = compare.grade_device(bel, bil1, bil2, bkr, dup)

        data_check = request.form['data_check']
        depth = request.form.get('depth', type=int)
        rod = request.form.get('rod', type=int)
        grade_brake = compare.grade_brake(depth, rod)

        grade_TO = compare.markM(grade_wheel, grade_spring, grade_dvs, grade_transmission,grade_pneumatics,grade_device,grade_brake)

        info.grade = grade_TO
        info.status = "допущен"
        repair = compare.repairM()

        try:
            m = Maintenance(type=type, date_maintenance=date_maintenance, grade_TO=grade_TO, repair=repair, id_machine=id)
            db.session.add(m)
            db.session.flush()

            w = Wheel(first_across_rl=first_across_rl, first_across_rr= first_across_rr, first_across_ll =first_across_ll,
                      first_across_lr=first_across_lr, second_across_rl =second_across_rl, second_across_rr = second_across_rr,
                      second_across_ll=second_across_ll, second_across_lr = second_across_lr,first_lateral_r =first_lateral_r,
                      first_lateral_l=first_lateral_l, second_lateral_r = second_lateral_r,second_lateral_l =second_lateral_l,
                      grade_wheel=grade_wheel, maintenance_id=m.id_maintenance)
            db.session.add(w)
            db.session.commit()

            s = Springs(first_r_spring_H1 = first_r_spring_H1,first_r_spring_H2 = first_r_spring_H2,first_l_spring_H1 = first_l_spring_H1,
                        first_l_spring_H2 = first_l_spring_H2,second_r_spring_H1 = second_r_spring_H1,second_r_spring_H2 = second_r_spring_H2,
                        second_l_spring_H1 = second_l_spring_H1,second_l_spring_H2 =second_l_spring_H2,first_r_spring_m =first_r_spring_m,
                        first_l_spring_m = first_l_spring_m,second_r_spring_m =second_r_spring_m,second_l_spring_m =second_l_spring_m,
                        grade_spring=grade_spring, maintenance_id=m.id_maintenance)
            db.session.add(s)
            db.session.commit()

            d = Dvs(time=time, type_oil=type_oil, amount_oil=amount_oil, pressure_oil=pressure_oil,tension=tension,
                    voltage=voltage, grade_dvs=grade_dvs, maintenance_id=m.id_maintenance)
            db.session.add(d)
            db.session.commit()

            t = Transmission(pressure_oil_p = pressure_oil_p,pressure_oil_t =pressure_oil_t,pressure_oil_s =pressure_oil_s,
                             grade_transmission=grade_transmission, maintenance_id=m.id_maintenance)
            db.session.add(t)
            db.session.commit()

            p = Pneumatics(compressor =compressor, density_PM =density_PM,density_TM =density_TM, density_TC =density_TC,
                           time_TC =time_TC,density_UR =density_UR,time_TM =time_TM,time_UP =time_UP,reducer = reducer,pace_1 =pace_1,
                           pace_2 =pace_2,pace_3 = pace_3,EPK = EPK,grade_pneumatics=grade_pneumatics, maintenance_id=m.id_maintenance)
            db.session.add(p)
            db.session.commit()

            de = Device(bel=bel, bil1=bil1, bil2=bil2, bkr=bkr, dup=dup, grade_device=grade_device, maintenance_id=m.id_maintenance)
            db.session.add(de)
            db.session.commit()

            b = Brakes(data_check =data_check,depth = depth, rod =rod,grade_brake=grade_brake, maintenance_id=m.id_maintenance)
            db.session.add(b)
            db.session.commit()
        except:
            print("ошибка")

    return render_template("grade.html", title="Провести оценку")


@app.route('/', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get('next')

            return redirect(url_for('home'))
        else:
            flash('Некорректный логин или пароль', category='error')
    else:
        flash('Пожалуйста, заполните логин и пароль', category='error')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not (login or password or password2):
            flash('')
        elif password != password2:
            flash('пароли не совпадают', category='error')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))

    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('posts'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)

    return response


@app.route('/home')
@login_required
def home():
    info = []
    try:
        info = Machines.query.all()
    except:
        print("ошибка")

    return render_template("home.html", list=info)


@app.route('/machine/<int:id>')
@login_required
def machine_detail(id):
    info = []
    info1 = []
    col = "red"
    try:
        info = Machines.query.get(id)
        info1 = Maintenance.query.filter_by(id_machine=id).order_by(Maintenance.date_maintenance.desc()).all()
    except:
        print("ошибка")
    legend = 'Monthly Data'
    labels = []
    values = []
    labels = Maintenance.query.all()
    values = Maintenance.query.order_by(Maintenance.grade_TO).all()
    print(values)
    return render_template("machine_detail.html", list=info, list1=info1, col=col,values=values, labels=labels, legend=legend)


@app.route('/grade_detail/<int:id>')
@login_required
def grade_detail(id):
    info = []
    info1 = []

    try:
        info = Maintenance.query.get(id)
        info1 = Maintenance.query.filter_by(id_machine=id).order_by(Maintenance.date_maintenance.desc()).all()
    except:
        print("ошибка")

    return render_template("grade_detail.html", list=info, list1=info1)


@app.route('/maintenance/<int:id>')
@login_required
def maintenance_detail(id):
    info = []
    try:
        info = Maintenance.query.all()
        info = Maintenance.query.get(id)
    except:
        print("ошибка")
    return render_template("maintenance_detail.html", list=info)


@app.route('/remove', methods=["POST"])
@login_required
def remove():
    checked_boxes = request.form.getlist("check")
    for id in checked_boxes:
        Maintenance.query.all()
        Transmission.query.all()
        Dvs.query.all()
        Wheel.query.all()
        Springs.query.all()
        Pneumatics.query.all()
        Device.query.all()
        Brakes.query.all()
        wheel=Wheel.query.filter_by(maintenance_id=id).first()
        springs=Springs.query.filter_by(maintenance_id=id).first()
        pneumatics=Pneumatics.query.filter_by(maintenance_id=id).first()
        device=Device.query.filter_by(maintenance_id=id).first()
        brakes =Brakes.query.filter_by(maintenance_id=id).first()
        transmission = Transmission.query.filter_by(maintenance_id=id).first()
        dvs = Dvs.query.filter_by(maintenance_id=id).first()
        to = Maintenance.query.get_or_404(id)
        try:
            db.session.delete(wheel)
            db.session.delete(springs)
            db.session.delete(pneumatics)
            db.session.delete(device)
            db.session.delete(brakes)
            db.session.delete(transmission)
            db.session.delete(dvs)
            db.session.delete(to)
            db.session.commit()
        except:
            return "При удалении произошла ошибка"

    return redirect('/home')


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
@login_required
def post_update(id):
    info = []
    info = To.query.all()
    info = To.query.get(id)
    if request.method == "POST":
        info.number = request.form['number']
        info.type_TO = request.form['type_TO']
        info.pressure1 = request.form['pressure1']
        info.pressure2 = request.form['pressure2']
        info.pressure3 = request.form['pressure3']
        info.pressure_dvs = request.form['pressure_dvs']
        info.hours = request.form['hours']

        try:
            db.session.commit()
            return redirect('/home')
        except:
            print("ошибка")
    else:

        return render_template("post_update.html", list=info)



@app.route('/excel')
def excel():
    conn = sqlite3.connect('C:/Users/Admin/PycharmProjects/diplom/sweater/rzd.db')
    df = pd.read_sql('SELECT id_maintenance, type, date_maintenance, grade_TO, repair FROM Maintenance WHERE id_machine=1', conn)
    df.columns = ['Номер', 'Тип ТО', 'Дата ТО', 'Оценка', 'Ремонт']
    df.to_excel(r'C:/Users/Admin/PycharmProjects/diplom/result.xlsx', sheet_name='Sheet1')
    flash('Файл успешно скачен в раздел загрузки', category='success')
    return redirect('/home')


@app.route("/simple_chart")
def chart():
    legend = 'Monthly Data'
    session.add(Maintenance)
    session.commit()
    print(session.query(Maintenance.type, Maintenance.grade_TO).all())
    labels = []
    values = []
    labels = Maintenance.query.all()
    values = Maintenance.query.order_by(Maintenance.grade_TO).all()
    print(values)
    return render_template('chart.html', values=values, labels=labels, legend=legend)

