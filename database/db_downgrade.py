#!flask/bin/python
from migrate.versioning import api

from pipig.app_config import config_class
SQLALCHEMY_DATABASE_URI = config_class.SQLALCHEMY_DATABASE_URI
SQLALCHEMY_MIGRATE_REPO = config_class.SQLALCHEMY_MIGRATE_REPO

v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v - 1)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('Current database version: ' + str(v))
