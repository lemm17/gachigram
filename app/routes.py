from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.entities import User
from werkzeug.urls import url_parse


@app.route('/')
@app.route("/home")
@login_required
def home():
    return render_template("profile.html", user = current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user is None or not user.check_pass(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(login=form.login.data, email=form.email.data, phone_number=form.phone.data)
        user.set_pass(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Register', form=form)

@app.route("/id<prof_id>", methods=['GET', 'POST'])
def check_profile(prof_id):
    exists = db.session.query(User).filter_by(id=prof_id)
    if exists.scalar() != None:
        return render_template("profile.html", user = exists.first())
    else:
        return "Пользователь не найден"

