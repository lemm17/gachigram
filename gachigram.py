from app import app, db, socketio
from app.entities import *


@app.shell_context_processor
def make_shell_context():
    """ Контекст оболочки

    Функция создаёт контекст оболочки, который добавляет экземпляр и модели базы
    данных в сеанс оболочки Декоратор app.shell_context_processor регистрирует
    функцию как функцию контекста оболочки. Когда запускается команда flask shell,
    она будет вызывать эту функцию и регистрировать элементы, возвращаемые ею в
    сеансе оболочки.После того, как вы добавите функцию обработчика flask shell,
    вы можете работать с объектами базы данных, не импортируя их.
    """
    return {'db': db, 'User': User, 'Publication': Publication, 'association_subscriptions': association_subscriptions}
