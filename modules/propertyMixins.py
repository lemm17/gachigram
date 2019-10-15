class DemoUserMixin:
    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        pass

    @property
    def avatar(self):
        return self._avatar

    @avatar.setter
    def avatar(self, value):
        pass

    @property
    def ref(self):
        return self._ref

    @ref.setter
    def ref(self, value):
        pass


class UserDataMixin:
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if len(value) < 151:
            self._description = value

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
    def like_data(self):
        return self._like_data

    @like_data.setter
    def like_data(self, value):
        pass

    @property
    def dislike_data(self):
        return self._dislike_data

    @dislike_data.setter
    def dislike_data(self, value):
        pass

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, value):
        pass

    @property
    def notifications(self):
        return self._notifications

    @notifications.setter
    def notifications(self, value):
        pass

    @property
    def comments_data(self):
        return self._comments_data

    @comments_data.setter
    def comments_data(self, value):
        pass

    @property
    def registration_date(self):
        return self._registration_date

    @registration_date.setter
    def registration_date(self, value):
        pass


class SettingsMixin:
    @property
    def bg_theme(self):
        return self._bg_theme

    @bg_theme.setter
    def bg_theme(self, value):
        self._bg_theme = value

    @property
    def opportunity_to_comment(self):
        return self._opportunity_to_comment

    @opportunity_to_comment.setter
    def opportunity_to_comment(self, value):
        self._opportunity_to_comment = not self._opportunity_to_comment

    @property
    def email_alerts(self):
        return self._email_alerts

    @email_alerts.setter
    def email_alerts(self, value):
        self._email_alerts = not self._email_alerts


class PublicationMixin:
    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        pass

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
    def likes(self):
        return self._likes

    @likes.setter
    def likes(self, value):
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
    def comments(self):
        return self._comments

    @comments.setter
    def comments(self, value):
        pass

    @property
    def self_like(self):
        return self._self_like

    @self_like.setter
    def self_like(self, value):
        """
            Если стоит дизлайк, отключаем его и ставим лайк
            или если стоит лайк, отключаем его
            иначе просто ставим лайк
        """
        if self._self_dislike:
            self._self_dislike = False

            self._self_like = True
        elif self._self_like:
            self._self_like = False
        else:
            self._self_like = True

    @property
    def self_dislike(self):
        return self._self_dislike

    @self_dislike.setter
    def self_dislike(self, value):
        """
            Если стоит лайк, отключаем его и ставим дизлайк
            или если стоит дизлайк, отключаем его
            иначе просто ставим дизлайк
        """
        if self._self_like:
            self._self_like = False
            self._self_dislike = True
        elif self._self_dislike:
            self._self_dislike = False
        else:
            self._self_dislike = True