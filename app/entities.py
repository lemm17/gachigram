from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

association_subscriptions = db.Table('association_subscriptions',
                       db.Column('subscriber_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                       db.Column('subscription_obj_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                       )

likes = db.Table('likes',
                       db.Column('id_publication', db.Integer, db.ForeignKey('publication.id'), primary_key=True),
                       db.Column('id_user', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                       )

dislikes = db.Table('dislikes',
                       db.Column('id_publication', db.Integer, db.ForeignKey('publication.id'), primary_key=True),
                       db.Column('id_user', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                       )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), index=True, unique=True, nullable=False)
    avatar = db.Column(db.String(256), default='/static/avatars/ricardo.jpg')
    description = db.Column(db.Text)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    phone_number = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256))  # , nullable=False)
    registration_date = db.Column(db.DateTime(), default=datetime.utcnow)
    subscriptions = db.relationship(
        'User', secondary=association_subscriptions,
        primaryjoin=(association_subscriptions.c.subscriber_id == id),
        secondaryjoin=(association_subscriptions.c.subscription_obj_id == id),
        backref=db.backref('association_subscriptions', lazy='dynamic'), lazy='dynamic')
    subscribers = db.relationship(
        'User', secondary=association_subscriptions,
        primaryjoin=(association_subscriptions.c.subscription_obj_id == id),
        secondaryjoin=(association_subscriptions.c.subscriber_id == id),
        lazy='dynamic')
    likes = db.relationship(
        'Publication', secondary=likes,
        primaryjoin=(likes.c.id_user == id),
        lazy='dynamic')
    dislikes = db.relationship(
        'Publication', secondary=dislikes,
        primaryjoin=(dislikes.c.id_user == id),
        lazy='dynamic')
    publications = db.relationship('Publication', backref='author', lazy='dynamic')

    def sub(self, user):
        if not self.is_subscribed(user):
            self.subscriptions.append(user)

    def show_subscriptions(self):
        for user in self.subscriptions:
            print(user)

    def show_subscribers(self):
        for user in self.subscribers:
            print(user)

    def unsub(self, user):
        if self.is_subscribed(user):
            self.subscriptions.remove(user)

    def is_subscribed(self, user):
        return self.subscriptions.filter(
            association_subscriptions.c.subscription_obj_id == user.id).count() > 0

    def set_pass(self, password):
        self.password_hash = generate_password_hash(password)

    def check_pass(self, password):
        return check_password_hash(self.password_hash, password)

    def create_pub(self, description, content=None):
        if not content:
            new_publication = Publication(description=description, id_user=self.id)
        else:
            new_publication = Publication(content=content, description=description, id_user=self.id)
        db.session.add(new_publication)

    def show_pub(self):
        for pub in self.publications:
            print(pub)

    def delete_pub(self, id_publication):
        if self.publications.filter(Publication.id == id_publication).count() > 0:
            db.session.query(Publication).filter(Publication.id == id_publication).delete()

    def set_like(self, id_publication, user):
        for publication in self.publications:
            if publication.id == id_publication:
                publication
                break

    def __repr__(self):
        return '<User {}>'.format(self.login)


class Publication(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(256), default='/static/publications/default.jpg')
    description = db.Column(db.Text)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.relationship(
        'User', secondary=likes,
        primaryjoin=(likes.c.id_publication == id),
        lazy='dynamic')
    dislikes = db.relationship(
        'User', secondary=dislikes,
        primaryjoin=(dislikes.c.id_publication == id),
        lazy='dynamic')

    def set_like(self, user):
        pass



    def __repr__(self):
        return '<Publication with id{} from user {}>'.format(self.id, self.id_user)
#
# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     id_publication = db.Column(db.Integer, db.ForeignKey('publication.id'), nullable=False)
#     id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     text = db.Column(db.String, nullable=False)
#     date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#
#     def __repr__(self):
#         return '<Comment {} on publication {} from user {}>'.format(self.id, self.id_publication, self.id_user)
#
#
# class Notification(db.Model):
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     type = db.Column(db.String(32), nullable=False)
#     id_publication = db.Column(db.Integer, db.ForeignKey('publication.id'))
#     id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#
#     def __repr__(self):
#         return '<Notification {} with type {} from user {}>'.format(self.id, self.type, self.id_user)
