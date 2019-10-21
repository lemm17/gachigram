from basicModels import *


class Notification(BasicModel):
    _TABLE = 'notifications'
    _FIELDS_MAPPING = {
        'type': str,
        'time': str,
        'id_user': int,
        'id_publication': int
    }

    def __init__(self, id_notification, id_obj_notification, notification_type, time, id_user, id_publication, is_read):
        # Типы - unsubscribe, subscribe, comment, like, dislike
        self._id_notification = id_notification
        self._id_obj_notification = id_obj_notification
        self._notification_type = notification_type
        self._time = time
        self._id_user = id_user
        self._id_publication = id_publication
        self._is_read = is_read

    def is_read(self):
        return self._is_read

    def make_read(self):
        if not self.is_read():
            self._is_read = True
            self.query("""
            UPDATE notifications
            SET is_read = 1
            WHERE id = {0}
            """.format(self._id_notification))
