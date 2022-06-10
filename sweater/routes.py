from flask import render_template, url_for, request, redirect, flash, session
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
import pandas as pd  # pip install pandas
import sqlite3

import compare

from sweater import app, db
from sweater.models import User, Machines, Maintenance, Transmission, Dvs, Wheel, Springs, Device, Brakes, Pneumatics

from sweater.Train import Train


@app.route("/create", methods=("POST", "GET"))
@login_required
def create():
    if request.method == "POST":
        train = []
        train.append(request.form['id_number'])
        train.append(request.form['date_manufacture'])
        train.append(request.form['name_factory'])
        train.append(request.form['lifetime'])
        train.append(request.form['owner'])
        train.append(request.form['date_start'])
        Train.create_train(train)
    return render_template("create.html", title="Провести оценку")


@app.route("/grade/<int:id>", methods=("POST", "GET"))
@login_required
def grade(id):
    info = Machines.query.get(id)
    if request.method == "POST":
        forms_data = request.form
        type = request.form['type']
        date_maintenance = request.form['date_maintenance']
        wheels = []
        for key, value in forms_data:
            if 'across' in key:
                wheels.append(int(value))
            if 'lateral' in key:
                wheels.append(int(value))

        springs = []
        for key, value in forms_data:
            if 'spring' in key:
                springs.append(int(value))

        dvs = []
        dvs.append(request.form.get('time', type=float))
        type_oil = request.form['type_oil']
        dvs.append(request.form.get('amount_oil', type=float))
        dvs.append(request.form.get('pressure_oil', type=float))
        dvs.append(request.form.get('tension', type=float))
        dvs.append(request.form.get('voltage', type=float))

        transmission = []
        transmission.append(request.form.get('pressure_oil_p', type=float))
        transmission.append(request.form.get('pressure_oil_t', type=float))
        transmission.append(request.form.get('pressure_oil_s', type=float))

        pneumatics = []
        transmission.append(request.form.get('compressor', type=float))
        transmission.append(request.form.get('density_PM', type=float))
        transmission.append(request.form.get('density_TM', type=float))
        transmission.append(request.form.get('density_TC', type=float))
        transmission.append(request.form.get('time_TC', type=float))
        transmission.append(request.form.get('density_UR', type=float))
        transmission.append(request.form.get('time_TM', type=float))
        transmission.append(request.form.get('time_UP', type=float))
        transmission.append(request.form.get('reducer', type=float))
        transmission.append(request.form.get('pace_1', type=float))
        transmission.append(request.form.get('pace_2', type=float))
        transmission.append(request.form.get('pace_3', type=float))
        transmission.append(request.form.get('EPK', type=float))

        device = []
        device.append(request.form['bel'])
        device.append(request.form['bil1'])
        device.append(request.form['bil2'])
        device.append(request.form['bkr'])
        device.append(request.form['dup'])

        brake = []
        data_check = request.form['data_check']
        brake.append(request.form.get('depth', type=float))
        brake.append(request.form.get('rod', type=float))

        train = Train(id, wheels, springs, dvs, transmission, pneumatics, device, brake, type_oil, data_check, type, date_maintenance)
        grade_TO = train.make_maintenance()

        info.grade = grade_TO
        info.status = train.change_statis(id)

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
    try:
        info = Machines.query.get(id)
        info1 = Maintenance.query.filter_by(id_machine=id).order_by(Maintenance.date_maintenance.desc()).all()
    except:
        print("ошибка")
    legend = 'Monthly Data'
    labels = Maintenance.query.all()
    values = Maintenance.query.order_by(Maintenance.grade_TO).all()
    print(values)
    return render_template("machine_detail.html", list=info, list1=info1, values=values, labels=labels,
                           legend=legend)


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
        wheel = Wheel.query.filter_by(maintenance_id=id).first()
        springs = Springs.query.filter_by(maintenance_id=id).first()
        pneumatics = Pneumatics.query.filter_by(maintenance_id=id).first()
        device = Device.query.filter_by(maintenance_id=id).first()
        brakes = Brakes.query.filter_by(maintenance_id=id).first()
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
    df = pd.read_sql(
        'SELECT id_maintenance, type, date_maintenance, grade_TO, repair FROM Maintenance WHERE id_machine=1', conn)
    df.columns = ['Номер', 'Тип ТО', 'Дата ТО', 'Оценка', 'Ремонт']
    df.to_excel(r'C:/Users/Admin/PycharmProjects/diplom/result.xlsx', sheet_name='Sheet1')
    flash('Файл успешно скачен в раздел загрузки', category='success')
    return redirect('/home')

