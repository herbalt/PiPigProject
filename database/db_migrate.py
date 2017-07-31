#!flask/bin/python
import imp
from migrate.versioning import api
from pipig import app

from pipig.app_config import config_class
SQLALCHEMY_DATABASE_URI = config_class.SQLALCHEMY_DATABASE_URI
SQLALCHEMY_MIGRATE_REPO = config_class.SQLALCHEMY_MIGRATE_REPO

from pipig.data import db


from pipig.appliances.models import Appliance, ApplianceType
from pipig.binders.models import BindDatapointsSensors, BindDatapointsAppliances
from pipig.curing_sessions.models import CuringSession
from pipig.data_points.models import DataPoints, DataPoint
from pipig.generics.models import GenericReading, GenericUnits
from pipig.pi_gpio.models import GpioPin
from pipig.recipes.models import Recipe
from pipig.sensors.models import Sensor, SensorType
# from pi_pig.units.models import
from pipig.users.models import UserAccount, UserAccountStatus, UserProfile
from pipig.pi_pig.models import PiPigModel, PiPigStatus


v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
tmp_module = imp.new_module('old_model')
old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
exec old_model in tmp_module.__dict__
script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI,
                                          SQLALCHEMY_MIGRATE_REPO,
                                          tmp_module.meta, db.metadata)
open(migration, "wt").write(script)
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('New migration saved as ' + migration)
print('Current database version: ' + str(v))
