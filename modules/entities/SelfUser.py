import sqlite3
from basicModels import *
from Publication import *
from Setting import *


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
                                                       publication[2], publication[3])
        return publications

    def update_likes(self):
        return [i[0] for i in self.query("""
                    SELECT id_publication FROM likes
                    WHERE id_user = {0}
                """.format(self._id))]

    def update_dislikes(self):
        return [i[0] for i in self.query("""
                    SELECT id_publication FROM dislikes
                    WHERE id_user = {0}
                """.format(self._id))]

    def update_subscribers(self):
        subscribers = {}
        for subscriber_id in SelfData.get_subscribers(self._id):
            subscribers[subscriber_id] = SelfData.query("""
                SELECT login, avatar FROM users WHERE id = {0}
            """.format(subscriber_id))[0]
        return subscribers

    def update_subscriptions(self):
        subscriptions = {}
        for id_obj_subscriptions in SelfData.get_subscriptions(self._id):
            subscriptions[id_obj_subscriptions] = SelfData.query("""
                SELECT login, avatar FROM users WHERE id = {0}
            """.format(id_obj_subscriptions))[0]
        return subscriptions

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
        self._subscribers = self.update_subscribers()

        # Заполняем подписки
        self._subscriptions = self.update_subscriptions()

        # Заполняем собственные лайки (id публикаций на которые поставил лайк)
        self._likes = self.update_likes()

        # Заполняем собственные дизлайки (id публикаций на которые поставил дизлайк)
        self._dislikes = self.update_dislikes()

        # Заполняем публикации пользователя
        self._publications = self.update_publications()

        # Получаем настройки пользователя из таблицы
        self._setting = Setting(self.query("""
            SELECT * FROM settings
            WHERE id_user = {0}
        """.format(self._id))[0])

        # Получить все уведомления пользователя в какую-нибудь переменную

    @classmethod
    def _create_mapping(cls):
        cls.query("""
            CREATE TABLE IF NOT EXISTS users
            (id INTEGER, login TEXT, description TEXT, avatar TEXT, email TEXT,
            phone_number TEXT, password TEXT, registration_date TEXT,
            PRIMARY KEY (id))
        """)

    @classmethod
    def get_subscribers(cls, self_id):
        """
            Возвращает список id подписчиков
        :param
            self_id (int): Свой id
        :return:
            id_subscribers (list): id'шники подписчиков
        """
        subscriptions = cls.query("""
            SELECT * FROM subscriptions
            WHERE id_obj_subscription = {0}
        """.format(self_id))
        print(subscriptions)
        id_subscribers = [i[0] for i in subscriptions]
        return id_subscribers

    @classmethod
    def get_subscriptions(cls, self_id):
        """
            Возвращает список id объектов подписки
        :param
            self_id (int): Свой id
        :return:
            id_obj_subscriptions (list): id'шники подписок
        """
        subscriptions = cls.query("""
                    SELECT * FROM subscriptions
                    WHERE id_subscriber = {0}
                """.format(self_id))
        id_obj_subscriptions = [i[1] for i in subscriptions]
        return id_obj_subscriptions

    def subscribe(self, id_obj_subscriptions):
        """
            Позволяет подписаться на кого-то
        :param
            id_obj_subscriptions (int): id объекта подписки
        """
        if self._id != id_obj_subscriptions and id_obj_subscriptions not in self._subscriptions.keys():
            self.query("""
                INSERT INTO subscriptions
                VALUES ({0}, {1})
            """.format(self._id, id_obj_subscriptions))
            self._subscriptions[id_obj_subscriptions] = self.query("""
                SELECT login, avatar FROM users WHERE id = {0}
            """.format(id_obj_subscriptions))[0]

    # Метод отписки

    def create_publication(self, content, description):
        self.query("""
            INSERT INTO publications (content, description, id_user)
            VALUES ({0}, {1}, {2})
        """.format(content, description, self._id))
        self._publications = self.update_publications()

    def delete_publication(self, id_publication):
        if id_publication in self._publications.keys():
            del self._publications[id_publication]
            # Необходимо каскадное удаление

    def set_like(self, id_publication):
        """
            Позволяет поставить или удалить лайк (на/c) запис(ь/и)
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
        else:
            self._likes.remove(id_publication)
            self.query("""
                DELETE FROM likes
                WHERE id_publication = {0} AND id_user = {1}
            """.format(id_publication, self._id))

    def set_dislike(self, id_publication):
        """
            Позволяет поставить или удалить дизлайк (на/c) запис(ь/и)
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
        else:
            self._dislikes.remove(id_publication)
            self.query("""
                DELETE FROM dislikes
                WHERE id_publication = {0} AND id_user = {1}
            """.format(id_publication, self._id))


if __name__ == '__main__':
    # Тест
    user1 = SelfData('1')
    # print(user1._subscribers)
    # print(user1._subscriptions)
    # print(user1._likes)
    # print(user1._dislikes)
    print(user1._publications)
    # print(user1._likes)
    # print(user1._dislikes)
    # user1.set_like(2)
    # print(user1._likes)
    # print(user1._dislikes)