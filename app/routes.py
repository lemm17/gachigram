from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import *


@app.route('/')
@app.route('/index')
def index():
    return "Hello world!"


@app.route("/home")
def profile():
    return render_template("profile.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/home')
    return render_template('login.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    return render_template('registration.html', form=form)
