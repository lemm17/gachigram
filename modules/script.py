import sqlite3
from propertyMixins import *
import random

# СКРИПТ НЕ АКТУАЛЕН 22.10.2019

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

    def show(self, obj):
        for key, value in obj.to_dict().items():
            if type(value) == list:
                print(key + "=>")
                for elem in value:
                    print("\t" + elem.__str__())
            else:
                print(key + " => " + value)



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
        return "Object DemoUser => login = {0}".format(self.login)


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
        Args:
            demo_user (DemoUser): Экземляр класса DemoUser
            comment_text (str): Текст комментария
        """
        for (key, value) in demo_user.__dict__.items():
            setattr(self, key, value)
        self.comment = comment_text

    def __str__(self):
        return "Комментарий пользователя {0}: {1}".format(self.login, self.comment)

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
        'self_like': bool,
        'self_dislike': bool
    }
    _TABLE = 'publications'

    @classmethod
    def _get_by_pk_mock(cls, user_login):
        return {
            'login': user_login,
            'id': random.randint(0, 1000),
            'content': 'content_{0}.jpg'.format(user_login),
            'likes': [DemoUser.get_by_pk('userLogin{0}'.format(i)) for i in range(2, 8)],
            'dislikes': [DemoUser.get_by_pk('userLogin{0}'.format(i)) for i in range(9, 11)],
            'comments': [Comment(DemoUser.get_by_pk('userLogin{0}'.format(i)), "Текст") for i in range(2, 10)],
            'self_like': True,
            'self_dislike': True
        }

    def add_comment(self, self_login, comment_text):
        """
        Добавляем комментарий
        Args:
             self_login (str): логин комментатора
             comment_text (str): введённый им текст
        """
        new_comment = Comment(DemoUser.get_by_pk(self_login), comment_text)
        self.comments.append(new_comment)

    def __str__(self):
        string = """Object Publication => login = {0}, id публикации = {1}\n\t""".format(self.login, self.id)
        string += "----------------------лайки----------------------\n"
        for like in self.likes:
            string += "\t" + like.__str__() + "\n"
        string += "\t----------------------дизлайки----------------------\n"
        for dislike in self.dislikes:
            string += "\t" + dislike.__str__() + "\n"
        string += "\t----------------------Комментарии----------------------\n"
        for comment in self.comments:
            string += "\t" + comment.__str__() + "\n"
        return string


class UserData(UserDataMixin, DemoUser):
    _FIELDS_MAPPING = {
        'login': str,
        'description': str,
        'avatar': str,
        'subscribers': list,
        'subscriptions': list,
        'publications': list,
    }

    @classmethod
    def _get_by_pk_mock(cls, user_login):
        return {
            'login': user_login,
            'description': "Описание странички {0}".format(user_login),
            'avatar': 'ava_{0}.png'.format(user_login),
            # 18 подпсичиков
            'subscribers': [DemoUser.get_by_pk('userLogin{0}'.format(i)) for i in range(2, 20)],
            # 20 подписок
            'subscriptions': [DemoUser.get_by_pk('userLogin{0}'.format(i)) for i in range(20, 40)],
            # 5 публикаций
            'publications': [Publication.get_by_pk(user_login) for i in range(5)]
        }

    def give_like(self, id_publication, self_login):
        """
            ищем необходимую запись по id, после чего
            меняем self_like записи на True/False,
            убираем дизлайк из списка дизлайков, если self_like == False
            и добавляем/удаляем DemoUser в likes
        Args:
            id_publication (int): id необходимой публикации
            self_login (str): собственный логин из selfData
        """
        for elem in self.publications:
            if elem.id == id_publication:
                if not elem.self_like:
                    elem.self_like = True
                    elem.likes.append(DemoUser.get_by_pk(self_login))
                    try:
                        elem.dislikes.remove(DemoUser.get_by_pk(self_login))
                    except ValueError:
                        pass
                else:
                    elem.self_like = False
                    elem.likes.remove(DemoUser.get_by_pk(self_login))

    def give_dislike(self, id_publication, self_login):
        """
            ищем необходимую запись по id, после чего
            меняем self_dislike записи на True/False,
            убираем лайк из списка лайков, если self_dislike == False
            и добавляем/удаляем DemoUser в dislikes
        Args:
            id_publication (int): id необходимой публикации
            self_login (str): собственный логин из selfData
        """
        for elem in self.publications:
            if elem.id == id_publication:
                if not elem.self_dislike:
                    elem.self_dislike = True
                    elem.dislikes.append(DemoUser.get_by_pk(self_login))
                    try:
                        elem.likes.remove(DemoUser.get_by_pk(self_login))
                    except ValueError:
                        pass
                else:
                    elem.self_dislike = False
                    elem.dislikes.remove(DemoUser.get_by_pk(self_login))

    def add_comment(self, id_publication, self_login, comment_text):
        """
        Добавляем комментарий, если настройками разрешено
        Args:
             id_publication (int): id необходимой публикации
             self_login (str): логин комментатора
             comment_text (str): введённый им текст
        """
        if self.settings.opportunity_to_comment:
            for publication in self.publications:
                if publication.id == id_publication:
                    publication.add_comment(self_login, comment_text)

    def delete_comment(self, self_login, comment_login, id_publication):
        """
            Возможность удалить свой комментарий
        Args:
            self_login (str): Свой логин
            comment_login (str): Логин комментатора
            id_publication (int): ID публикации под которой нужно удалить коммент
        """
        if self_login == comment_login:
            for publication in self.publications:
                if publication.id == id_publication:
                    for comment in publication.comments:
                        if comment.login == comment_login:
                            publication.comments.remove(Comment(DemoUser.get_by_pk(self_login), comment.comment))
                            break
                    break


# class SelfData(UserDataMixin, DemoUser):
#     _FIELDS_MAPPING = {
#         'login': str,
#         'description': str,
#         'avatar': str,
#         'subscribers': list,
#         'subscriptions': list,
#         'publications': list,
#         'like_data': list,
#         'dislike_data': list,
#         'settings': Settings,
#         'notifications': list,
#         'comments_data': list,
#         'registration_date': str
#     }
#
#     @classmethod
#     def _get_by_pk_mock(cls, user_login):
#         return {
#             'login': user_login,
#             'avatar': 'ava_{0}.png'.format(user_login),
#             # 18 подпсичиков
#             'subscribers': [DemoUser.get_by_pk('userLogin{0}'.format(i)) for i in range(2, 20)],
#             # 20 подписок
#             'subscriptions': [DemoUser.get_by_pk('userLogin{0}'.format(i)) for i in range(20, 40)],
#             # 5 публикаций
#             'publications': [Publication.get_by_pk(user_login) for i in range(5)],
#             # 50 лайков
#             'like_data': [DemoUser.get_by_pk('userLogin{0}'.format(i)) for i in range(2, 52)],
#             # 3 дизлайка
#             'dislike_data': [DemoUser.get_by_pk('userLogin{0}'.format(i)) for i in range(52, 55)],
#             'settings': Settings.get_by_pk(user_login),
#             'notifications': [],
#             'comments_data': [],
#             'registration_date': '10.10.2019'
#         }


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
    # test_publication()
    a = UserData.get_by_pk('userLogin1')
    a.show(a)
    publication_id = random.choice(a.publications).id
    print("Берем рандомный пост, id = {0} и ставим лайк за userLogin2".format(publication_id))
    a.give_like(publication_id, "userLogin2")
    a.show(a)