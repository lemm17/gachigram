import sqlite3
from propertyMixins import *


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
            'opportunity_to_comment': True,
            'email_alerts': True
        }


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
            'subscribers': [],
            'subscriptions': [],
            'publications': [],
            'like_data': [],
            'dislike_data': [],
            'settings': Settings.get_by_pk(user_login),
            'notifications': [],
            'comments_data': [],
            'registration_date': '10.10.2019'
        }


a = DemoUser.get_by_pk('userLogin1')
print(a.__dict__)
print(a.to_dict())
