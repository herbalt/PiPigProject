#!flask/bin/python

from migrate.versioning import api
from pipig.data import db
from pipig import app
import os.path



from pi_pig.app_config import config_class
SQLALCHEMY_DATABASE_URI = config_class.SQLALCHEMY_DATABASE_URI
SQLALCHEMY_MIGRATE_REPO = config_class.SQLALCHEMY_MIGRATE_REPO

with app.app_context():
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
    db.create_all()
    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    else:
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO,
                            api.version(SQLALCHEMY_MIGRATE_REPO))
