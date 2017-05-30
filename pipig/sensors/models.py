from generics.constants import COMPONENT_TYPE_SENSOR
from generics.models import GenericReading
from pipig.data import db, CRUDMixin

class SensorType(db.Model, CRUDMixin):
    """
    Determines the SensorType
    Example, DHT22, TMP32, TestCounter
    """
    __tablename__ = "sensor_type"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    type_name = db.Column(db.String(140), nullable=False)
    units_id = db.Column(db.Integer, nullable=False)
    minimum_refresh = db.Column(db.Float(), default=0)

    def __init__(self, type_name, units_id=0, minimum_refresh=0.0):
        self.type_name = type_name
        self.units_id = units_id
        self.minimum_refresh = minimum_refresh

    def get_minimum_refresh(self):
        return self.minimum_refresh

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type_name

    def get_units_id(self):
        return self.units_id


class Sensor(db.Model, CRUDMixin):
    """
    Determines the configuration of a Sensor
    Can add a GPIO pin if required
    """
    __tablename__ = "sensor"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    type_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    interval_between_readings = db.Column(db.Float, nullable=True)
    gpio_pin_id = db.Column(db.Integer, nullable=True, default=None)

    def __init__(self, name, type_id, interval_between_readings, gpio_pin_id=None):
        self.type_id = type_id
        self.name = name
        self.interval_between_readings = interval_between_readings
        self.gpio_pin_id = gpio_pin_id

    def __str__(self):
        return "Id: " + str(self.id) + \
               " Name:" + self.name + \
               " TypeId: " + str(self.type_id) + \
               " Interval: " + str(self.interval_between_readings)

    def get_interval_between_readings(self):
        return self.interval_between_readings

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_type_id(self):
        return self.type_id

    def get_gpio_pin_id(self):
        return self.gpio_pin_id


    def get_readings(self):
        return GenericReading.query.filter_by(component_id=self.get_id()).all()


    def process_sensor_reading_list_to_single_point(self, list_of_sensor_reading_objects=None):
        """
        Takes a list of Data Point Objects and averages the values,
        then creates a new DataPoint with:
            latest timestamp, the new value, and the original data_points_id
        :return: Data Point Object
        """
        if list_of_sensor_reading_objects is None or list_of_sensor_reading_objects == []:
            return None

        value_sum = 0

        for reading in list_of_sensor_reading_objects:
            value_sum += reading.get_value()

        last_point = list_of_sensor_reading_objects[-1]

        try:
            average_value = value_sum / len(list_of_sensor_reading_objects)
            return GenericReading(self.get_id, COMPONENT_TYPE_SENSOR, average_value, last_point.get_timestamp())
        except ZeroDivisionError:
            return None

    def get_reading_at_time(self, reading_time):
        """
        Returns the Sensor reading corresponding to a given time.
        If no Sensor Reading at a given time, then retrieve readings either side of time and average the readings
        :param reading_time: Time stamp to review
        :return: Sensor Reading Object
        """

        # Processes Sensor Readings if multiple readings at time_elapsed
        initial_query = GenericReading.query.filter_by(component_id=self.get_id(), reading_timestamp=reading_time).all()


        if initial_query is not None:
            initial_result = self.process_sensor_reading_list_to_single_point(initial_query)
            if initial_result is not None:
                return initial_result

        # Get the list of Readings associated with the Sensor Object
        all_points = self.get_readings()
        if len(all_points) == 0:
            return None

        # These two variables track the current closet time values to the time variable
        low_sensor_reading = None
        high_sensor_reading = None

        # Loop through the sensor reading list to assess each against the tracking variables
        for index in range(0, len(all_points)):
            # Populate the low variable if currently not set and has a time value less than the input
            if low_sensor_reading is None and all_points[index].get_timestamp() <= reading_time:
                low_sensor_reading = all_points[index]

            # Populate the high variable if currently not set and has a time value greater than the input
            if high_sensor_reading is None and all_points[index].get_timestamp() >= reading_time:
                high_sensor_reading = all_points[index]

            # Populate the low variable if has a elapsed value less than the input and greater than the current low variable
            if all_points[index].get_timestamp() <= reading_time and \
                            all_points[index].get_timestamp() > low_sensor_reading.get_timestamp():
                low_sensor_reading = all_points[index]

            # Populate the high variable if has a elapsed value less than the input and less than the current low variable
            if all_points[index].get_timestamp() >= reading_time and \
                            all_points[index].get_timestamp() < high_sensor_reading.get_timestamp():
                high_sensor_reading = all_points[index]

        # Attempt to process all values at the low variable's elapsed
        try:
            low_sensor_reading = self.get_reading_at_time(low_sensor_reading.get_timestamp())
        except AttributeError:
            # If time input is before any DataPoint
            first_data_point = all_points[0]
            first_data_point.reading_timestamp = reading_time
            return first_data_point

        # Attempt to process all values at the high variable's elapsed
        try:
            high_sensor_reading = self.get_reading_at_time(high_sensor_reading.get_timestamp())
        except AttributeError:
            # If time_elapsed input is after any DataPoint
            last_sensor_reading = all_points[-1]
            last_sensor_reading.reading_timestamp = reading_time
            return last_sensor_reading

        # Average the low and high variable values and set with the time_elapsed input
        processed_sensor_reading = self.process_sensor_reading_list_to_single_point([low_sensor_reading, high_sensor_reading])
        processed_sensor_reading.reading_timestamp = reading_time
        return processed_sensor_reading





