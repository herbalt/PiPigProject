from pipig.data import db, CRUDMixin
from sensors.models import Sensor
from binders.models import BindDatapoitnsAppliances, BindDatapoitnsSensors
from binders.models import BindDatapoitnsSensors

class Recipe(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "RECIPE\n" + \
               "ID: " + str(self.get_id()) + \
               "\nName: " + self.get_name() + \
               "\nSensor Bindings: " + str(self.get_sensor_datapoints_binding_ids()) + \
               "\nAppliance Bindings: " + str(self.get_appliance_datapoints_binding_ids()) + \
               "\nSensor Ids: " + str(self.get_sensor_ids()) + \
               "\nAppliance Ids: " + str(self.get_appliance_ids()) + \
               "\nDatapoints Ids: " + str(self.get_datapoints_ids())

    def __eq__(self, other):
        equal_id = self.get_id() == other.get_id()
        equal_name = self.get_name() == other.get_name()
        equal_sensor_bindings = self.get_sensor_datapoints_binding_ids() == other.get_sensor_datapoints_binding_ids()
        equal_appliance_bindings = self.get_appliance_datapoints_binding_ids() == other.get_appliance_datapoints_binding_ids()
        equal_sensor_ids = self.get_sensor_ids() == other.get_sensor_ids()
        equal_appliance_ids = self.get_appliance_ids() == other.get_appliance_ids()
        equal_datapoints_ids = self.get_datapoints_ids() == other.get_datapoints_ids()
        return equal_id and equal_name and equal_sensor_bindings and equal_appliance_bindings and equal_sensor_ids and equal_appliance_ids and equal_datapoints_ids

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
            result = binder.get_sensor_id()
            if result not in binder_ids:
                binder_ids.append(result)
        return binder_ids

    def get_appliance_ids(self):
        binder_list = BindDatapoitnsAppliances.query.filter_by(recipe_id=self.get_id()).all()
        binder_ids = []
        for binder in binder_list:
            result = binder.get_appliance_id()
            if result not in binder_ids:
                binder_ids.append(result)
        return binder_ids

    def get_datapoints_ids(self):
        binder_list = BindDatapoitnsSensors.query.filter_by(recipe_id=self.get_id()).all()
        binder_ids = []
        for binder in binder_list:
            result = binder.get_sensor_id()
            if result not in binder_ids:
                binder_ids.append(result)

        binder_list = BindDatapoitnsAppliances.query.filter_by(recipe_id=self.get_id()).all()

        for binder in binder_list:
            result = binder.get_appliance_id()
            if result not in binder_ids:
                binder_ids.append(result)

        return binder_ids

    def get_datapoints_for_sensor(self, sensor_id):
        """
        
        :param sensor_id: 
        :return: The corresponding Datapoint IDs for the relevant Sensor
        """

        output_list = []
        sensor_binders = self.get_sensor_datapoints_binding_ids()
        for binder_id in sensor_binders:
            binder = BindDatapoitnsSensors.get(binder_id)
            if binder.get_sensor_id() == sensor_id:
                output_list.append(binder.get_datapoints_id())
        return output_list

    def get_appliances_for_datapoint(self, datapoints_id):
        """
        
        :param datapoints_id: 
        :return: The corresponding Appliance IDs for the relevant Datapoint
        """

        output_list = []
        appliance_binders = self.get_appliance_datapoints_binding_ids()
        for binder_id in appliance_binders:
            binder = BindDatapoitnsAppliances.get(binder_id)
            if binder_id.get_datapoints_id() == datapoints_id:
                output_list.append(binder.get_appliance_id())
        return output_list

    def get_appliance_binders_for_datapoint(self, datapoints_id):
        """

        :param datapoints_id: 
        :return: The corresponding Appliance IDs for the relevant Datapoint
        """

        output_list = []
        appliance_binders = self.get_appliance_datapoints_binding_ids()
        for binder_id in appliance_binders:
            binder = BindDatapoitnsAppliances.get(binder_id)
            if binder_id.get_datapoints_id() == datapoints_id:
                output_list.append(binder_id)
        return output_list




