import sqlite3
from basicModels import *
from Publication import *
from Setting import *
from Notification import *
from UserData import *
from datetime import datetime


class SelfData(BasicModel):
    _TABLE = 'users'
    _FIELDS_MAPPING = {
        'id': int,
        'login': str,
        'description': str,
        'avatar': str,
        'email': str,
        'phone_number': str,
        'password': str,
        'registration_date': str
    }

    def update_publications(self):
        publications = {}
        publications_data = self.query("""
                    SELECT * FROM publications
                    WHERE id_user = {0}
                """.format(self._id))
        for publication in publications_data:
            publications[publication[0]] = Publication(publication[0], publication[1],
                                                       publication[2], publication[3], publication[4])
        self._publications = publications

    def update_likes(self):
        self._likes = [i[0] for i in self.query("""
                    SELECT id_publication FROM likes
                    WHERE id_user = {0}
                """.format(self._id))]

    def update_dislikes(self):
        self._dislikes =  [i[0] for i in self.query("""
                    SELECT id_publication FROM dislikes
                    WHERE id_user = {0}
                """.format(self._id))]

    def update_subscribers(self):
        subscribers = {}
        for subscriber_id in SelfData.get_subscribers(self._id):
            subscribers[subscriber_id] = SelfData.query("""
                SELECT login, avatar FROM users WHERE id = {0}
            """.format(subscriber_id))[0]
        self._subscribers = subscribers

    def update_subscriptions(self):
        subscriptions = {}
        for id_obj_subscriptions in SelfData.get_subscriptions(self._id):
            subscriptions[id_obj_subscriptions] = SelfData.query("""
                SELECT login, avatar FROM users WHERE id = {0}
            """.format(id_obj_subscriptions))[0]
        self._subscriptions = subscriptions

    def update_comments(self):
        comments = {}
        comments_data = self.query("""
            SELECT id, id_publication, comment_text, comment_time FROM comments
            WHERE id_user = {0}
        """.format(self._id))
        if len(comments_data) > 0:
            for comment in comments_data:
                try:
                    comments[comment[1]][comment[0]] = (comment[2], comment[3])
                except KeyError:
                    comments[comment[1]] = {}
                    comments[comment[1]][comment[0]] = (comment[2], comment[3])
        self._comments = comments

    def update_notifications(self):
        notifications_data = self.query("""
                    SELECT * FROM notifications
                    WHERE id_obj_notification = {0}
                """.format(self._id))
        if len(notifications_data) > 0:
            self._notifications = [Notification(i[0], i[1], i[2], i[3], i[4], i[5], i[6]) for i in notifications_data]

    def __init__(self, pk):
        validate_data = self.get_by_pk(pk)
        self._id = validate_data['id']
        self._login = validate_data['login']
        self._description = validate_data['description']
        self._avatar = validate_data['avatar']
        self._email = validate_data['email']
        self._phone_number = validate_data['phone_number']
        self._password = validate_data['password']
        self._registration_date = validate_data['registration_date']

        # Заполняем подписчиков
        self.update_subscribers()

        # Заполняем подписки
        self.update_subscriptions()

        # Заполняем собственные лайки (id публикаций на которые поставил лайк)
        self.update_likes()

        # Заполняем собственные дизлайки (id публикаций на которые поставил дизлайк)
        self.update_dislikes()

        # Заполняем публикации пользователя
        self.update_publications()

        # Заполняем комментарии пользователя
        self.update_comments()

        # Получаем настройки пользователя из таблицы
        self._setting = Setting(self.query("""
            SELECT * FROM settings
            WHERE id_user = {0}
        """.format(self._id))[0])

        # Получаем все уведомления пользователя в какую-нибудь переменную
        self.update_notifications()


    @classmethod
    def get_subscribers(cls, self_id):
        """
            Возвращает список id подписчиков
        :param self_id: Свой id
        :return:
            id_subscribers: id'шники подписчиков
        """
        subscriptions = cls.query("""
            SELECT * FROM subscriptions
            WHERE id_obj_subscription = {0}
        """.format(self_id))
        id_subscribers = [i[0] for i in subscriptions]
        return id_subscribers

    @classmethod
    def get_subscriptions(cls, self_id):
        """
            Возвращает список id объектов подписки
        :param self_id: Свой id
        :return:
            id_obj_subscriptions: id'шники подписок
        """
        subscriptions = cls.query("""
                    SELECT * FROM subscriptions
                    WHERE id_subscriber = {0}
                """.format(self_id))
        id_obj_subscriptions = [i[1] for i in subscriptions]
        return id_obj_subscriptions

    def subscribe(self, id_obj_subscription):
        """
            Позволяет подписаться на кого-то и отправить уведомление
        :param id_obj_subscriptions: id объекта подписки
        """
        if self._id != id_obj_subscription and id_obj_subscription not in self._subscriptions.keys():
            self.query("""
                INSERT INTO subscriptions
                VALUES ({0}, {1})
            """.format(self._id, id_obj_subscription))
            self._subscriptions[id_obj_subscription] = self.query("""
                SELECT login, avatar FROM users WHERE id = {0}
            """.format(id_obj_subscription))[0]

            # Отправляем уведомление
            self.send_notifications('subscribe', None, id_obj_subscription)

    def unsubscribe(self, id_obj_subscription):
        """
            Позволяет отписаться и отправить уведомление
        :param id_obj_subscription: id человека от которого нужно отписаться
        """
        if id_obj_subscription in self._subscriptions.keys():
            self.query("""
                DELETE FROM subscriptions
                WHERE id_subscriber = {0} AND id_obj_subscription = {1}
            """.format(self._id, id_obj_subscription))
            del self._subscriptions[id_obj_subscription]

            # Отправляем уведомление
            self.send_notifications('unsubscribe', None, id_obj_subscription)

    def create_publication(self, content, description):
        """
            Позволяет создать публикацию
        :param content: путь до картинки или видео
        :param description: Описание публикации
        """
        self.query("""
            INSERT INTO publications (content, description, id_user)
            VALUES ({0}, {1}, {2})
        """.format(content, description, self._id))
        self.update_publications()

    def delete_publication(self, id_publication):
        """
            Позволяет удалить свою публикацию
        :param id_publication: id публикации
        """
        if id_publication in self._publications.keys():
            self._publications[id_publication].delete()
            del self._publications[id_publication]
        self.update_likes()
        self.update_dislikes()
        self.update_comments()

    def set_like(self, id_publication):
        """
            Позволяет поставить или удалить лайк (на/c) запис(ь/и) и отправляет уведомление
        :param
            id_publication (int): id публикации
        """
        if id_publication not in self._likes:
            self._likes.append(id_publication)
            self.query("""
                INSERT INTO likes
                VALUES ({0}, {1})
            """.format(id_publication, self._id))
            if id_publication in self._dislikes:
                self._dislikes.remove(id_publication)
                self.query("""
                    DELETE FROM dislikes
                    WHERE id_publication = {0} AND id_user = {1}
                """.format(id_publication, self._id))

            # Отправляем уведомление если это пост не SelfUser
            if id_publication not in self._publications.keys():
                self.send_notifications('like', id_publication)
        else:
            self._likes.remove(id_publication)
            self.query("""
                DELETE FROM likes
                WHERE id_publication = {0} AND id_user = {1}
            """.format(id_publication, self._id))
            if id_publication not in self._publications.keys():
                self.delete_notification('like', id_publication)

    def set_dislike(self, id_publication):
        """
            Позволяет поставить или удалить дизлайк (на/c) запис(ь/и) и отправить ему уведомление
        :param
            id_publication (int): id публикации
        """
        if id_publication not in self._dislikes:
            self._dislikes.append(id_publication)
            self.query("""
                INSERT INTO dislikes
                VALUES ({0}, {1})
            """.format(id_publication, self._id))
            if id_publication in self._likes:
                self._likes.remove(id_publication)
                self.query("""
                    DELETE FROM likes
                    WHERE id_publication = {0} AND id_user = {1}
                """.format(id_publication, self._id))
            # Посылаем уведомление
            if id_publication not in self._publications.keys():
                self.send_notifications('dislike', id_publication)
        else:
            self._dislikes.remove(id_publication)
            self.query("""
                DELETE FROM dislikes
                WHERE id_publication = {0} AND id_user = {1}
            """.format(id_publication, self._id))
            # Убираем уведомление
            if id_publication not in self._publications.keys():
                self.delete_notification('like', id_publication)

    def comment(self, id_publication, text):
        """
            Позволяет комментировать свою запись
        :param id_publication: id публикации
        :param text: текст комментария
        """
        if id_publication in self._publications.keys():
            self.query("""
                INSERT INTO comments (id_publication, id_user, comment_text, comment_time)
                VALUES ({0}, {1}, '{2}', '{3}')
            """.format(id_publication, self._id, text, datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")))
            self.update_comments()

    def delete_self_comment(self, id_publication, id_comment):
        """
            Позволяет удалить свой комментарий из любой публикации
        :param id_publication: id публикации
        :param id_comment: id коммента
        """
        if id_publication in self._comments.keys():
            if id_comment in self._comments[id_publication].keys():
                del self._comments[id_publication][id_comment]
                self.query("""
                DELETE FROM comments
                WHERE id = {0}
                """.format(id_comment))

    def get_note_read_notifications(self):
        note_read_notifications = []
        for notification in self._notifications:
            if not notification.is_read():
                note_read_notifications.append(notification)
        return note_read_notifications

    def read_all_notifications(self):
        for notification in self._notifications:
            notification.make_read()

    def send_notifications(self, type_notification, id_publication=None, id_obj_notification=None):
        if type_notification == "subscribe" or type_notification == "unsubscribe":
            self.query("""
                INSERT INTO notifications (id_obj_notification, type, time, id_user, id_publication, is_read)
                VALUES ({0}, '{1}', '{2}', {3}, {4}, {5})
            """.format(id_obj_notification, type_notification, datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"),
                       self._id, 'NULL', 0))
        else:
            # Получатель
            post_owner_id = self.query("""
                SELECT id_user FROM publications
                WHERE id = {0}
            """.format(id_publication))[0][0]

            self.query("""
                INSERT INTO notifications (id_obj_notification, type, time, id_user, id_publication, is_read)
                VALUES ({0}, '{1}', '{2}', {3}, {4}, {5})
            """.format(post_owner_id, type_notification, datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"), self._id,
                       id_publication, 0))

    def delete_notification(self, id_publication, type_notification):
        if type_notification == 'like' or type_notification == 'dislike':
            self.query("""
                DELETE FROM notifications
                WHERE id_user = {0} AND id_publication = {1}
            """.format(self._id, id_publication))



if __name__ == '__main__':
    # Тест
    user1 = SelfData(4)
    # print(user1._subscribers)
    # print(user1._subscriptions)
    # print(user1._likes)
    # print(user1._dislikes)
    # print(user1._publications)
    # print(user1._likes)
    # print(user1._dislikes)
    # user1.set_like(2)
    # print(user1._likes)
    # print(user1._dislikes)
    # user1.delete_publication(1)

    # Проверка комментариев
    # print(user1._publications)
    # print(user1._comments)
    # user1.comment(0, 'Оставил новый коммент')
    # print(user1._comments)
    # user1.delete_self_comment(0, 5)
    # print(user1._comments)

    # Проверка уведомлений
    # print(user1.get_note_read_notifications())
    # user1.read_all_notifications()
    # print(user1.get_note_read_notifications())
    # user1.set_like(3)
    # user1.subscribe(2)