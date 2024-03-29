﻿# Gachigram

## СУТЬ ПРОЕКТА

Данный проект выступает в роли web приложения для публикации фотографий и видео.
***
Приложение будет обладать следущими возможностями:
* создание аккаунта пользователя
* публикация фото, видео 
* отмечать публикацию как понравившуюся или не понравившуюся
* комментарии публикаций
* обмен сообщениями в общем чате
* возможность подписки на другого пользователя
* просмотр уведомлений


  > он может быть выбран из предложенного списка или загружен пользователем

## СУЩНОСТИ
1. **User** - Список данных пользователя, обладает следующими полями:
    * id
    * login
    * avatar - ссылка на файл с аватаром пользователя
    * background - ссылка на файл с фоном профиля
    * description - описание профиля, максимальная длина: 150 символов
    * email 
    * phone_number
    * password_hash
    * registration_date - дата регистрации пользователя
    * subscriprions - список подписок
    * subscribers - список подписчков
    * likes - список публикаций, лайкнутых пользователем
    * dislikes список публикаций, дизлайкнутых пользователем
    * publications - список публикаций пользователя
    * settings - настройки профиля
    * notifications - список уведомлений
    **Методы**
    * sub(self, user) - позволяет подписаться на user
    * show_subscriptions(self) - показывает подписки
    * show_subscribers(self) - показывает подписчиков
    * unsub(self, user) - позволяет отписаться от user
    * is_subscribed(self, user) - проверят подписан ли self на user
    * set_pass(self, password) - позволяет изменить пароль
    * check_pass(self, password) - проверять пароль
    * create_pub(self, description, content = None) - создаёт публикацию с описанием description (content - ссылка на фото/видео)
    * show_pub(self) - показывает публикацию
    * delete_pub(self, id_publication) - удаляет публикацию
    * set_like(self, id_publication) - позволяет лайкнуть публикацию
    * set_dislike(self, id_publication) - позволяет дизлайкнуть публикацию
    * create_comment(self, id_publication, text) - позволяет комментировать запись
    * delete_comments(cls, id_comment) - удаление комментария
    * change_ea(self) - 
    * change_otc(self) - 
    * show_notification(self, **kwargs) - позволяет просмотреть уведомления
    * read_notification(self, id_notification = None) - позволяет прочитать уведомлени(е/я)
    
2. **Publication** - данные о публикации, обладает следующими полями:
    * id 
    * content - ссылка на фото/видео
    * description - описание
    * id_user 
    * likes - список пользователей, лайкнувших запись
    * dislikes - список пользователей, дизлайкнувших запись
    * comments
    **Методы**
    * set_like(self, user) - поставить/убрать лайк user
    * set_dislike(self, user) - поставить/убрать дизлайк user
    * set_comment(self, user, text) - добавить комментарий user
    * show_likes(self) - показать все лайки
    * show_dislikes(self) - показать все дизлайки
    * show_comments(self) - показать все комментарии
    
3. **Comment** - сущность коментария, содержащая:
    * id
    * id_publication
    * id_user
    * text - текст комментария
    * time - время создания комментария
    
4. **Settings** - Сущность, описывающая все настройки профиля конкретного пользователя. Поля:
    * id_user
    * op_to_com - возможность запрета комментирования
    * email_alerts - возможность запрета email оповещений
    **Методы**
    * email_alerts_change(self) - запрещает/разрешает email оповещения
    * op_to_com_change(self)
    
5. **Notification** - сущность уведомления, содержащая:
    * id
    * type
    * id_publication
    * id_user
    * text 
    * date - время создания
    * read - прочитано/непрочитано


