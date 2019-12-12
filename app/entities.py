from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# association_messages = db.Table(
#     'association_messages',
#     db.Column('id_dialog', db.Integer, db.ForeignKey('dialog.id')),
#     db.Column('id_message', db.Integer, db.ForeignKey('message.id'), primary_key=True)
# )

# association_dialog = db.Table(
#     'association_dialog',
#     db.Column('id_first', db.Integer, db.ForeignKey('user.id')),
#     db.Column('id_second', db.Integer, db.ForeignKey('user.id')),
#     db.Column('id_dialog', db.Integer, db.ForeignKey('dialog.id'), primary_key=True)
# )

association_subscriptions = db.Table(
    'association_subscriptions',
    db.Column(
        'subscriber_id',
        db.Integer,
        db.ForeignKey('user.id'),
        primary_key=True
    ),
    db.Column(
        'subscription_obj_id',
        db.Integer,
        db.ForeignKey('user.id'),
        primary_key=True
    )
)

likes = db.Table(
    'likes',
    db.Column(
        'id_publication',
        db.Integer,
        db.ForeignKey(
            'publication.id',
            ondelete='CASCADE'
        ),
        primary_key=True
    ),
    db.Column(
        'id_user',
        db.Integer,
        db.ForeignKey(
            'user.id',
            ondelete='CASCADE'
        ),
        primary_key=True
    )
)

dislikes = db.Table(
    'dislikes',
    db.Column(
        'id_publication',
        db.Integer,
        db.ForeignKey(
            'publication.id',
            ondelete='CASCADE'
        ),
        primary_key=True
    ),
    db.Column(
        'id_user',
        db.Integer,
        db.ForeignKey(
            'user.id',
            ondelete='CASCADE'
        ),
        primary_key=True
    )
)


class User(UserMixin, db.Model):
    """Класс User наследован от UserMixin, db.Model,базового класса для всех
    моделей из Flask-SQLAlchemy и содержит описание модели базы данных пользователя.

    Этот класс определяет несколько полей как переменные класса. Поля 
    создаются как экземпляры класса db.Column, который принимает тип поля в 
    качестве аргумента, а также другие уточняющие аргументы. Экземпляры
    класса db.relationship отражают взаимосвязь между базами данных
    """

    id = db.Column(db.Integer, primary_key=True, index=True)
    login = db.Column(db.String(64), index=True, unique=True, nullable=False)
    avatar = db.Column(db.String(256), default='https://s3.eu-north-1.amazonaws.com/lemmycases.ru/avatars/ricardo.jpg')
    description = db.Column(db.Text)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    registration_date = db.Column(db.DateTime(), default=datetime.utcnow)
    subscriptions = db.relationship(
        'User', secondary=association_subscriptions,
        primaryjoin=(association_subscriptions.c.subscriber_id == id),
        secondaryjoin=(association_subscriptions.c.subscription_obj_id == id),
        backref=db.backref('association_subscriptions', lazy='dynamic'),
        lazy='dynamic'
    )
    subscribers = db.relationship(
        'User', secondary=association_subscriptions,
        primaryjoin=(association_subscriptions.c.subscription_obj_id == id),
        secondaryjoin=(association_subscriptions.c.subscriber_id == id),
        lazy='dynamic'
    )
    likes = db.relationship(
        'Publication', secondary=likes,
        primaryjoin=(likes.c.id_user == id),
        lazy='dynamic'
    )
    dislikes = db.relationship(
        'Publication', secondary=dislikes,
        primaryjoin=(dislikes.c.id_user == id),
        lazy='dynamic'
    )
    publications = db.relationship('Publication', backref='author', lazy='dynamic')
    settings = db.relationship('Settings', uselist=False, backref='author')
    notifications = db.relationship('Notification', backref='recipient', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    def sub(self, user):
        """Метод класса User(UserMixin, db.Model)

        Позволяет подписаться на user, т.е. отправляет уведомление
        :param user: объект пользователя на которого нужно подписаться
        """
        if not self.is_subscribed(user):
            self.subscriptions.append(user)
            db.session.add(Notification(
                type='subscription',
                id_user=user.id,
                text="Пользователь {} подписался на вас".format(self.login))
            )
            db.session.commit()

    def count_subscriptions(self):
        """Метод класса User(UserMixin, db.Model)

        Метод возвращает количество всех подписчиков пользователя
        """
        return len(self.subscriptions.all())

    def count_subscribers(self):
        """Метод класса User(UserMixin, db.Model)

        Метод возвращает количество всех подписок пользователя
        """
        return len(self.subscribers.all())

    def count_publications(self):
        """Метод класса User(UserMixin, db.Model)

        Метод возвращает количество всех публикаций пользователя
        """
        return len(self.publications.all())

    def show_subscriptions(self):
        """Метод класса User(UserMixin, db.Model)

        Метод выводит все подписки пользователя
        """
        for user in self.subscriptions:
            print(user)

    def show_subscribers(self):
        """Метод класса User(UserMixin, db.Model)

        Метод выводит всех подписчиков пользователя
        """
        for user in self.subscribers:
            print(user)

    def unsub(self, user):
        """Метод класса User(UserMixin, db.Model)

        Позволяет отписаться от user, т.е. отправляет уведомление
        :param user: объект пользователя от которого нужно отписаться
        """
        if self.is_subscribed(user):
            self.subscriptions.remove(user)
            db.session.add(Notification(
                type='unsubscription',
                id_user=user.id,
                text="Пользователь {} отписался от вас".format(self.login)
            ))
            db.session.commit()

    def is_subscribed(self, user):
        """Метод класса User(UserMixin, db.Model)

        Проверяет, подписан ли self на user
        :param user: объект пользователя
        """
        if self.id != user.id:
            return self.subscriptions.filter(
                association_subscriptions.c.subscription_obj_id == user.id).count() > 0

    def set_pass(self, password):
        """Метод класса User(UserMixin, db.Model)

        Позволяет установить пароль и захэшировать его
        :param password: пароль
        """
        self.password_hash = generate_password_hash(password)

    def check_pass(self, password):
        """Метод класса User(UserMixin, db.Model)

        Сравнивает пароль с хэшем
        :param password: пароль
        :return:
            True: верный пароль
            False: неверный пароль
        """
        return check_password_hash(self.password_hash, password)

    def create_pub(self, description, content):
        """Метод класса User(UserMixin, db.Model)

        Позволяет создать публикацию
        :param description: описание публикации
        :param content: ссылка на фото/видео
        """
        new_publication = Publication(content=content, description=description, id_user=self.id)
        db.session.add(new_publication)
        db.session.commit()

    def show_pub(self):
        """Метод класса User(UserMixin, db.Model)

        Метод выводит все публикации пользователя
        """
        for pub in self.publications:
            print(pub)

    def get_pubs(self):
        """Метод класса User(UserMixin, db.Model)

        Метод возвращает публикации пользователя
        """
        return self.publications

    def delete_pub(self, id_publication):
        """Метод класса User(UserMixin, db.Model)

        Метод удаляет публикацию из базы данных
        """
        if self.publications.filter(Publication.id == id_publication).count() > 0:
            self.publications.filter(Publication.id == id_publication).delete()

    def set_like(self, id_publication):
        """Метод класса User(UserMixin, db.Model)

        Позволяет поставить лайк на публикацию, т.е. отправляет уведомление
        :param id_publication: id публикации
        """
        publication = Publication.query.get(id_publication)
        publication.set_like(self)
        db.session.add(Notification(
            type='like',
            id_user=publication.author.id,
            id_publication=publication.id,
            text="Пользователь {} поставил лайк на публикацию {}".format(self.login, id_publication)
        ))
        db.session.commit()

    def set_dislike(self, id_publication):
        """Метод класса User(UserMixin, db.Model)
        Позволяет поставить дизлайк на публикацию, т.е. отправляет уведомление
        :param id_publication: айди публикации
        """
        publication = Publication.query.get(id_publication)
        publication.set_dislike(self)
        db.session.add(Notification(
            type='dislike',
            id_user=publication.author.id,
            id_publication=publication.id,
            text="Пользователь {} поставил дизлайк на публикацию {}".format(self.login, id_publication)
        ))
        db.session.commit()

    def is_like(self, id_publication):
        return id_publication in self.likes

    def is_dislike(self, id_publication):
        return id_publication in self.dislikes

    def create_comment(self, id_publication, text):
        """Метод класса User(UserMixin, db.Model)
        Позволяет создать комментарий, т.е. отправляет уведомление
        :param id_publication: айди публикации
        :param text: текст комментария
        """
        publication = Publication.query.get(id_publication)
        if publication.author.settings.op_to_com or publication.author == self:
            comment_id = publication.set_comment(self, text)
            db.session.add(Notification(type='comment',
                                        id_user=publication.author.id,
                                        id_publication=publication.id,
                                        text="Пользователь {} оставил комментарий на публикацию {}".format(self.login,
                                                                                                           id_publication)
                                        ))
            db.session.commit()
            return comment_id

    @classmethod
    def delete_comment(cls, id_comment):
        """Метод класса User(UserMixin, db.Model)

        Метод удаляет комментарий из базы данных
        """
        Comment.query.filter(Comment.id == id_comment).delete()

    def change_ea(self):
        self.settings.email_alerts_change()

    def change_otc(self):
        self.settings.op_to_com_change()

    def show_notification(self, **kwargs):
        """Метод класса User(UserMixin, db.Model)

        Позволяет просмотреть уведомления
        :param kwargs:
            read=True (показать прочитанные уведомления)
            read=False (показать непрочитанные уведомления)
            read=None (показать все уведомления)
        """
        if kwargs.get('read') is None:
            for notification in self.notifications:
                print(notification)
        elif kwargs.get('read'):
            for notification in self.notifications:
                if notification.read:
                    print(notification)
        elif not kwargs.get('read'):
            for notification in self.notifications:
                if not notification.read:
                    print(notification)

    def read_notification(self, id_notification=None):
        """Метод класса User(UserMixin, db.Model)

        Позволяет прочитать уведомлени(е/я)
        :param id_notification: айди уведомления (если необходимо удалить выборочно)
        """
        if not id_notification:
            for notification in self.notifications:
                notification.read = True
        else:
            for notification in self.notifications:
                if notification.id == id_notification:
                    notification.read = True
                    break
        db.session.commit()

    # ---------------------------------------------------

    def get_message_lists(self):
        pass

    # def send_message(self, id_recipient, text):
    #     msg_list = None
    #     for message_list in self.message_lists:
    #         if message_list.id_user == self.id:
    #             message_list.id_first_user == id_recipient
    #             and message_list.id_second_user == self.id
    #             or message_list.id_first_user == self.id
    #             and message_list.id_second_user == id_recipient
    #         ):
    #             msg_list = message_list
    #             break
    #     if msg_list:
    #         new_message = Message(id_sender=self.id, id_message_list=msg_list.id, text=text)
    #         db.session.add(new_message)
    #     else:
    #         new_message_list = MessageList(id_first_user=self.id, id_second_user=id_recipient)
    #         db.session.add(new_message_list)
    #         db.session.add(Message(id_sender=self.id, id_message_list=new_message_list.id, text=text))
    #     db.session.commit()
    #
    # def delete_message(self, id_recipient , id_message):
    #     msg_list = None
    #     for message_list in self.message_lists:
    #         if (
    #                 message_list.id_first_user == id_recipient
    #                 and message_list.id_second_user == self.id
    #                 or message_list.id_first_user == self.id
    #                 and message_list.id_second_user == id_recipient
    #         ):
    #             msg_list = message_list
    #             break
    #     if msg_list:
    #         for message in msg_list:
    #             if message.id == id_message:
    #                 message.delete()
    #                 db.session.commit()
    #                 break

    def __repr__(self):
        """Метод класса User(UserMixin, db.Model)
        
        Метод __repr__ сообщает, как печатать объекты этого класса
        """
        return '<User {}>'.format(self.login)


class Publication(db.Model):
    """Класс Publication наследован от db.Model,базового класса для всех
    моделей из Flask-SQLAlchemy и содержит описание модели базы данных публикации.

    Этот класс определяет несколько полей как переменные класса. Поля 
    создаются как экземпляры класса db.Column, который принимает тип поля
    в качестве аргумента, а также другие уточняющие аргументы. Экземпляры
    класса db.relationship отражают взаимосвязь между базами данных
    """

    id = db.Column(db.Integer, primary_key=True, index=True)
    content = db.Column(db.String(256), default='/static/publications/default.jpg')
    description = db.Column(db.Text)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    publication_date = db.Column(db.DateTime(), default=datetime.utcnow)
    likes = db.relationship(
        'User', secondary=likes,
        primaryjoin=(likes.c.id_publication == id),
        lazy='dynamic')
    dislikes = db.relationship(
        'User', secondary=dislikes,
        primaryjoin=(dislikes.c.id_publication == id),
        lazy='dynamic')
    comments = db.relationship('Comment', backref='publication', lazy='dynamic')

    def set_like(self, user):
        """Метод класса Publication(db.Model)
        
        Метод проверяет принадлежит ли лайк или дизлайк пользователю и добавить 
        его в спискок или удалить
        """
        if user in self.likes:
            self.likes.remove(user)
        elif user in self.dislikes:
            self.dislikes.remove(user)
            self.likes.append(user)
        else:
            self.likes.append(user)
        db.session.commit()

    def set_dislike(self, user):
        """Метод класса Publication(db.Model)
        
        Метод проверяет принадлежит ли лайк или дизлайк пользователю и добавить 
        его в спискок или удалить
        """
        if user in self.dislikes:
            self.dislikes.remove(user)
        elif user in self.likes:
            self.likes.remove(user)
            self.dislikes.append(user)
        else:
            self.dislikes.append(user)
        db.session.commit()

    def set_comment(self, user, text):
        """Метод класса Publication(db.Model)
        
        Метод позволяет добавить комменатрий к публикации
        """
        new_comment = Comment(id_publication=self.id, id_user=user.id, text=text)
        db.session.add(new_comment)
        return new_comment.id

    def show_likes(self):
        """Метод класса Publication(db.Model)
        
        Метод выводит пользователя, если лайк принадлежит ему
        """
        for user in self.likes:
            print(user)

    def show_dislikes(self):
        """Метод класса Publication(db.Model)
        
        Метод выводит пользователя, если дизлайк принадлежит ему
        """
        for user in self.dislikes:
            print(user)

    def show_comments(self):
        """Метод класса Publication(db.Model)
        
        Метод выводит пользователя, если комментарий принадлежит ему
        """
        for user in self.comments:
            print(user)

    def has_like(self, id_user):
        user = User.query.get(int(id_user))
        if user in self.likes.all():
            return True
        return False

    def has_dislike(self, id_user):
        user = User.query.get(int(id_user))
        if user in self.dislikes.all():
            return True
        return False

    def count_likes(self):
        return len(self.likes.all())

    def count_dislikes(self):
        return len(self.dislikes.all())

    def get_comments(self, for_user):
        result = []
        for comment in self.comments:
            result.append({
                'login': comment.author.login,
                'avatar': comment.author.avatar,
                'comment_text': comment.text,
                'comment_time': comment.time,
                'comment_id': comment.id,
                'op_to_delete': True if comment.author == for_user else False
            })
        return result

    def __repr__(self):
        """Метод класса User(UserMixin, db.Model)
        
        Метод __repr__ сообщает, как печатать объекты этого класса
        """
        return '<Publication {} from {}>'.format(self.id, self.author)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    id_publication = db.Column(db.Integer, db.ForeignKey('publication.id', ondelete='CASCADE'), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    text = db.Column(db.String, nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        """Метод класса User(UserMixin, db.Model)
        
        Метод __repr__ сообщает, как печатать объекты этого класса
        """
        return '<Comment {} on publication {} from user {}>'.format(self.id, self.id_publication, self.id_user)


class Settings(db.Model):
    """Класс Settings наследован от db.Model,базового класса для всех
    моделей из Flask-SQLAlchemy и содержит описание модели базы данных настроек.

    Этот класс определяет несколько полей как переменные класса. Поля 
    создаются как экземпляры класса db.Column, который принимает тип поля
    в качестве аргумента, а также другие уточняющие аргументы. Экземпляры
    класса db.relationship отражают взаимосвязь между базами данных
    """

    id_user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, primary_key=True,
                        index=True)
    op_to_com = db.Column(db.Boolean, default=True)
    email_alerts = db.Column(db.Boolean, default=True)

    def email_alerts_change(self):
        self.email_alerts = not self.email_alerts

    def op_to_com_change(self):
        self.op_to_com = not self.op_to_com

    def __repr__(self):
        """Метод класса User(UserMixin, db.Model)
        
        Метод __repr__ сообщает, как печатать объекты этого класса
        """
        return '<Settings {} EO = {}, OTC={}>'.format(self.author, self.email_alerts, self.op_to_com)


class Notification(db.Model):
    """Класс Notification наследован от db.Model,базового класса для всех
    моделей из Flask-SQLAlchemy и содержит описание модели базы данных уведомлений.
    Этот класс определяет несколько полей как переменные класса. Поля
    создаются как экземпляры класса db.Column, который принимает тип поля
    в качестве аргумента, а также другие уточняющие аргументы. Экземпляры
    класса db.relationship отражают взаимосвязь между базами данных
    """
    id = db.Column(db.Integer, primary_key=True, index=True)
    type = db.Column(db.String(32), nullable=False)
    id_publication = db.Column(db.Integer, db.ForeignKey('publication.id', ondelete='CASCADE'))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    text = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        """Метод класса User(UserMixin, db.Model)

        Метод __repr__ сообщает, как печатать объекты этого класса
        """
        return '<Notification {} with type {} for user {} ~ read = {}>'.format(self.id, self.type, self.id_user,
                                                                               self.read)


# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     sender = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
#     text = db.Column(db.String, nullable=False)
#     date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     read = db.Column(db.Boolean, default=False)
#
#     def read_message(self):
#         self.read = True
#
#     # def get_sender(self):
#     #     return User.query.get(self.id_sender)


# class Dialog(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     delete_first = db.Column(db.Boolean, default=False)
#     delete_second = db.Column(db.Boolean, default=False)
#     id_user_first = db.Column(db.Integer, db.ForeignKey('user.id', name='user_first', ondelete='CASCADE'))
#     id_user_second = db.Column(db.Integer, db.ForeignKey('user.id', name='user_second', ondelete='CASCADE'))
#     messages = db.relationship(
#         'Message', secondary=association_messages,
#         primaryjoin=(association_messages.c.id_dialog == id),
#         backref=db.backref('dialog', lazy='dynamic'),
#         lazy='dynamic'
#     )


@login.user_loader
def load_user(id):
    """Функция загрузчика пользователя.
       
    Функцию можно вызвать для загрузки пользователя, передав в её аргумент
    идентификатор (id) пользователя.
    """
    return User.query.get(int(id))
