from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.entities import User, Publication
from werkzeug.urls import url_parse
# from config import S3_BUCKET, S3_KEY, S3_SECRET
import boto3

# s3 = boto3.client(
#     's3',
#     aws_access_key_id=S3_KEY,
#     aws_secret_access_key=S3_SECRET,
# )


@app.route('/')
@app.route('/home')
def home():
    pub = Publication.query.order_by(Publication.id.desc()).all()
    return render_template("home.html", publication = pub)

@login_required
@app.route("/profile_<login>")
def profile(login):
    if login == current_user.login:
        return render_template("current_profile.html", user=current_user)
    else:
        return render_template("profile.html", user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile', login = current_user.login))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data.lower()).first()
        if user is None or not user.check_pass(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('profile', login = current_user.login)
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
        user = User(login=form.login.data.lower(), email=form.email.data, phone_number=form.phone.data)
        user.set_pass(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Register', form=form)


@login_required
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template("settings.html", user=current_user)


@login_required
@app.route('/setting<setting>', methods=['POST'])
def setting_change(setting):
    if setting == 'ea':
        current_user.change_ea()
        db.session.commit()
    else:
        current_user.change_otc()
        db.session.commit()
    return ''

@login_required
@app.route('/add_publication', methods=['POST'])
def add_publication():
    pub = request.get_json()
    toCom = Publication(content=pub['link'], description=pub['description'], id_user=current_user.id)
    db.session.add(toCom)
    db.session.commit()
    return ""


# @login_required
# @app.route('/upload', methods=['POST'])
# def upload_avatar():
#     file = request.files['file']
#     expansion = ''
#     if file.filename[-4:] == '.png':
#         expansion = '.png'
#     elif file.filename[-4:] == '.jpg':
#         expansion = '.jpg'
#     elif file.filename[-5:] == '.jpeg':
#         expansion = '.jpeg'
#     if expansion:
#         s3_cli = boto3.client('s3',
#              aws_access_key_id=S3_KEY,
#              aws_secret_access_key= S3_SECRET)
#         s3_cli.put_object(Body=file, ACL='public-read', Bucket='lemmycases.ru', Key='avatars/{}'.format(current_user.login + expansion))
#         current_user.avatar = "https://s3.eu-north-1.amazonaws.com/lemmycases.ru/avatars/{}".format(current_user.login + expansion)
#         db.session.commit()
#     else:
#         flash('Выберите фотографию с форматом .jpg, .jpeg или .png')

#     return redirect(url_for('settings'))


@app.route("/id<prof_id>", methods=['GET', 'POST'])
def check_profile(prof_id):
    exists = db.session.query(User).filter_by(id=prof_id)
    if exists.scalar() != None:
        return render_template("profile.html", user=exists.first())
    else:
        return "Пользователь не найден"
