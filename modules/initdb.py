import sqlite3
import random
from datetime import datetime

TABLES = ['users', 'publications', 'subscriptions', 'settings', 'likes',
          'dislikes', 'comments', 'notifications']


def init_db():
    """
        Создаём таблицы для db.db
    """
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute("""PRAGMA foreign_keys = ON""")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users
        (id INTEGER NOT NULL, login TEXT NOT NULL, description TEXT, avatar TEXT, email TEXT,
        phone_number TEXT NOT NULL, password TEXT NOT NULL, registration_date TEXT NOT NULL,
        PRIMARY KEY (id))
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS publications
        (id INTEGER NOT NULL, content TEXT NOT NULL, description TEXT, id_user INTEGER NOT NULL, time TEXT NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY (id_user) REFERENCES users(id))
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions
        (id_subscriber INTEGER NOT NULL, id_obj_subscription INTEGER NOT NULL,
        FOREIGN KEY (id_subscriber) REFERENCES users(id) ON DELETE CASCADE
        FOREIGN KEY (id_obj_subscription) REFERENCES users(id) ON DELETE CASCADE)
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings
        (id_user INTEGER NOT NULL, bg_theme TEXT, op_to_com INTEGER NOT NULL, email_alerts INTEGER NOT NULL,
        FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE)
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS likes
        (id_publication INTEGER NOT NULL, id_user INTEGER NOT NULL,
        FOREIGN KEY (id_publication) REFERENCES publications(id) ON DELETE CASCADE
        FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE)
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dislikes
        (id_publication INTEGER NOT NULL, id_user INTEGER NOT NULL,
        FOREIGN KEY (id_publication) REFERENCES publications(id) ON DELETE CASCADE
        FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE)
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments
        (id INTEGER NOT NULL, id_publication INTEGER NOT NULL, id_user INTEGER NOT NULL, comment_text TEXT,
        comment_time TEXT NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY (id_publication) REFERENCES publications(id) ON DELETE CASCADE 
        FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE)
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications
        (id INTEGER NOT NULL, id_obj_notification INTEGER NOT NULL, type TEXT NOT NULL, time TEXT NOT NULL,
        id_user INTEGER NOT NULL, id_publication INTEGER, is_read INTEGER NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY (id_obj_notification) REFERENCES users(id) ON DELETE CASCADE 
        FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE 
        FOREIGN KEY (id_publication) REFERENCES publications(id) ON DELETE CASCADE )
    """)
    conn.commit()
    conn.close()


def insert_test_data():
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    for i in range(5):
        cursor.execute("""
            INSERT INTO users
            VALUES ('{0}', 'testLogin{0}', 'Тестовое описание пользователя {0}',
            '../avatars/avatar{0}.png', 'testlogin{0}@gmail.com', '+79519190054', 'easypassword{0}',
            '16.10.2019')
        """.format(i))

    # Заполняем таблицу подписок
    subscriptions = [
        # 001 подписан на 000
        # слева те, кто подписан на тебя, справа те, на кого ты подписан
        ('1', '0'),
        ('0', '1'),
        ('2', '1'),
        ('3', '1'),
        ('4', '1')
    ]
    cursor.executemany("""
        INSERT INTO subscriptions
        VALUES (?, ?)
    """, subscriptions)

    # Заполняем таблицу пользовательских настроек
    settings = [('{0}'.format(i), '../bg_themes{0}.png'.format(i), '1', '1') for i in range(5)]
    cursor.executemany("""
        INSERT INTO settings
        VALUES (?, ?, ?, ?)
    """, settings)

    # YYYY-MM-DD
    # Заполняем таблицу публикаций (сделаем 5 публикаций)
    publications = [('{0}'.format(i), '../publications/content{0}'.format(i),
                     'Описание публикации {0}'.format(i), random.randint(0, 5),
                     datetime.strftime(datetime.now(), "%Y-%m-%d"))
                    for i in range(5)]
    cursor.executemany("""
            INSERT INTO publications
            VALUES (?, ?, ?, ?, ?)
        """, publications)

    # Пусть каждый пользователь поставит лайк на рандомную публикацию
    likes = [(random.randint(0, 5), i) for i in range(5)]
    cursor.executemany("""
                INSERT INTO likes
                VALUES (?, ?)
            """, likes)
    # Предположим, что дизлайки никто не ставил

    # YYYY-MM-DD HH:MM
    # Пусть каждый пользователь оставит комментарий на рандомную публикацию
    comments = [(i, random.randint(0, 5),
                i, 'Комментарий пользователя {0}'.format(i),
                datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")) for i in range(5)]

    cursor.executemany("""
                    INSERT INTO comments
                    VALUES (?, ?, ?, ?, ?)
                """, comments)
    # Уведомления пока не будем записывать
    conn.commit()
    conn.close()


def clear_table(table):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM {0}
    """.format(table))
    conn.commit()
    conn.close()


def clear_all_table():
    for table in TABLES:
        clear_table(table)


if __name__ == "__main__":
    init_db()
    insert_test_data()