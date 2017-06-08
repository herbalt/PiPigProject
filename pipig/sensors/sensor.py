from abc import abstractmethod, ABCMeta
from time import sleep, time

from generics.constants import COMPONENT_TYPE_SENSOR
from pipig import app
from pipig.sensors.models import Sensor, SensorType
from generics.models import GenericReading, GenericUnits
from general.patterns import AsyncTask
from gpio_pins.models import GpioPin

from gpio.config import GPIO, PI_CONNECTED

try:
    import Adafruit_DHT
    sensor_args = {'11': Adafruit_DHT.DHT11,
                   '22': Adafruit_DHT.DHT22,
                   '2302': Adafruit_DHT.AM2302}
except ImportError:
    pass

class BaseSensor(AsyncTask):
    """
    Object to Interact with a Sensor of a particular configuration
    """
    __metaclass__ = ABCMeta

    sensor = None
    sensor_type = None
    sensor_units = None

    def __init__(self, sensor_id):
        super(BaseSensor, self).__init__()
        self.sensor_id = sensor_id
        self.state = False

    # ---------------------------------------------------------------------
    # GET METHODS
    # ---------------------------------------------------------------------
    def __str__(self):
        result = "Sensor: " + self.get_name() + "\n"
        result = result + "Type: " + str(self.obj_type())
        return result

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def get_id(self):
        return self.sensor_id

    def obj_sensor(self):
        if self.sensor is None:
            with app.app_context():
                self.sensor = Sensor.get(self.get_id())

        return self.sensor

    def obj_type(self):
        if self.sensor_type is None:
            self.sensor_type = SensorType.get(self.obj_sensor().get_type_id())
        return self.sensor_type

    def obj_units(self):
        if self.sensor_units is None:
            self.sensor_units = GenericUnits.get(self.obj_type().get_id())
        return self.sensor_units

    def get_name(self):
        return self.obj_sensor().name

    def get_interval_between_readings(self):
        # with app.app_context():
        obj = self.obj_sensor()
        interval = obj.get_interval_between_readings()
        return interval

    def get_type_id(self):
        return self.obj_sensor().get_type_id()

    def get_minimum_refresh(self):
        # with app.app_context():
        obj = self.obj_type()
        min = obj.get_minimum_refresh()
        return min

    def get_units(self):
        return self.obj_units().get_display_units()

    def get_state(self):
        return self.state

    def get_gpio_pin(self):
        if self.obj_sensor().get_gpio_pin_id() is None:
            return None
        return GpioPin.get(self.obj_sensor().get_gpio_pin_id()).get_pin_number()

    # ---------------------------------------------------------------------
    # ASYNCTASK OVER RIDE METHODS
    # ---------------------------------------------------------------------

    @abstractmethod
    def take_reading(self):
        raise NotImplementedError

    def pre_execute(self, payload=None):
        self.state = True
        return payload

    def operation(self, params=None):
        entry = None
        while self.state:
            timestamp = time()
            reading = self.take_reading()
            reading = GenericReading(component_id=self.get_id(), component_type_id=COMPONENT_TYPE_SENSOR, reading_value=reading,
                                     reading_timestamp=timestamp)

            self.on_progress(progress=reading)
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


class SensorBasic(BaseSensor):
    """
    Example implementation of a BaseSensor
    """
    def __init__(self, sensor_id):
        super(SensorBasic, self).__init__(sensor_id)
        self.counter = 0

    def take_reading(self):
        self.counter += 1
        # print self.get_name() + "\ntake_reading: " + str(self.counter) + "\n"
        return self.counter


class SensorADC(BaseSensor):

    def __init__(self, sensor_id):
        super(SensorADC, self).__init__(sensor_id)

    def take_reading(self):
        pass


class SensorDHT22(BaseSensor):

    def __init__(self, sensor_id):
        super(SensorDHT22, self).__init__(sensor_id)

    def take_reading(self):
        humidity, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, self.get_gpio_pin())
        return humidity, temp


class SensorDHT22Temperature(SensorDHT22):
    def __init__(self, sensor_id, celsius=True):
        super(SensorDHT22Temperature, self).__init__(sensor_id)
        self.celsius = celsius

    def take_reading(self):
        try:
            result = SensorDHT22.take_reading(self)
            # print str(result)
            if result is None:
                raise TypeError

            if self.celsius:
                return result[1]
            else:
                return result[1] * (9/5) + 32

        except IndexError:
            return None
        except TypeError:
            return None


class SensorDHT22Humidity(SensorDHT22):
    def __init__(self, sensor_id):
        super(SensorDHT22Humidity, self).__init__(sensor_id)

    def take_reading(self):
        try:
            result = SensorDHT22.take_reading(self)
            if result is None:
                raise TypeError
            return result[0]

        except IndexError:
            return None
        except TypeError:
            return None