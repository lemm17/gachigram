class UserDataMixin:
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        pass

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        pass

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        pass

    @property
    def avatar(self):
        return self._avatar

    @avatar.setter
    def avatar(self, value):
        pass

    @property
    def subscriptions(self):
        return self._subscriptions

    @subscriptions.setter
    def subscriptions(self, value):
        pass

    @property
    def subscribers(self):
        return self._subscribers

    @subscribers.setter
    def subscribers(self, value):
        pass

    @property
    def publications(self):
        return self._publications

    @publications.setter
    def publications(self, value):
        pass

    @property
    def bg_theme(self):
        return self._bg_theme

    @bg_theme.setter
    def bg_theme(self, value):
        pass

    @property
    def op_to_com(self):
        return self._op_to_com

    @op_to_com.setter
    def op_to_com(self, value):
        pass


class SelfUserMixin:
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        pass

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        pass

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if len(value) < 151:
            self._description = value

    @property
    def avatar(self):
        return self._avatar

    @avatar.setter
    def avatar(self, value):
        if value[-4:-1] == '.png' or value[-4:-1] == '.jpg' or value[-5:-1] == '.jpeg':
            self._avatar = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        """Проверка на валидный имейл"""
        pass

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        """Проверка на валидный номер телефона"""
        pass

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        """Проверка на валдиный пароль"""
        self._password = value

    @property
    def registration_date(self):
        return self._registration_date

    @registration_date.setter
    def registration_date(self, value):
        pass

    @property
    def subscribers(self):
        return self._subscribers

    @subscribers.setter
    def subscribers(self, value):
        pass

    @property
    def subscriptions(self):
        return self._subscriptions

    @subscriptions.setter
    def subscriptions(self, value):
        pass

    @property
    def publications(self):
        return self._publications

    @publications.setter
    def publications(self, value):
        pass

    @property
    def likes(self):
        return self._likes

    @likes.setter
    def likes(self, value):
        pass

    @property
    def dislikes(self):
        return self._dislikes

    @dislikes.setter
    def dislikes(self, value):
        pass

    @property
    def setting(self):
        return self._setting

    @setting.setter
    def setting(self, value):
        pass

    @property
    def notifications(self):
        return self._notifications

    @notifications.setter
    def notifications(self, value):
        pass

    @property
    def comments(self):
        return self._comments

    @comments.setter
    def comments(self, value):
        pass


class SettingsMixin:
    @property
    def id_user(self):
        return self._id_user

    @id_user.setter
    def id_user(self, value):
        pass

    @property
    def bg_theme(self):
        return self._bg_theme

    @bg_theme.setter
    def bg_theme(self, value):
        """Проверить картинку, заменить"""
        pass

    @property
    def op_to_com(self):
        return self._op_to_com

    @op_to_com.setter
    def op_to_com(self, value):
        self._op_to_com = not self._op_to_com

    @property
    def email_alerts(self):
        return self._email_alerts

    @email_alerts.setter
    def email_alerts(self, value):
        self._email_alerts = not self._email_alerts


class PublicationMixin:
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        pass

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        pass

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if len(value) <= 500:
            self._description = value

    @property
    def id_user(self):
        return self._id_user

    @id_user.setter
    def id_user(self, value):
        pass

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        pass

    @property
    def comments(self):
        return self._comments

    @comments.setter
    def comments(self, value):
        pass


class NotificationMixin:
    @property
    def id_notification(self):
        return self._id_notification

    @id_notification.setter
    def id_notification(self):
        pass

    @property
    def id_obj_notification(self):
        return self._id_obj_notification

    @id_obj_notification.setter
    def id_obj_notification(self):
        pass

    @property
    def notification_type(self):
        return self._notification_type

    @notification_type.setter
    def notification_type(self):
        pass

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self):
        pass

    @property
    def id_user(self):
        return self._id_user

    @id_user.setter
    def id_user(self):
        pass

    @property
    def id_publication(self):
        return self._id_publication

    @id_publication.setter
    def id_publication(self):
        pass

    @property
    def is_read(self):
        return self._is_read

    @is_read.setter
    def is_read(self):
        pass