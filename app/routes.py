from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db, socketio
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.entities import User, Publication, Settings, Comment, datetime, Notification
from werkzeug.urls import url_parse
from config import S3_BUCKET, S3_KEY, S3_SECRET
import boto3, json

s3 = boto3.client(
    's3',
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET,
)


@app.route('/')
@app.route('/home')
def home():
    '''Рендер html шаблона home.html

    Функция внутри себя принимает имя файла шаблона и переменную, являющуюся
    аргументом шаблона, а затем генерирует указанный html шаблон, заменив его
    заполнители фактическими значениями.
    '''
    notifs = db.session.query(Notification.id, Notification.text, Publication.content).join(Publication,  Publication.id == Notification.id_publication).filter_by(id_user = current_user.id).filter(Notification.read == False).order_by(Notification.id.desc()).all()
    pubs = []
    if current_user.is_authenticated:
        for subscription in current_user.subscriptions:
            for publication in subscription.publications.all():
                pubs.insert(0, publication)
                if len(pubs) == 10:
                    return render_template("home.html", publication=pubs, user=current_user, page='home', notifications_a = notifs)
    else:
        return redirect(url_for('login'))

    return render_template("home.html", publication=pubs, user=current_user, page='home', notifications_a = notifs, unread_count = len(notifs))


@login_required
@app.route("/profile_<login>")
def profile(login):
    '''Рендер html шаблона profile.html

    Аргумент функции - другая функция "Login"
    Функция внутри себя принимает имя файла шаблона и переменную, являющуюся
    аргументом шаблона, а затем генерирует указанный html шаблон, заменив его
    заполнители фактическими значениями.
    '''
    notifs = db.session.query(Notification.id, Notification.text, Publication.content).join(Publication,  Publication.id == Notification.id_publication).filter_by(id_user = current_user.id).filter(Notification.read == False).order_by(Notification.id.desc()).all()
    return render_template("profile.html",
                           user=User.query.filter_by(login=login).first(),
                           indexes=[3 * i - 2 for i in range(1, 1000)],
                           page='profile',
                           notifications_a = notifs,
                           unread_count = len(notifs)
                           )


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Функция входа в систему (авторизации)
    
    Для авторизованных пользователей, функция осуществяляет перенаправление
    пользователя на страницу профиля. Проверка производится с помощью выражения
    "current_user.is_authenticated". Переменная current_user поступает из Flask-Login.

    В другом случае происход обработка формы LoginForm(). Когда браузер получает
    запрос POST в результате нажатия пользователем кнопки submit функция отправляет
    запрос в базу данных с введенными в форму аторизации параметрами.
    Если пользователь не найден, то функция перенаправляет его обратно на
    страницу авторизации, иначе на страницу проифиля.

    Функция внутри себя принимает имя файла шаблона и переменную, являющуюся
    аргументом шаблона, а затем генерирует html шаблон в соответствии с выполненными 
    условиями, заменив его заполнители фактическими значениями.
    '''
    if current_user.is_authenticated:
        return redirect(url_for('profile', login=current_user.login))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data.lower()).first()
        if user is None or not user.check_pass(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('profile', login=current_user.login)
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


# def authenticated():                           #попытка зафункционалить
#     '''Возвращает True или False'''
#     return current_user.is_authenticated
# def validate(form):
#     '''Возвращает True или False'''
#     return form.validate_on_submit()
# def get_user(form):
#     return User.query.filter_by(login=form.login.data.lower()).first()
# def chek_pass(usr,form):
#     '''Возвращает True или False'''
#     return usr.check_pass(form.password.data)
# def authentication(form):
#     if get_user(LoginForm()) and chek_pass(get_user(LoginForm()),LoginForm()):
#         login_user(get_user(), remember=form.remember_me.data)
#         next_page = request.args.get('next')
#     else:
#         flash('Invalid username or password')
#         return redirect(url_for('login'))
#     if not next_page or url_parse(next_page).netloc != '':
#         next_page = url_for('profile', login=current_user.login)
#     return redirect(next_page)    
# def render(form)
#     return render_template('login.html', title='Sign In', form=form)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if authenticated():
#         return redirect(url_for('profile', login=current_user.login))
#     authentication(LoginForm()) if validate(LoginForm()) else render(LoginForm())


@login_required
@app.route('/logout')
def logout():
    '''Функция выхода из системы'''
    logout_user()
    return redirect(url_for('login'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    '''Функция регистрации пользователя
    
    Для авторизованных пользователей, функция осуществяляет перенаправление
    пользователя на страницу профиля. Проверка производится с помощью выражения
    "current_user.is_authenticated". Переменная current_user поступает из Flask-Login.

    В другом случае происход обработка формы RegistrationForm(). Когда браузер получает
    запрос POST в результате нажатия пользователем кнопки submit функция создает нового 
    пользователя с именем, электронной почтой и паролем, записывает их в базу данных и 
    затем перенаправляет запрос на вход, чтобы пользователь мог войти в систему.
    '''
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(login=form.login.data.lower(), email=form.email.data)
        user.set_pass(form.password.data)
        db.session.add(user)
        db.session.commit()
        user_settings = Settings(id_user=user.id)
        db.session.add(user_settings)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Register', form=form)


@login_required
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    notifs = db.session.query(Notification.id, Notification.text, Publication.content).join(Publication,  Publication.id == Notification.id_publication).filter_by(id_user = current_user.id).filter(Notification.read == False).order_by(Notification.id.desc()).all()
    '''Рендер html шаблона settings.html

    Функция внутри себя принимает имя файла шаблона и переменную, являющуюся
    аргументом шаблона, а затем генерирует указанный html шаблон, заменив его
    заполнители фактическими значениями.
    '''
    return render_template("settings.html", user=current_user, notifications_a = notifs, unread_count = len(notifs))


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
    '''Функция добавления публикации

    Функция запрашивает файл с помощью модуля request и устанавливает
    расширение запрашиваемого файла.

    При соответсвии формата файла заданным условиям публикация создаётся
    и отправляется на сервер. При ошибочном формате публикация не создаётся.

    Функция возвращает объект формата json
    '''
    pub = request.files['newPub']
    expansion = ''
    if pub.filename[-4:] == '.png':
        expansion = '.png'
    elif pub.filename[-4:] == '.jpg':
        expansion = '.jpg'
    elif pub.filename[-5:] == '.jpeg':
        expansion = '.jpeg'
    if expansion:
        key = '{}/{}'.format(current_user.login.lower(), datetime.utcnow().strftime('%B_%d_%Y-%H_%M_%S') + expansion)
        s3.put_object(Body=pub, ACL='public-read', Bucket='lemmycases.ru',
                      Key=key)
        current_user.create_pub(
            description=request.form['description'],
            content="https://s3.eu-north-1.amazonaws.com/lemmycases.ru/{}".format(key)
        )
        rqst = {
            'ref': current_user.get_pubs()[-1].content,
            'id': current_user.get_pubs()[-1].id
        }
    else:
        rqst = {
            'error': 'Неверный формат!'
        }
    return json.dumps(rqst)


@login_required
@app.route('/like<pub_id>', methods=['POST'])
def likes(pub_id):
    current_user.set_like(int(pub_id))
    return ""


@login_required
@app.route('/dislike<pub_id>', methods=['POST'])
def dislikes(pub_id):
    current_user.set_dislike(int(pub_id))
    return ""


@login_required
@app.route('/pub_info<pub_id>', methods=['GET'])
def pub_info(pub_id):
    pub = Publication.query.filter_by(id=int(pub_id)).first()
    user = User.query.filter_by(id=pub.id_user).first()
    response = {
        "publication_date": pub.publication_date,
        "description": pub.description,
        "count_likes": pub.count_likes(),
        "count_dislikes": pub.count_dislikes(),
        "comments": pub.get_comments(current_user),
        "current_user_like": pub.has_like(current_user.id),
        "current_user_dislike": pub.has_dislike(current_user.id),
        "user_login": user.login,
        "user_avatar": user.avatar,
        "is_current_user": current_user.id == user.id,
        "op_to_com": user.settings.op_to_com
    }
    return jsonify(response)


@login_required
@app.route('/pub_delete<pub_id>', methods=['POST'])
def pub_delete(pub_id):
    pub_content = Publication.query.get(int(pub_id))
    pub_content = pub_content.content.split('/')[-2:]
    key = '{}/{}'.format(pub_content[0], pub_content[1])
    # example = 'https://s3.eu-north-1.amazonaws.com/lemmycases.ru/kitty/December_11_2019-08_22_21.jpg'
    s3.delete_object(Bucket='lemmycases.ru',
                     Key=key)
    current_user.delete_pub(int(pub_id))
    db.session.commit()
    response = {
        'status': 'ok'
    }
    return jsonify(response)


@login_required
@app.route('/unsub<login>', methods=['POST'])
def unsub(login):
    user = User.query.filter_by(login=login).first()
    current_user.unsub(user)
    response = {
        'status': 'ok'
    }
    db.session.commit()
    return jsonify(response)


@login_required
@app.route('/sub<login>', methods=['POST'])
def sub(login):
    user = User.query.filter_by(login=login).first()
    current_user.sub(user)
    response = {
        'status': 'ok'
    }
    db.session.commit()
    return jsonify(response)


@login_required
@app.route('/upload', methods=['POST'])
def upload_avatar():
    '''Функция загрузки аватара

    Функция запрашивает файл с помощью модуля request и устанавливает
    расширение запрашиваемого файла.

    При соответсвии формата файла заданным условиям аватар загружаетя в профиль.
    При ошибочном формате аватар не загружается.

    Функция возвращает ссылку '/settings'
    '''
    file = request.files['file']
    expansion = ''
    if file.filename[-4:] == '.png':
        expansion = '.png'
    elif file.filename[-4:] == '.jpg':
        expansion = '.jpg'
    elif file.filename[-5:] == '.jpeg':
        expansion = '.jpeg'
    if expansion:
        s3.put_object(Body=file, ACL='public-read', Bucket='lemmycases.ru',
                      Key='avatars/{}'.format(current_user.login + expansion))
        current_user.avatar = "https://s3.eu-north-1.amazonaws.com/lemmycases.ru/avatars/{}".format(
            current_user.login + expansion)
        db.session.commit()
    else:
        flash('Выберите фотографию с форматом .jpg, .jpeg или .png')

    return redirect(url_for('settings'))


@login_required
@app.route('/subscribers_<user>')
def subscribers(user):
    '''Рендер html шаблона subscribers.html
    
    Функция внутри себя принимает имя файла шаблона и переменную, являющуюся
    аргументом шаблона, а затем генерирует указанный html шаблон для конкретного 
    пользователя, заменив его заполнители фактическими значениями.
    '''
    notifs = db.session.query(Notification.id, Notification.text, Publication.content).join(Publication,  Publication.id == Notification.id_publication).filter_by(id_user = current_user.id).filter(Notification.read == False).order_by(Notification.id.desc()).all()
    usr = User.query.filter_by(login=user).first()
    return render_template('subscribers.html', user=usr, var='subscribers', notifications_a = notifs, unread_count = len(notifs))


@login_required
@app.route('/subscriptions_<user>')
def subscriptions(user):
    '''Рендер html шаблона subscribers.html

    Функция внутри себя принимает имя файла шаблона и переменную, являющуюся
    аргументом шаблона, а затем генерирует указанный html шаблон, заменив его
    заполнители фактическими значениями.
    '''
    usr = User.query.filter_by(login=user).first()
    notifs = db.session.query(Notification.id, Notification.text, Publication.content).join(Publication,  Publication.id == Notification.id_publication).filter_by(id_user = current_user.id).filter(Notification.read == False).order_by(Notification.id.desc()).all()
    return render_template('subscribers.html', user=usr, var='subscriptions', notifications_a = notifs, unread_count = len(notifs))


@login_required
@app.route('/MorePublication<series>', methods=["GET"])
def MorePublicationPlease(series):
    response = {}
    i = 0
    for subscription in current_user.subscriptions:
        for publication in subscription.publications.all():
            i += 1
            if i > int(series):
                response[publication.id] = {
                    "Content": publication.content,
                    "User_login": publication.author.login
                }
                if len(response.keys()) == 10:
                    return jsonify(response)
    return jsonify(response)


@login_required
@app.route('/Comment<pub_id>/<txt>', methods=["GET"])
def PubComment(pub_id, txt):
    comment_id = current_user.create_comment(int(pub_id), txt)
    db.session.commit()
    response = {
        "Login": current_user.login,
        "Avatar": current_user.avatar,
        "id": comment_id
    }
    return jsonify(response)


@login_required
@app.route('/comment_delete<comment_id>', methods=["GET"])
def comment_delete(comment_id):
    comment = Comment.query.get(int(comment_id))
    if comment.publication.author == current_user or comment.author == current_user:
        User.delete_comment(comment_id)
        db.session.commit()
        return {
            'msg': 'successfully'
        }
    return {
        'msg': 'unsuccessfully'
    }

@login_required
@app.route('/change_description', methods=["POST"])
def change_description():
    new_description = request.form.get('description')
    current_user.description = new_description
    db.session.commit()
    return {
        'status': 'successfully'
    }

@login_required
@app.route('/chat')
def sessions():
    user = current_user
    notifs = db.session.query(Notification.id, Notification.text, Publication.content).join(Publication,  Publication.id == Notification.id_publication).filter_by(id_user = current_user.id).filter(Notification.read == False).order_by(Notification.id.desc()).all()
    return render_template('session.html', user=user, notifications_a = notifs, unread_count = len(notifs))


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

@login_required
@app.route('/notif_<user_login>', methods=["GET"])
def Notifications(user_login):
    notifs1 = db.session.query(Notification.id, Notification.text, Publication.content).join(Publication,  Publication.id == Notification.id_publication).filter_by(id_user = current_user.id).filter(Notification.read == False).order_by(Notification.id.desc()).all()
    if current_user.login == user_login:
        notifs = db.session.query(Notification.id, Notification.text, Publication.content).join(Publication,  Publication.id == Notification.id_publication).filter_by(id_user = current_user.id).order_by(Notification.id.desc()).all()
        return render_template("all_notif.html", notifications = notifs, notifications_a = notifs1, unread_count = len(notifs1))
    else:
        return render_template("all_notif.html", notifications = None, notifications_a = notifs1, unread_count = len(notifs1))

@login_required
@app.route('/notif_read_<notification_id>', methods=["GET"])
def NotificationRead(notification_id):
    current_user.read_notification(None)
    db.session.commit()
    response = {
        'status': 'ok'
    }
    return jsonify(response)
