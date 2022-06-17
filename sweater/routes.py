from flask import render_template, url_for, request, redirect, flash, session
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
import pandas as pd  # pip install pandas
import sqlite3
from styleframe import StyleFrame

import xlsxwriter
from datetime import datetime, timedelta

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
    info = []
    info = Machines.query.get(id)
    if request.method == "POST":
        forms_data = request.form
        type = request.form['type']
        date_maintenance = request.form['date_maintenance']
        wheels = []
        for key, value in forms_data.items():
            if 'across' in key:
                wheels.append(int(value))
            if 'lateral' in key:
                wheels.append(int(value))

        springs = []
        for key, value in forms_data.items():
            if 'spring' in key:
                springs.append(int(value))

        dvs = []
        dvs.append(request.form.get('time', type=int))
        type_oil = request.form['type_oil']
        dvs.append(request.form.get('amount_oil', type=int))
        dvs.append(request.form.get('pressure_oil', type=float))
        dvs.append(request.form.get('tension', type=float))
        dvs.append(request.form.get('voltage', type=float))

        transmission = []
        transmission.append(request.form.get('pressure_oil_p', type=float))
        transmission.append(request.form.get('pressure_oil_t', type=float))
        transmission.append(request.form.get('pressure_oil_s', type=float))

        pneumatics = []
        pneumatics.append(request.form.get('compressor', type=float))
        pneumatics.append(request.form.get('density_PM', type=float))
        pneumatics.append(request.form.get('density_TM', type=float))
        pneumatics.append(request.form.get('density_TC', type=float))
        pneumatics.append(request.form.get('time_TC', type=float))
        pneumatics.append(request.form.get('density_UR', type=float))
        pneumatics.append(request.form.get('time_TM', type=float))
        pneumatics.append(request.form.get('time_UP', type=float))
        pneumatics.append(request.form.get('reducer', type=float))
        pneumatics.append(request.form.get('pace_1', type=float))
        pneumatics.append(request.form.get('pace_2', type=float))
        pneumatics.append(request.form.get('pace_3', type=float))
        pneumatics.append(request.form.get('EPK', type=float))

        device = []
        device.append(request.form['bel'])
        device.append(request.form['bil1'])
        device.append(request.form['bil2'])
        device.append(request.form['bkr'])
        device.append(request.form['dup'])

        brake = []
        data_check = request.form['data_check']
        brake.append(request.form.get('depth', type=int))
        brake.append(request.form.get('rod', type=int))

        train = Train(id, info, wheels, springs, dvs, transmission, pneumatics, device, brake, type_oil, data_check, type, date_maintenance)
        train.make_maintenance()
    return render_template("grade.html", title="Провести оценку", list=info)


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
    return redirect(url_for('home'))


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
    info_to = []
    try:
        info = Machines.query.get(id)
        info_to = Maintenance.query.filter_by(id_machine=id).order_by().all()
    except:
        print("ошибка")
    return render_template("machine_detail.html", list=info, list1=info_to)


@app.route('/grade_detail/<int:id>')
@login_required
def grade_detail(id):
    info = []
    info_to = []
    try:
        info = Maintenance.query.get(id)
        info_to = Maintenance.query.filter_by(id_machine=id).order_by(Maintenance.date_maintenance.desc()).all()
    except:
        print("ошибка")

    return render_template("grade_detail.html", list=info, list1=info_to)


@app.route('/maintenance/<int:id>')
@login_required
def maintenance_detail(id):
    info = []
    try:
        info = Maintenance.query.get(id)
    except:
        print("ошибка")
    return render_template("maintenance_detail.html", list=info)


@app.route('/remove-grade', methods=["POST"])
@login_required
def remove_grade():
    checked_boxes = request.form.getlist("check")
    for id in checked_boxes:
        Maintenance.query.all()
        to = Maintenance.query.get_or_404(id)
        try:
            db.session.delete(to)
            db.session.commit()
        except:
            return "При удалении произошла ошибка"

    return redirect('/home')


@app.route('/remove', methods=["POST"])
@login_required
def remove():
    checked_boxes = request.form.getlist("check")
    for id in checked_boxes:
        Machines.query.all()
        machines = Machines.query.get_or_404(id)
        try:
            db.session.delete(machines)
            db.session.commit()
        except:
            return "При удалении произошла ошибка"

    return redirect('/home')


@app.route('/machine/<int:id>/update', methods=['POST', 'GET'])
@login_required
def machine_update(id):
    info = []
    info = Machines.query.get(id)
    if request.method == "POST":
        info.id_number = request.form['id_number']
        info.date_manufacture = request.form['date_manufacture']
        info.name_factory = request.form['name_factory']
        info.lifetime = request.form['lifetime']
        info.owner = request.form['owner']
        info.date_start = request.form['date_start']

        try:
            db.session.commit()
            return redirect('/machine/'+str(id))
        except:
            print("ошибка")
    else:

        return render_template("machine_update.html", list=info)


@app.route('/excel', methods=['POST', 'GET'])
def excel():
    conn = sqlite3.connect('C:/Users/Admin/PycharmProjects/diplom/sweater/rzd.db')
    df = pd.read_sql('SELECT * FROM Maintenance', conn)
    df.columns = ['Номер', 'Тип ТО', 'Дата ТО', 'Оценка', 'Ремонт', 'Статус', 'Номер машины']

    def highlight_rows(s):
        con = s.copy()
        con[:] = None
        if (s['Статус'] == 'Допущен'):
            con[:] = "background-color: #98FB98"
        elif (s['Статус'] == 'Не допущен'):
            con[:] = "background-color: red"
        else:
            con[:] = "background-color: #F0E68C"
        return con

    styled = df.style.apply(highlight_rows, axis=1)
    writer = pd.ExcelWriter('C:/Users/Admin/PycharmProjects/diplom/result.xlsx')
    styled.to_excel(writer, sheet_name='my_analysis', engine='openpyxl', index=False)

    #df.to_excel(writer, sheet_name='my_analysis', index=False, na_rep='NaN')

    for column in df:
        column_width = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets['my_analysis'].set_column(col_idx, col_idx, column_width)

    writer.save()
    flash('Файл успешно скачен в раздел загрузки', category='success')
    return redirect('/home')

