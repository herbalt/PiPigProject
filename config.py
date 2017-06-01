from os.path import abspath, dirname, join, os
from credentials import credentials
from processors.factory import PRINT_DATABASE
basedir = dirname(abspath(__file__))

class BaseConfiguration(object):
    NAME = 'BaseConfiguration'
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'flask-session-insecure-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(basedir, 'production.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_ECHO = False
    HASH_ROUNDS = 100000

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    MAIL_USERNAME = credentials.MAIL_USERNAME
    MAIL_PASSWORD = credentials.MAIL_PASSWORD

    # mail accounts
    MAIL_DEFAULT_SENDER = credentials.MAIL_USERNAME

    # SENSOR_PROCESSOR_CHAIN = PRINT_DATABASE
    # APPLIANCE_PROCESSOR_CHAIN = PRINT_DATABASE
    SENSOR_PROCESSOR_CHAIN = 'database'
    APPLIANCE_PROCESSOR_CHAIN = 'database'


class TestConfiguration(BaseConfiguration):
    NAME = 'TestConfiguration'
    TESTING = True
    WTF_CSRF_ENABLED = False
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(basedir, 'TEST2.db')
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' + join(basedir, 'test.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # + join(_cwd, 'testing.db')
    # Since we want our unit tests to run quickly
    # we turn this down - the hashing is still done
    # but the time-consuming part is left out.
    HASH_ROUNDS = 1

    MAIL_DEBUG = True
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_SSL = False

    # PRESERVE_CONTEXT_ON_EXCEPTION = False

class TestDatabaseConfiguration(BaseConfiguration):
    NAME = 'TestDatabaseConfiguration'
    TESTING = True
    WTF_CSRF_ENABLED = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(basedir, 'development.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository_development')
    # Since we want our unit tests to run quickly
    # we turn this down - the hashing is still done
    # but the time-consuming part is left out.
    HASH_ROUNDS = 1

    MAIL_DEBUG = True
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_SSL = False

class DebugConfiguration(BaseConfiguration):
    NAME = 'DebugConfiguration'
    DEBUG = True




