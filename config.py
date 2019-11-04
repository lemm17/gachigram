import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgres://postgres:postgrepass@localhost:5432/gachibase'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True