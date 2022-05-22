from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
import pandas as pd   #  pip install pandas
import sqlite3

import compare

from sweater import app, db
from sweater.models import User, To, Transmission, Dvs


@app.route("/create", methods=("POST", "GET"))
def create():
    if request.method == "POST":
        number = request.form['number']
        type_TO = request.form['type_TO']
        pressure1 = request.form['pressure1']
        pressure2 = request.form['pressure2']
        pressure3 = request.form['pressure3']
        pressure_dvs = request.form['pressure_dvs']
        hours = request.form['hours']

        mark_transmission = compare.markTR(pressure1, pressure2, pressure3)
        mark_dvs = compare.markDVS(pressure_dvs, hours)
        grade = compare.markM(mark_transmission, mark_dvs)

        repair = compare.repair(grade)

        try:
            m = To(number=number, type_TO=type_TO, grade=grade, repair=repair)

            db.session.add(m)
            db.session.flush()

            t = Transmission(pressure1=pressure1, pressure2=pressure2,
                             pressure3=pressure3, mark_transmission=mark_transmission, machine_id=m.id)

            db.session.add(t)
            db.session.commit()

            d = Dvs(pressure_dvs=pressure_dvs, hours=hours, mark_dvs=mark_dvs, machine1_id=m.id)
            db.session.add(d)
            db.session.commit()

        except:
            print("ошибка")

    return render_template("create.html", title="Провести оценку")


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
        info = To.query.all()
    except:
        print("ошибка")

    return render_template("home.html", list=info)


@app.route('/posts/<int:id>')
@login_required
def post_detail(id):
    info = []
    try:
        info = To.query.all()
        info = To.query.get(id)
    except:
        print("ошибка")
    return render_template("post_detail.html", list=info)


@app.route('/remove', methods=["POST"])
@login_required
def remove():
    checked_boxes = request.form.getlist("check")
    for id in checked_boxes:
        To.query.all()
        Transmission.query.all()
        Dvs.query.all()
        transmission = Transmission.query.filter_by(id=id).first()
        dvs = Dvs.query.filter_by(id=id).first()
        to = To.query.get_or_404(id)
        try:
            db.session.delete(to)
            db.session.delete(transmission)
            db.session.delete(dvs)
            db.session.commit()
            print("После удаления:", To.query.all(), Transmission.query.all())
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
    conn = sqlite3.connect('C:/Users/Admin/PycharmProjects/diplom/rzd.db')
    df = pd.read_sql('SELECT * FROM Transmission', conn)
    df.to_excel(r'C:/Users/Admin/PycharmProjects/diplom/result.xlsx', index=False)
    transmission = Transmission.query.order_by(Transmission.id.desc()).all()
    flash('Файл успешно скачен', category='success')
    return redirect('/home')

