from basicModels import *


class Publication(BasicModel):
    def __init__(self, id, content, description, id_user):
        self._id = id
        self._content = content
        self._description = description
        self._id_user = id_user
        self._comment = {}

    # метод оставки коммента

    # Метод удаляющий коммент