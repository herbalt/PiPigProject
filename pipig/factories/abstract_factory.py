from factories.factory import SensorFactory, ApplianceFactory, DatapointFactory, ApplianceBinderFactory

class AbstractFactory:
    SENSOR = 'sensor'
    APPLIANCE = 'appliance_model'
    DATAPOINTS = 'datapoints'
    APPLIANCE_BINDER = 'applianceBinder'

    def __init__(self):
        self.sensor_factory = SensorFactory()
        self.appliance_factory = ApplianceFactory()
        self.datapoints_factory = DatapointFactory()
        self.appliance_binder_factory = ApplianceBinderFactory()

    def build_objects_dict(self, factory_type, object_id_list):
        if factory_type == self.SENSOR:
            return self.sensor_factory.build_object_dict(object_id_list)
        if factory_type == self.APPLIANCE:
            return self.appliance_factory.build_object_dict(object_id_list)
        if factory_type == self.DATAPOINTS:
            return self.datapoints_factory.build_object_dict(object_id_list)
        if factory_type == self.APPLIANCE_BINDER:
            return self.appliance_binder_factory.build_object_dict(object_id_list)
        return None

