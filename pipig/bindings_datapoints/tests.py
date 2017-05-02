from appliances.tests import build_appliance_model
from binding_session.tests import build_session_sensor_model, build_session_appliance_model
from bindings_datapoints.datapoint_binding import DataPointsApplianceBinder, DataPointsSensorBinder, \
    IncorrectReadingTypeError
from bindings_datapoints.models import BindDataPointsAppliances, BindDataPointsSensors
from data_points.tests import build_datapoints
from general.patterns import Observer
from generics.constants import COMPONENT_TYPE_SENSOR, COMPONENT_TYPE_DATAPOINTS_SENSOR_BINDER, \
    COMPONENT_TYPE_DATAPOINTS_APPLIANCE_BINDER
from generics.models import GenericReading
from sensors.tests import helper_populate_sensor_readings
from test_helpers.test_base import BaseTestCase
from test_helpers.test_forms import FormTestCase
from test_helpers.test_generics import unwritten_test


#________________________________________________________________
#
# Unit Tests
#________________________________________________________________

class BindDataPointsSensorModelTests(BaseTestCase):
    def build_test_obj(self):
        return build_datapoint_sensor_model("Test", "T", 0.005, 0.02, None, [(0.0, 0.0), (10.0, 0.1), (20.0, 0.2), (30.0, 0.3)])

    def test_get_id(self):
        obj = self.build_test_obj()
        self.assertTrue(type(obj) == BindDataPointsSensors)
        self.assertTrue(obj.get_id() == 1, "%s should produce an ID of 1" % str(obj))

    def test_get_session_sensor_id(self):
        obj = self.build_test_obj()
        self.assertTrue(type(obj) == BindDataPointsSensors)
        self.assertTrue(obj.get_session_sensor_id() == 1, "%s should produce an SessionSensor ID of 1" % str(obj))

    def test_get_datapoint_id(self):
        obj = self.build_test_obj()
        self.assertTrue(type(obj) == BindDataPointsSensors)
        self.assertTrue(obj.get_datapoints_id() == 1, "%s should produce an DataPoint ID of 1" % str(obj))


class MockSensorDataPointsObserver(Observer):
    def __init__(self):
        Observer.__init__(self)
        self.reading = None

    def receive(self, result, status_code=0):
        self.reading = result

    def get_reading(self):
        return self.reading


class BindDataPointsSensorObjectTests(BaseTestCase):
    def build_test_obj(self):
        return build_datapoint_sensor_object("Test", "T", 0.005, 0.02, None,
                                            [(0.0, 0.0), (10.0, 0.1), (20.0, 0.2), (30.0, 0.3)])

    def test_get_id(self):
        obj = self.build_test_obj()
        self.assertTrue(obj.get_id() == 1, "%s should produce an ID of 1" % str(obj))

    def test_get_session_id(self):
        obj = self.build_test_obj()
        self.assertTrue(obj.get_session_id() == 1, "%s should produce an Session ID of 1" % str(obj))

    def test_get_sensor_id(self):
        obj = self.build_test_obj()
        self.assertTrue(obj.get_sensor_id() == 1, "%s should produce an Sensor ID of 1" % str(obj))

    def test_get_datapoint_id(self):
        obj = self.build_test_obj()
        self.assertTrue(obj.get_datapoints_id() == 1, "%s should produce an DataPoint ID of 1" % str(obj))

    def helper_get_datapoints_at_time_elapsed(self, obj, expected, time_elapsed):
        point = obj.get_datapoint_at_time_elapsed(time_elapsed)
        self.assertTrue(point.get_value() == expected, "%s should produce a value of %d, but is %d" % (str(point), expected, point.get_value()))

    def test_get_datapoint_at_time_elapsed(self):
        obj = self.build_test_obj()

        self.helper_get_datapoints_at_time_elapsed(obj, 0.0, 0.0)
        self.helper_get_datapoints_at_time_elapsed(obj, 10.0, 0.1)
        self.helper_get_datapoints_at_time_elapsed(obj, 30.0, 0.3)
        self.helper_get_datapoints_at_time_elapsed(obj, 30.0, 0.4)
        self.helper_get_datapoints_at_time_elapsed(obj, 5.0, 0.05)


    def helper_request_output(self, obj, time_elapsed, expected):
        observe = MockSensorDataPointsObserver()
        obj.attach(observe)

        result = obj.request_output(time_elapsed)

        self.assertTrue(result.get_value() == expected,
                        "%s should have a difference of %d, however is %d" % (str(obj), expected, result.get_value()))

        self.assertTrue(result.get_timestamp() == time_elapsed, "%s should have a time value of %d however is %d" % (str(obj), time_elapsed, result.get_timestamp()))

        self.assertTrue(result.get_component_type_id() == COMPONENT_TYPE_DATAPOINTS_SENSOR_BINDER, "%s should have a component type id of %d however is %d" % (str(obj), COMPONENT_TYPE_DATAPOINTS_SENSOR_BINDER, result.get_component_type_id()))

        self.assertTrue(result.get_component_id() == obj.get_id(), "%s should have a component if of %d however is %d" % (str(obj), obj.get_id(), result.get_component_id()))

        self.assertIsNotNone(observe.get_reading(), "%s should have notified an observer with a reading, however has not" % (str(obj)))


    def test_request_output(self):
        obj = self.build_test_obj()
        helper_populate_sensor_readings(obj.get_sensor_id(), [(2.0, 0.0), (10.0, 0.1), (18.0, 0.2), (28.0, 0.4)])

        self.helper_request_output(obj, time_elapsed=0.1, expected=0.0)
        self.helper_request_output(obj, time_elapsed=0.3, expected=-7.0)


    def helper_difference_between_reading_and_datapoint_at_time_elapsed(self, obj, time_elapsed, expected):
        observe = MockSensorDataPointsObserver()
        obj.attach(observe)

        result = obj.difference_between_reading_and_datapoint_at_time_elapsed(time_elapsed)
        self.assertTrue(result == expected,
                        "%s should have a difference of %d, however is %d" % (str(obj), expected, result))

    def test_difference_between_reading_and_datapoint_at_time_elapsed(self):
        obj = self.build_test_obj()
        helper_populate_sensor_readings(obj.get_sensor_id(), [(2.0, 0.0), (10.0, 0.1), (18.0, 0.2), (28.0, 0.4)])

        self.helper_difference_between_reading_and_datapoint_at_time_elapsed(obj, time_elapsed=0.0, expected=2.0)
        self.helper_difference_between_reading_and_datapoint_at_time_elapsed(obj, time_elapsed=0.1, expected=0.0)
        self.helper_difference_between_reading_and_datapoint_at_time_elapsed(obj, time_elapsed=0.2, expected=-2.0)

    def test_difference_between_reading_and_datapoint_at_time_elapsed_irregular_values(self):
        obj = self.build_test_obj()
        helper_populate_sensor_readings(obj.get_sensor_id(), [(2.0, 0.0), (10.0, 0.1), (18.0, 0.2), (28.0, 0.4)])

        self.helper_difference_between_reading_and_datapoint_at_time_elapsed(obj, time_elapsed=0.3, expected=-7.0)
        self.helper_difference_between_reading_and_datapoint_at_time_elapsed(obj, time_elapsed=0.4, expected=-2.0)


class BindDataPointsApplianceModelTests(BaseTestCase):
    def build_test_obj(self):
        return build_datapoint_appliance_model("Test", "T", None, [(0.0, 0.0), (10.0, 0.1), (20.0, 0.2), (30.0, 0.3)])

    def test_get_id(self):
        obj = self.build_test_obj()
        self.assertTrue(type(obj) == BindDataPointsAppliances)
        self.assertTrue(obj.get_id() == 1, "%s should produce an ID of 1" % str(obj))

    def test_session_appliance_id(self):
        obj = self.build_test_obj()
        self.assertTrue(type(obj) == BindDataPointsAppliances)
        self.assertTrue(obj.get_session_appliance_id() == 1, "%s should produce an SessionAppliance ID of 1" % str(obj))

    def test_datapoints_id(self):
        obj = self.build_test_obj()
        self.assertTrue(type(obj) == BindDataPointsAppliances)
        self.assertTrue(obj.get_datapoints_id() == 1, "%s should produce an DataPoints ID of 1" % str(obj))

    def test_polarity(self):
        obj = self.build_test_obj()
        self.assertTrue(type(obj) == BindDataPointsAppliances)
        self.assertTrue(obj.get_polarity() == 1, "%s should produce an Polarity of 1" % str(obj))


class BindDataPointsApplianceObjectTests(BaseTestCase):
    def build_test_obj(self, polarity=1):
        return build_datapoint_appliance_object("Test", "T", None, [(0.0, 0.0), (10.0, 0.1), (20.0, 0.2), (30.0, 0.3)], polarity)

    def test_get_id(self):
        obj = self.build_test_obj()
        self.assertTrue(obj.get_id() == 1, "%s should produce an ID of 1" % str(obj))

    def test_get_session_id(self):
        obj = self.build_test_obj()
        self.assertTrue(obj.get_session_id() == 1, "%s should produce an Session ID of 1" % str(obj))

    def test_get_appliance_id(self):
        obj = self.build_test_obj()
        self.assertTrue(obj.get_appliance_id() == 1, "%s should produce an Appliance ID of 1, however was %d" % (str(obj), obj.get_appliance_id()))

    def test_get_datapoints_id(self):
        obj = self.build_test_obj()
        self.assertTrue(obj.get_datapoints_id() == 1, "%s should produce an DataPoints ID of 1" % str(obj))

    def test_get_polarity(self):
        obj = self.build_test_obj()
        self.assertTrue(obj.get_binder_polarity() == 1, "%s should produce an Polarity of 1" % str(obj))

    def test_receive(self):
        obj = self.build_test_obj()

        reading = GenericReading(0, 0, 0, 0)
        self.assertRaises(IncorrectReadingTypeError, obj.receive, reading)

        try:
            reading = GenericReading(0, COMPONENT_TYPE_DATAPOINTS_SENSOR_BINDER, 0, 0)
        except IncorrectReadingTypeError:
            self.assertTrue(False, "Reading should not raise and error with the correct type id")


    def helper_test_calculate_output_value(self, polarity, input_reading, expected):
        obj = self.build_test_obj(polarity)
        result = obj.calculate_output_value(input_reading)
        self.assertTrue(result == expected, "%s should create an output value of %d, however was %d when the input value was %d" % (str(obj), expected, result, input_reading))

    def test_calculate_output_value_positive_polarity(self):

        self.helper_test_calculate_output_value(polarity=1, input_reading=-5, expected=0)
        self.helper_test_calculate_output_value(polarity=1, input_reading=5, expected=1)
        self.helper_test_calculate_output_value(polarity=1, input_reading=0, expected=0)

    def test_calculate_output_value_negative_polarity(self):
        self.helper_test_calculate_output_value(polarity=-1, input_reading=-5, expected=1)
        self.helper_test_calculate_output_value(polarity=-1, input_reading=5, expected=0)
        self.helper_test_calculate_output_value(polarity=-1, input_reading=0, expected=0)

    def test_calculate_output_value_no_polarity(self):
        self.helper_test_calculate_output_value(polarity=0, input_reading=-5, expected=0)
        self.helper_test_calculate_output_value(polarity=0, input_reading=5, expected=0)
        self.helper_test_calculate_output_value(polarity=0, input_reading=0, expected=0)

    def helper_readings_the_same_however_do_not_require_matching_ids(self, first_reading, second_reading):
        component = first_reading.get_component_id() is second_reading.get_component_id()
        component_type = first_reading.get_component_id() == second_reading.get_component_id()
        value = first_reading.get_value() == second_reading.get_value()
        timestamp = first_reading.get_timestamp() == second_reading.get_timestamp()
        return component and component_type and value and timestamp

    def test_generate_appliance_reading(self):
        obj = self.build_test_obj()
        input_reading = GenericReading(1, COMPONENT_TYPE_DATAPOINTS_SENSOR_BINDER, -5, 10.0)

        result = obj.generate_appliance_reading(input_reading)
        expected_reading = GenericReading(obj.get_id(), COMPONENT_TYPE_DATAPOINTS_APPLIANCE_BINDER, 0, 10.0)

        message = "%s should have a reading of %s however is %s" % (str(obj), str(expected_reading), str(result))
        self.assertTrue(self.helper_readings_the_same_however_do_not_require_matching_ids(result, expected_reading), message)

# ________________________________________________________________
#
# Builders to use in Unit Tests
# ________________________________________________________________


def build_datapoint_sensor_model(base_name, display_units, minimum_refresh, interval_between_readings, gpio_pin_number=None, datapoints_tuple_list = None):
    session_sensor = build_session_sensor_model(base_name, display_units, minimum_refresh, interval_between_readings, gpio_pin_number=None)
    datapoints = build_datapoints(base_name, datapoints_tuple_list)

    datapoint_sensor = BindDataPointsSensors.create(session_sensor_id=session_sensor.get_id(), datapoints_id=datapoints.get_id())
    return datapoint_sensor


def build_datapoint_appliance_model(base_name, display_units, gpio_pin_number=None, datapoints_tuple_list = None, polarity=1):
    session_appliance = build_session_appliance_model(base_name, display_units, gpio_pin_number=None)
    datapoints = build_datapoints(base_name, datapoints_tuple_list)
    datapoint_appliance = BindDataPointsAppliances.create(session_appliance_id=session_appliance.get_id(), datapoints_id=datapoints.get_id(), polarity=polarity)
    return datapoint_appliance


def build_datapoint_sensor_object(base_name, display_units, minimum_refresh, interval_between_readings, gpio_pin_number=None, datapoint_tuple_list=None):
    datapoints_sensor = build_datapoint_sensor_model(base_name, display_units, minimum_refresh, interval_between_readings, gpio_pin_number, datapoint_tuple_list)
    result = DataPointsSensorBinder(datapoints_sensor.get_id())
    return result


def build_datapoint_appliance_object(base_name, display_units, gpio_pin_number=None, datapoint_tuple_list=None, polarity=1):
    datapoints_appliance = build_datapoint_appliance_model(base_name, display_units, gpio_pin_number, datapoint_tuple_list, polarity)
    result = DataPointsApplianceBinder(datapoints_appliance.get_id())
    return result



