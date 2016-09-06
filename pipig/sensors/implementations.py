from abc import abstractmethod, ABCMeta
from time import sleep, time
from pipig.sensors.models import SensorReadings, Sensor, SensorType, SensorUnits
from general.patterns import AsyncTask, Observer
from pipig.data import db

from datetime import datetime


class BaseSensor(AsyncTask):
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

    def pre_execute(self, payload=None):
        self.state = True
        return payload

    def create_reading(self, sensor_id, reading_value, reading_timestamp):
        # entry = SensorReadings.create(sensor_id=id, reading_value=reading, reading_timestamp=timestamp)
        # entry = SensorReadings.create(sensor_id=1, reading_value=1.9, reading_timestamp=1.2)
        try:
            reading = SensorReadings(sensor_id=sensor_id, reading_value=reading_value, reading_timestamp=reading_timestamp)

            db.session.add(reading)
            db.session.commit()

            return reading
        except:
            return None

    def operation(self, params=None):
        entry = None
        while self.state:
            timestamp = time()
            reading = self.take_reading()
            id = self.get_id()

            self.create_reading(id, reading, timestamp)
            entry_works = entry is None

            self.on_progress(progress=entry)
            if self.is_cancelled():
                return entry, AsyncTask.STATUS_CODE_CANCEL
            sleep(self.get_interval_between_readings())
        return entry

    def cancel(self, payload=None):
        self.state = False
        return payload

    def complete(self, payload=None):
        self.state = False
        return payload



