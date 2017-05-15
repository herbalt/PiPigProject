from binding_session.models import BindSessionsSensors, BindSessionAppliances
from bindings_datapoints.models import BindDataPointsSensors, BindDataPointsAppliances
from data_points.models import DataPoints
from general.patterns import Observer, Subject
from generics.constants import COMPONENT_TYPE_DATAPOINTS_SENSOR_BINDER, COMPONENT_TYPE_DATAPOINTS_APPLIANCE_BINDER
from generics.models import GenericReading
from pipig import app
from sensors.models import Sensor
from sessions.models import Session


class DataPointsSensorBinder(Subject):
    objBindSessionSensors = None
    objBindDataPointsSensors = None
    objSensor = None
    objSession = None

    def __init__(self, bind_datapoints_sensors_id):
        super(DataPointsSensorBinder, self).__init__()
        self.bind_datapoints_sensors_id = bind_datapoints_sensors_id

    def obj_datapoints_sensor_binder(self):
        if self.objBindDataPointsSensors is None:
            with app.app_context():
                obj = BindDataPointsSensors.get(self.bind_datapoints_sensors_id)
                # obj = BindDataPointsSensors.query.filter_by(id=self.bind_datapoints_sensors_id).first()
            return obj
        return self.objBindDataPointsSensors

    def obj_sensor(self):
        if self.objSensor is None:
            with app.app_context():
                # obj = Sensor.query.filter_by(id=self.get_sensor_id()).first()
                obj = Sensor.get(self.get_sensor_id())
            return obj
        return self.objSensor

    def obj_session(self):
        if self.objSession is None:
            with app.app_context():
                # obj = Session.query.filter_by(id=self.get_session_id()).first()
                obj = Session.get(self.get_session_id())
            return obj
        return self.objSession

    def obj_session_sensor_binder(self):
        if self.objBindSessionSensors is None:
            with app.app_context():
                # obj = BindSessionsSensors.query.filter_by(id=self.obj_datapoints_sensor_binder().get_id()).first()
                obj = BindSessionsSensors.get(self.obj_datapoints_sensor_binder().get_id())
            return obj
        return self.objBindSessionSensors

    def get_id(self):
        return self.obj_datapoints_sensor_binder().get_id()

    def get_session_id(self):
        return self.obj_session_sensor_binder().get_session_id()

    def get_sensor_id(self):
        return self.obj_session_sensor_binder().get_sensor_id()

    def get_datapoints_id(self):
        return self.obj_datapoints_sensor_binder().get_datapoints_id()

    def get_datapoint_at_time_elapsed(self, time_elapsed):
        datapoints = DataPoints.get(id=self.get_datapoints_id())
        return datapoints.get_point(time_elapsed)

    def difference_between_reading_and_datapoint_at_time_elapsed(self, time_elapsed):
        reading_time = self.obj_session().get_reading_time(time_elapsed)
        sensor_value = self.obj_sensor().get_reading_at_time(reading_time).get_value()
        datapoints_value = self.get_datapoint_at_time_elapsed(time_elapsed).get_value()

        return sensor_value - datapoints_value

    def request_output(self, time_elapsed):
        value = self.difference_between_reading_and_datapoint_at_time_elapsed(time_elapsed)

        reading = GenericReading(self.get_id(), COMPONENT_TYPE_DATAPOINTS_SENSOR_BINDER, value, time_elapsed)
        self.notify(reading)
        return reading





class DataPointsApplianceBinder(Observer, Subject):
    objBindDataPointsAppliances = None
    objBindSessionAppliances = None

    def __init__(self, bind_datapoints_appliances_id):
        Observer.__init__(self)
        Subject.__init__(self)
        self.bind_datapoints_appliances_id = bind_datapoints_appliances_id

    def __str__(self):
        return "DataPointsApplianceBinder: Id %d, SessionId %d, DatapointsId %d, ApplianceId %d, Polarity %d" % (self.get_id(), self.get_session_id(), self.get_datapoints_id(), self.get_appliance_id(), self.get_binder_polarity())

    def obj_datapoints_appliance_binder(self):
        if self.objBindDataPointsAppliances is None:
            with app.app_context():
                # obj = BindDataPointsAppliances.query.filter_by(id=self.bind_datapoints_appliances_id).first()
                obj = BindDataPointsAppliances.get(self.bind_datapoints_appliances_id)
            return obj
        return self.objBindDataPointsAppliances

    def obj_session_appliance_binder(self):
        if self.objBindSessionAppliances is None:
            with app.app_context():
                # obj = BindSessionAppliances.query.filter_by(id=self.obj_datapoints_appliance_binder().get_id()).first()
                obj = BindSessionAppliances.get(self.obj_datapoints_appliance_binder().get_id())
            return obj
        return self.objBindSessionAppliances

    def get_id(self):
        return self.obj_datapoints_appliance_binder().get_id()

    def get_session_id(self):
        return self.obj_session_appliance_binder().get_session_id()

    def get_appliance_id(self):
        return self.obj_session_appliance_binder().get_appliance_id()

    def get_datapoints_id(self):
        return self.obj_datapoints_appliance_binder().get_datapoints_id()

    def get_binder_polarity(self):
        return self.obj_datapoints_appliance_binder().get_polarity()

    def receive(self, result, status_code=0):
        """

        :param result: GenericReading with the value being the difference between a sensor reading and the datapoint
        :param status_code:
        :return:
        """

        if result.get_component_type_id != COMPONENT_TYPE_DATAPOINTS_SENSOR_BINDER:
            raise IncorrectReadingTypeError

        output_reading = self.generate_appliance_reading(result)
        self.notify(output_reading)

    def generate_appliance_reading(self, input_reading):
        """
        Manages the output reading to the Appliance based on the interaction with the datapoint
        :return:
        """
        output_value = self.calculate_output_value(input_reading.get_value())
        return GenericReading(self.get_id(), COMPONENT_TYPE_DATAPOINTS_APPLIANCE_BINDER, output_value, input_reading.get_timestamp())

    def calculate_output_value(self, input_value):
        """
        Converts an input reading from the difference between a Sensor and Datapoint to an output value for a Appliance
        This method is for a binary Appliance.
        Over-ride this method if a non-binary Appliance is required
        :param input_value:
        :return:
        """
        polarity = self.get_binder_polarity()

        if polarity == 0:
            return 0

        if polarity >= 1:
            if input_value <= 0:
                return 0
            else:
                return 1

        else:
            if input_value < 0:
                return 1
            else:
                return 0


class IncorrectReadingTypeError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)






