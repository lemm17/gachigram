import sqlite3
from propertyMixins import *
import random


class ValidationError(Exception):
    """Ошибка валидации"""


class SQLModel:
    _DATABASE = None
    _TABLE = None

    @classmethod
    def _connect(cls):
        return sqlite3.connect(cls._DATABASE)

    @classmethod
    def query(cls, query):
        conn = cls._connect()
        cur = conn.cursor()

        cur.execute(query)
        conn.commit()
        conn.close()

    def _create_mapping(self):
        """
        Здесь мы проверяем существование таблицы
        Если нет - создаем и накатываем поля
        """
        pass

    def _update_mapping(self):
        """
        Здесь мы проверяем что у нас есть в бд из полей
        Если чего то нет - досоздаем
        """
        pass

    @classmethod
    def _get_by_pk(cls, pk):
        conn = cls._connect()
        cur = conn.cursor()

        cur.execute(
            """
                SELECT *
                FROM :table
                WHERE id = :pk
            """,
            {'table': cls._TABLE, 'pk': pk}
        )

        result = {}
        record = cur.fetchone()
        for idx, col in enumerate(cur.description):
            result[col] = record[idx]
        conn.close()
        return result

    @classmethod
    def _get_by_pk_mock(cls, *args):
        return {
            'age': 123,
            'name': 'Iozef'
        }

    @classmethod
    def get_by_pk(cls, pk):
        # record = cls._get_by_pk(pk)
        record = cls._get_by_pk_mock(pk)
        obj = cls()
        obj.fill_data(record)
        return obj


class BasicModel(SQLModel):
    # Поля модели
    _FIELDS_MAPPING = {}
    _DATABASE = 'database.db'

    def __getattr__(self, attr):
        if attr in self._FIELDS_MAPPING.keys():
            return None
        raise AttributeError()

    def fill_data(self, data):
        """
        Args:
            data (dict): данные модели
        """
        for key, val in data.items():
            if self._validate(key, val):
                self.__dict__['_' + key] = val

    def _validate(self, key, val):
        key_type = self._FIELDS_MAPPING.get(key)
        if not key_type:
            return False
        if key_type != type(val):
            raise ValidationError
        return True

    def to_dict(self):
        inner_dict = {}
        for key in self._FIELDS_MAPPING:
            inner_dict[key] = getattr(self, key)
        return inner_dict


class DemoUser(DemoUserMixin, BasicModel):
    _FIELDS_MAPPING = {
        'login': str,
        'avatar': str,
        'ref': str
    }
    _TABLE = 'users'

    @classmethod
    def _get_by_pk_mock(cls, user_login):
        return {
            'login': user_login,
            'avatar': 'ava_{0}.png'.format(user_login)
        }

    def __str__(self):
        return "Object DemoUser\nlogin = {0}".format(self.login)


class Settings(SettingsMixin, BasicModel):
    _FIELDS_MAPPING = {
        'bg_theme': str,
        'opportunity_to_comment': bool,
        'email_alerts': bool
    }
    _TABLE = 'users_settings'

    @classmethod
    def _get_by_pk_mock(cls, user_login):
        return {
            'bg_theme': 'bg_theme_{0}.png'.format(user_login),
            'opportunity_to_comment': False,
            'email_alerts': True
        }

    def reset(self):
        self.bg_theme = None
        self.opportunity_to_comment = False
        self.email_alerts = True


class Comment(DemoUserMixin, BasicModel):
    _FIELDS_MAPPING = {
        'login': str,
        'avatar': str,
        'ref': str,
        'comment': str
    }

    def __init__(self, demo_user, comment_text):
        """
        :param
            demo_user (DemoUser): Экземляр класса DemoUser
            comment_text (str): Текст комментария
        """
        for (key, value) in demo_user.__dict__.items():
            setattr(self, key, value)
        self.comment = comment_text

    def __str__(self):
        return "Комментарий пользователя {0}:\n-{1}".format(self.login, self.comment)

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value):
        if type(value) == str and len(value) < 501:
            self._comment = value


class Publication(PublicationMixin, BasicModel):
    _FIELDS_MAPPING = {
        'login': str,
        'id': int,
        'content': str,
        'likes': list,
        'dislikes': list,
        'comments': list,
    }
    _TABLE = 'publications'

    @classmethod
    def _get_by_pk_mock(cls, user_login):
        return {
            'login': user_login,
            'id': random.randint(0, 1000),
            'content': 'content_{0}.jpg'.format(user_login),
            'likes': [DemoUser.get_by_pk('userLogin{0}'.format(i)) for i in range(2, 8)],
            'dislikes': [DemoUser.get_by_pk('userLogin{0}'.format(i)) for i in range(2, 4)],
            'comments': [Comment(DemoUser.get_by_pk('userLogin{0}'.format(i)), "Текст") for i in range(2, 10)],
        }

    def add_comment(self, user_login, comment_text):
        self.comments.append(Comment(user_login, comment_text))

    #TODO: Реализовать функцию удаления комментария по логину


class UserData(UserDataMixin, DemoUser):
    _FIELDS_MAPPING = {
        'login': str,
        'description': str,
        'avatar': str,
        'subscribers': list,
        'subscriptions': list,
        'publications': list,
        'like_data': list,
        'dislike_data': list,
        'settings': Settings,
        'notifications': list,
        'comments_data': list,
        'bg_theme': str,
        'registration_date': str
    }

    @classmethod
    def _get_by_pk_mock(cls, user_login):
        return {
            'login': user_login,
            'avatar': 'ava_{0}.png'.format(user_login),
            # 18 подпсичиков
            'subscribers': [DemoUser.get_by_pk('userLogin{0}'.format(i)) for i in range(2, 20)],
            # 20 подписок
            'subscriptions': [DemoUser.get_by_pk('userLogin{0}'.format(i)) for i in range(20, 40)],
            # 5 публикаций
            'publications': [Publication.get_by_pk(user_login) for i in range(5)],
            'like_data': [],
            'dislike_data': [],
            'settings': Settings.get_by_pk(user_login),
            'notifications': [],
            'comments_data': [],
            'registration_date': '10.10.2019'
        }
# a = DemoUser.get_by_pk('userLogin1')
# print(a.__dict__)
# print(a.to_dict())


def test_publication():
    demo_user = DemoUser.get_by_pk('userLogin1')
    a = Publication.get_by_pk(demo_user.login)
    print(a.__dict__)
    for elem in a.comments:
        print(elem)
    a.add_comment(demo_user, 'Я добавил 1 коммент')
    print('---------------------------------------')
    print(a.comments[-1])


if __name__ == '__main__':
    test_publication()


