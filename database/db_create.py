#!flask/bin/python
from migrate.versioning import api
from microblog.data import db
from microblog import app
import os.path

from microblog.app_config import config_class
SQLALCHEMY_DATABASE_URI = config_class.SQLALCHEMY_DATABASE_URI
SQLALCHEMY_MIGRATE_REPO = config_class.SQLALCHEMY_MIGRATE_REPO

with app.app_context():

    db.create_all()
    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    else:
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO,
                            api.version(SQLALCHEMY_MIGRATE_REPO))
