from basicModels import *
from datetime import datetime

class Publication(BasicModel):
    _TABLE = "publications"

    def __init__(self, id, content, description, id_user, time):
        self._id = id
        self._content = content
        self._description = description
        self._id_user = id_user
        self._time = time
        self._comments = self.get_comments()

    def delete(self):
        self.query("""
             DELETE FROM publications
             WHERE id = {0}
         """.format(self._id))

    def get_comments(self):
        comments_data = self.query("""
            SELECT * FROM comments
            WHERE id_publication = {0}
        """.format(self._id))
        result = {}
        if len(comments_data) > 0:
            for comment in comments_data:
                result[comment[2]] = (comment[0], comment[3], comment[4])
        return result

    def comment(self, id_sender, text_comment):
        time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")
        self.query("""
            INSERT INTO comments (id_publication, id_user, comment_text, comment_time)
            VALUES ({0}, {1}, '{2}', '{3}')
        """.format(self._id, id_sender, text_comment, time))
        id_comment = self.query("""
            SELECT last_insert_rowid()
        """)
        self._comments[id_sender] = (id_comment, text_comment, time)

    def delete_comment(self, id_comment):
        for id_sender in self._comments.keys():
            if self._comments[id_sender][0] == id_comment:
                del self._comments[id_sender]
                break
        self.query("""
            DELETE FROM comments
            WHERE id = {0}
        """.format(id_comment))