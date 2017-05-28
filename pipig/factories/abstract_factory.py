from factories.factory import SensorFactory, ApplianceFactory, DatapointFactory

class AbstractFactory:
    SENSOR = 'sensor'
    APPLIANCE = 'appliance'
    DATAPOINTS = 'datapoints'

    def __init__(self):
        self.sensor_factory = SensorFactory()
        self.appliance_factory = ApplianceFactory()
        self.datapoints_factory = DatapointFactory()

    def build_objects_dict(self, factory_type, object_id_list):
        if factory_type == self.SENSOR:
            return self.sensor_factory.build_object_dict(object_id_list)
        if factory_type == self.APPLIANCE:
            return self.appliance_factory.build_object_dict(object_id_list)
        if factory_type == self.DATAPOINTS:
            return self.datapoints_factory.build_object_dict(object_id_list)
        return None

