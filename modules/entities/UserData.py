from basicModels import *
from Publication import *
from Setting import *
from datetime import datetime


class UserData(BasicModel):
    _TABLE = 'users'
    _FIELDS_MAPPING = {
        'id': int,
        'login': str,
        'description': str,
        'avatar': str,
    }

    def get_subscriptions(self):
        subscriptions = self.query("""
                            SELECT * FROM subscriptions
                            WHERE id_subscriber = {0}
                        """.format(self._id))
        id_obj_subscriptions = [i[1] for i in subscriptions]
        subscriptions = {}
        for id_obj_subscriptions in id_obj_subscriptions:
            subscriptions[id_obj_subscriptions] = self.query("""
                        SELECT login, avatar FROM users WHERE id = {0}
                    """.format(id_obj_subscriptions))[0]
        return subscriptions

    def get_subscribers(self):
        subscriptions = self.query("""
            SELECT * FROM subscriptions
            WHERE id_obj_subscription = {0}
        """.format(self._id))
        id_subscribers = [i[0] for i in subscriptions]
        subscribers = {}
        for subscriber_id in id_subscribers:
            subscribers[subscriber_id] = self.query("""
                SELECT login, avatar FROM users WHERE id = {0}
            """.format(subscriber_id))[0]
        return subscribers

    def get_publications(self):
        publications = {}
        publications_data = self.query("""
                    SELECT * FROM publications
                    WHERE id_user = {0}
                """.format(self._id))
        for publication in publications_data:
            publications[publication[0]] = Publication(publication[0], publication[1],
                                                       publication[2], publication[3], publication[4])
        return publications

    def __init__(self, pk):
        validate_data = self.get_by_pk(pk)
        self._id = validate_data['id']
        self._login = validate_data['login']
        self._description = validate_data['description']
        self._avatar = validate_data['avatar']
        self._subscriptions = self.get_subscriptions()
        self._subscribers = self.get_subscribers()
        self._publications = self.get_publications()
        settings_data = self.query("""
            SELECT * FROM settings
            WHERE id_user = {0}
        """.format(self._id))[0]
        if settings_data[1]:
            self._bg_theme = True
        else: self._bg_theme = False
        if settings_data[2]:
            self._op_to_com = True
        else: self._op_to_com = False

    def subscribe(self, self_id):
        if self_id not in self._subscribers.keys():
            self._subscriptions[self_id] = self.query("""
                SELECT login, avatar FROM users WHERE id = {0}
            """.format(self_id))[0]

            self.query("""
                INSERT INTO subscriptions
                VALUES ({0}, {1})
            """.format(self_id, self._id))

            # Отправляем уведомление
            self.send_notifications('subscribe', self_id)

    def unsubscribe(self, self_id):
        if self_id in self._subscribers.keys():
            self.query("""
                DELETE FROM subscriptions
                WHERE id_subscriber = {0} AND id_obj_subscription = {1}
            """.format(self_id, self._id))
            del self._subscribers[self_id]

        # Отправляем уведомление
        self.send_notifications('unsubscribe', self_id)

    def send_notifications(self, type_notification, id_sender, id_publication=None):
        if type_notification == "subscribe" or type_notification == "unsubscribe":
            self.query("""
                INSERT INTO notifications (id_obj_notification, type, time, id_user, id_publication, is_read)
                VALUES ({0}, '{1}', '{2}', {3}, {4}, {5})
            """.format(self._id, type_notification, datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"),
                       id_sender, 'NULL', 0))
        else:
            self.query("""
                INSERT INTO notifications (id_obj_notification, type, time, id_user, id_publication, is_read)
                VALUES ({0}, '{1}', '{2}', {3}, {4}, {5})
            """.format(self._id, type_notification, datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"), id_sender,
                       id_publication, 0))

    def delete_notification(self, type_notification, id_sender, id_publication=None):
        if type_notification == 'like' or type_notification == 'dislike':
            self.query("""
                DELETE FROM notifications
                WHERE id_user = {0} AND id_publication = {1}
            """.format(id_sender, id_publication))

    def comment(self, id_sender, id_publication, comment_text):
        if id_publication in self._publications.keys() and self._op_to_com:
            self._publications[id_publication].comment(id_sender, comment_text)
            self.send_notifications('comment', id_sender, id_publication)

    def delete_comment(self, id_comment, id_publication, id_sender):
        # Если публикация существует и в ней есть комментарий с id_comment'ом и этот комментарий принадлежит id_sender
        if id_publication in self._publications.keys() and id_sender in self._publications[id_publication].get_comments().keys()\
                and self._publications[id_publication].get_comments()[id_sender][0] == id_comment:
            self._publications[id_publication].delete_comment(id_comment)