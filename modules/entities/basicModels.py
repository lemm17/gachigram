import sqlite3


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
        """
            Выполняет sql запрос в базу данных
        :param
            query: SQL запрос
        :return
            all_data_set: Полный датасэт запроса
        """
        conn = cls._connect()
        cur = conn.cursor()
        cur.execute(query)
        all_data_set = cur.fetchall()
        conn.commit()
        conn.close()
        return all_data_set

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
                FROM {0}
                WHERE id = {1}
            """.format(cls._TABLE, pk)
        )
        result = {}
        record = cur.fetchone()
        for idx, col in enumerate(cur.description):
            result[col[0]] = record[idx]
        conn.close()
        return result


class BasicModel(SQLModel):
    # Поля модели
    _FIELDS_MAPPING = {}
    _DATABASE = '../db.db'

    @classmethod
    def get_by_pk(cls, pk):
        """
            Обрабатывает набор данных и возвращает валидный вариант
        Args:
            pk - id пользователя
        """
        record = cls._get_by_pk(pk)
        validate_data = {}
        for key, val in record.items():
            if cls._validate(key, val):
                validate_data[key] = val
        return validate_data

    def __getattr__(self, attr):
        if attr in self._FIELDS_MAPPING.keys():
            return None
        raise AttributeError()

    @classmethod
    def _validate(cls, key, val):
        """
            Проверяет на валидность очередной элемент датасэта
        """
        key_type = cls._FIELDS_MAPPING.get(key)
        if not key_type:
            return False
        if key_type != type(val):
            raise ValidationError
        return True

    def to_dict(self):
        """
            Выводит все элементы объекта
        """
        inner_dict = {}
        for key in self._FIELDS_MAPPING:
            inner_dict[key] = getattr(self, "_" + key)
        return inner_dict