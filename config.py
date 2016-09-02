from os.path import abspath, dirname, join, os
from credentials import credentials
basedir = dirname(abspath(__file__))

class BaseConfiguration(object):
    NAME = 'BaseConfiguration'
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'flask-session-insecure-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(basedir, 'curing-pi.db')
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


class TestConfiguration(BaseConfiguration):
    NAME = 'TestConfiguration'
    TESTING = True
    WTF_CSRF_ENABLED = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # + join(_cwd, 'testing.db')

    # Since we want our unit tests to run quickly
    # we turn this down - the hashing is still done
    # but the time-consuming part is left out.
    HASH_ROUNDS = 1

    MAIL_DEBUG = True
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_SSL = False


class TestDatabaseConfiguration(BaseConfiguration):
    NAME = 'TestDatabaseConfiguration'
    TESTING = True
    WTF_CSRF_ENABLED = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(basedir, 'pipig_test.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository_testing')
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




