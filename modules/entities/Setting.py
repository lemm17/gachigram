from basicModels import *
from propertyMixins import SettingsMixin


class Setting(BasicModel, SettingsMixin):
    _TABLE = 'settings'
    _FIELDS_MAPPING = {
        'id_user': int,
        'bg_theme': str,
        'op_to_com': int,
        'email_alerts': int
    }

    def __init__(self, data):
        self._id_user = data[0]
        self._bg_theme = data[1]
        if data[2]:
            self._op_to_com = True
        else:
            self._op_to_com = False
        if data[3]:
            self._email_alerts = True
        else:
            self._email_alerts = False

    def change_bg_theme(self):
        """
            Функция замены заднего фона страницы
        """
        pass

    def change_op_to_com(self):
        self.op_to_com = not self.op_to_com

    def change_email_alerts(self):
        self.email_alerts = not self.email_alerts
