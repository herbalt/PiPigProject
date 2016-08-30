import os.path
import imp
from migrate.versioning import api
from microblog.data import db

from microblog.app_config import config_class
SQLALCHEMY_DATABASE_URI = config_class.SQLALCHEMY_DATABASE_URI
SQLALCHEMY_MIGRATE_REPO = config_class.SQLALCHEMY_MIGRATE_REPO


def db_create():
    try:
        db.create_all()
        if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
            api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
            api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
        else:
            api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
    except:
        return False
    return True


def db_drop():
    try:
        db.drop_all()
        return True
    except:
        return False


def db_downgrade():
    version = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, version - 1)
    version = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print('Current database version: ' + str(version))
    return version


def db_upgrade():
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    version = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print ('Current database version: ' + str(version))
    return version


def db_migrate():
    ver = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (ver+1))
    temp_module = imp.new_module('old_model')
    old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    exec (old_model, temp_module.__dict__)
    script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO,
                                              temp_module.meta, db.metadata)
    open(migration, "wt").write(script)
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    ver = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print ("New migration saved as " + migration)
    print ("Current database version " + str(ver))
    return ver
