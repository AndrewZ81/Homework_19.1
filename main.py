from flask import Flask
from flask_restx import Api

from app.config import Config
from app.create_db import db
# from app.models import User

from app.views.movies import movies_ns
from app.views.genres import genres_ns
from app.views.directors import directors_ns
from app.views.users import users_ns


def create_app(config_obj):
    """
    Создаёт экземпляр класса Flask и конфигурирует его
    :param config_obj: Объект конфигурации экземпляра класса Flask
    :return: Экземпляр класса Flask
    """
    application = Flask(__name__)
    application.config.from_object(config_obj)
    application.app_context().push()
    create_extensions(application)
    return application


def create_extensions(flask_app):
    """
    Создаёт расширения экземпляра класса Flask и конфигурирует их
    :param flask_app: Экземпляр класса Flask
    :return:
    """
    db.init_app(flask_app)
    api = Api(flask_app)
    api.add_namespace(movies_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(genres_ns)
    api.add_namespace(users_ns)
    # create_data(flask_app)


'''
def create_data(flask_app):
    """
    Создает объекты базы данных экземпляра класса Flask
    :param flask_app: Экземпляр класса Flask
    :return:
    """
    with flask_app.app_context():
        db.create_all()
        u1 = User(username="vasya", password="my_little_pony", role="user")
        u2 = User(username="oleg", password="qwerty", role="user")
        u3 = User(username="oleg", password="P@ssw0rd", role="admin")
        with db.session.begin():
            db.session.add_all([u1, u2, u3])
'''

app_config = Config()  # Создаём экземпляр класса конфигурации приложения
app = create_app(app_config)  # Создаём наше приложение Flask

if __name__ == "__main__":  # Точка входа в наше приложение Flask
    app.run()
