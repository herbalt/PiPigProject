from abc import abstractmethod, ABCMeta
from time import sleep
from models import SensorReading, Sensor, SensorType, SensorUnits
from general.patterns import ObserverAsyncTask

from datetime import datetime

class BaseSensor(ObserverAsyncTask):
    __metaclass__ = ABCMeta

    def __init__(self, sensor_id):
        super(BaseSensor, self).__init__()
        self.sensor_id = sensor_id
        self.state = False

    def __str__(self):
        result = "Sensor: " + self.get_name() + "\n"
        result = result + "Type: " + self.obj_sensor_type()
        return result

    def get_id(self):
        return self.sensor_id

    def obj_sensor(self):
        obj_sensor = Sensor.query.filter_by(id=self.get_id()).first()
        return obj_sensor

    def obj_sensor_type(self):
        return SensorType.query.filter_by(id=self.obj_sensor().id).first()

    def obj_sensor_units(self):
        sensor_type = self.obj_sensor_type()
        return SensorUnits.query.filter_by(id=sensor_type.get_id()).first()

    def get_name(self):
        return self.obj_sensor().name

    def get_interval_between_readings(self):
        return self.obj_sensor().get_interval_between_readings()

    def get_sensor_type_id(self):
        return self.obj_sensor().get_sensor_type_id()

    def get_minimum_refresh(self):
        return self.obj_sensor_type().get_minimum_refresh()

    def get_sensor_units(self):
        return self.obj_sensor_units().get_display_units()

    def get_state(self):
        return self.state

    @abstractmethod
    def take_reading(self):
        raise NotImplementedError

    def on_pre_execute(self):
        self.state = True

    def on_operation(self, params):
        while self.state:
            entry = SensorReading.create(self.get_id(), self.take_reading(), datetime())

            self.on_progress(progress=entry)

            if self.is_cancelled():
                return (False, entry)

            sleep(self.get_interval_between_readings())

        return (True, entry)