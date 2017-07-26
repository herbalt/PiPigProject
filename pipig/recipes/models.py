from pipig.data import db, CRUDMixin
from binders.models import BindDatapointsAppliances, BindDatapointsSensors


class Recipe(db.Model, CRUDMixin):
    """
    A Recipe is the complete set of Sensors, Appliances and DataPoints along with their binders.
    A Recipe object does not hold any functionality, it is just a pointer to all the relevant IDs
    """
    __tablename__ = 'recipe'
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

    def get_json(self):
        sensor_binders = self.get_list_sensor_binder_id_tuples()
        appliance_binders = self.get_list_appliance_binder_id_tuples()

        sbind_list = []
        for sbind in sensor_binders:
            binder = {'datapoint id': sbind[0], 'sensor id': sbind[1]}
            sbind_list.append(binder)

        abind_list = []
        for abind in appliance_binders:
            binder = {'datapoint id': abind[0], 'appliance id': abind[1], 'polarity': abind[2]}
            abind_list.append(binder)

        json = {
            'recipe id': self.get_id(),
            'name': self.get_name(),
            'list of sensor bindings': sbind_list,
            'list of appliance bindings': abind_list
        }
        return json

    """
    GET METHODS
    """
    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_sensor_datapoints_binding_ids(self):
        binder_list = BindDatapointsSensors.query.filter_by(recipe_id=self.get_id()).all()
        binder_ids = []
        for binder in binder_list:
            binder_ids.append(binder.get_id())
        return binder_ids

    def get_appliance_datapoints_binding_ids(self):
        binder_list = BindDatapointsAppliances.query.filter_by(recipe_id=self.get_id()).all()
        binder_ids = []
        for binder in binder_list:
            binder_ids.append(binder.get_id())
        return binder_ids

    def get_sensor_ids(self):
        binder_list = BindDatapointsSensors.query.filter_by(recipe_id=self.get_id()).all()
        binder_ids = []
        for binder in binder_list:
            result = binder.get_sensor_id()
            if result not in binder_ids:
                binder_ids.append(result)
        return binder_ids

    def get_appliance_ids(self):
        binder_list = BindDatapointsAppliances.query.filter_by(recipe_id=self.get_id()).all()
        binder_ids = []
        for binder in binder_list:
            result = binder.get_appliance_id()
            if result not in binder_ids:
                binder_ids.append(result)
        return binder_ids

    def get_datapoints_ids(self):
        binder_list = BindDatapointsSensors.query.filter_by(recipe_id=self.get_id()).all()
        binder_ids = []
        for binder in binder_list:
            result = binder.get_datapoints_id()
            if result not in binder_ids:
                binder_ids.append(result)

        binder_list = BindDatapointsAppliances.query.filter_by(recipe_id=self.get_id()).all()

        for binder in binder_list:
            result = binder.get_datapoints_id()
            if result not in binder_ids:
                binder_ids.append(result)

        return binder_ids

    def get_datapoints_for_sensor(self, sensor_id):
        """
        Based on a serial_sensor id this will iterate all the Sensor Binders.
        Will return a list of all the datapoint IDs that are connected
        :param sensor_id: 
        :return: The corresponding Datapoint IDs for the relevant Sensor
        """

        output_list = []
        sensor_binders = self.get_sensor_datapoints_binding_ids()
        for binder_id in sensor_binders:
            binder = BindDatapointsSensors.get(binder_id)
            if binder.get_sensor_id() == sensor_id:
                output_list.append(binder.get_datapoints_id())
        return output_list

    def get_appliances_for_datapoint(self, datapoints_id):
        """
        Based on a datapoints ID this will iterate all the Appliance Binders
        Will return a list of all the Appliance IDs that are connected
        :param datapoints_id: 
        :return: The corresponding Appliance IDs for the relevant Datapoint
        """

        output_list = []
        appliance_binders = self.get_appliance_datapoints_binding_ids()
        for binder_id in appliance_binders:
            binder = BindDatapointsAppliances.get(binder_id)
            if binder.get_datapoints_id() == datapoints_id:
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
            binder = BindDatapointsAppliances.get(binder_id)
            if binder_id.get_datapoints_id() == datapoints_id:
                output_list.append(binder_id)
        return output_list

    def get_list_sensor_binder_id_tuples(self):
        tuple_list = []
        for sensor_id in self.get_sensor_ids():
            for datapoints_id in self.get_datapoints_for_sensor(sensor_id):
                tuple_list.append((datapoints_id, sensor_id))
        return tuple_list

    def get_list_appliance_binder_id_tuples(self):
        tuple_list = []
        for datapoints_id in self.get_datapoints_ids():
            for appliance_id in self.get_appliances_for_datapoint(datapoints_id):
                tuple_list.append((datapoints_id, appliance_id, polarity))
        return tuple_list

    def get_list_appliance_binder_id_tuples(self):
        binders = self.get_appliance_datapoints_binding_ids()
        tuple_list = []
        for binder_id in binders:
            appliance_binder = BindDatapointsAppliances.get(binder_id)
            datapoints = appliance_binder.get_datapoints_id()
            appliance = appliance_binder.get_appliance_id()
            polarity = appliance_binder.get_polarity()
            tuple_list.append((datapoints, appliance, polarity))

        return tuple_list





