from basicModels import *


class Publication(BasicModel):
    _TABLE = "publications"
    def __init__(self, id, content, description, id_user, time):
        self._id = id
        self._content = content
        self._description = description
        self._id_user = id_user
        self._time = time
        self._comment = {}

    def delete(self):
        self.query("""
             DELETE FROM publications
             WHERE id = {0}
         """.format(self._id))

    # метод оставки коммента

    # Метод удаляющий коммент