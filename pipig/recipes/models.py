from pipig.data import db, CRUDMixin
from sensors.models import Sensor
from binders.models import BindDatapoitnsAppliances, BindDatapoitnsSensors


class Recipe(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)

    def __init__(self, name):
        self.name = name

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_sensor_datapoints_binding_ids(self):
        binder_list = BindDatapoitnsSensors.query.filter_by(recipe_id=self.get_id()).all()
        binder_ids = []
        for binder in binder_list:
            binder_ids.append(binder.get_id())
        return binder_ids

    def get_appliance_datapoints_binding_ids(self):
        binder_list = BindDatapoitnsAppliances.query.filter_by(recipe_id=self.get_id()).all()
        binder_ids = []
        for binder in binder_list:
            binder_ids.append(binder.get_id())
        return binder_ids

    def get_sensor_ids(self):
        binder_list = BindDatapoitnsSensors.query.filter_by(recipe_id=self.get_id()).all()
        binder_ids = []
        for binder in binder_list:
            binder_ids.append(binder.get_sensor_id())
        return binder_ids

    def get_appliance_ids(self):
        binder_list = BindDatapoitnsAppliances.query.filter_by(recipe_id=self.get_id()).all()
        binder_ids = []
        for binder in binder_list:
            binder_ids.append(binder.get_appliance_id())
        return binder_ids

    def get_datapoints_ids(self):
        binder_list = BindDatapoitnsSensors.query.filter_by(recipe_id=self.get_id()).all()
        binder_ids = []
        for binder in binder_list:
            binder_ids.append(binder.get_sensor_id())

        binder_list = BindDatapoitnsAppliances.query.filter_by(recipe_id=self.get_id()).all()

        for binder in binder_list:
            binder_ids.append(binder.get_appliance_id())

        return binder_ids









