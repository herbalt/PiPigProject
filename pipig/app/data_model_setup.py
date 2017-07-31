from appliances.models import Appliance
from data_points.models import DataPoints, DataPoint
from sensors.models import Sensor
from pipig import app
from appliances.data_setup import helper_setup_appliances
from sensors.data_setup import helper_setup_sensors
from factories.factory import APPLIANCE_TYPE_NAME_RELAY, APPLIANCE_TYPE_NAME_BASIC, SENSOR_TYPE_NAME_BASIC, SENSOR_TYPE_NAME_DHT22_CELSIUS



def data_setup_sensors():
    """
    Setup the generic data models for the Sensors
    :return: List of the IDs created
    """
    sensor_list = []
    sensor_list.append(helper_setup_sensors(factory_type_constant=SENSOR_TYPE_NAME_BASIC, sensor_name="Sensor1",
                                            interval_between_readings=0.5, gpio_pin_id=None))
    sensor_list.append(helper_setup_sensors(factory_type_constant=SENSOR_TYPE_NAME_BASIC, sensor_name="Sensor2",
                                            interval_between_readings=0.25, gpio_pin_id=None))
    sensor_list.append(helper_setup_sensors(factory_type_constant=SENSOR_TYPE_NAME_BASIC, sensor_name="Sensor3",
                                            interval_between_readings=0.5, gpio_pin_id=None))
    sensor_list.append(helper_setup_sensors(factory_type_constant=SENSOR_TYPE_NAME_DHT22_CELSIUS, sensor_name="GPIO Temperature1",
                                            interval_between_readings=2.0, gpio_pin_id=7))
    return sensor_list


def data_setup_datapoints():
    """
    Setup the generic data models for the DataPoints
    Includes steps to set the points
    :return: List of the IDs created
    """
    datapoints_list = []
    datapoints_list.append(helper_datapoints("datapoints1", [(10, 0), (5, 1), (15, 2), (5, 3)]).get_id())
    datapoints_list.append(helper_datapoints("datapoints2", [(1, 0), (2, 0.5), (3, 1.0), (4, 1.5)]).get_id())
    return datapoints_list


def helper_datapoints(name, list_value_time_elapsed_pairs):
    datapoints = DataPoints.create(name=name)
    datapoints_id = datapoints.get_id()
    for value_time_pair in list_value_time_elapsed_pairs:
        helper_datapoint(datapoints_id, value=value_time_pair[0], time_elapsed=value_time_pair[1])
    return datapoints


def helper_datapoint(datapoints_id, value, time_elapsed):
    datapoint = DataPoint.query.filter_by(data_points_id=datapoints_id).filter_by(value=value).filter_by(time_elapsed=time_elapsed).first()
    if datapoint is None:
        datapoint = DataPoint.create(data_points_id=datapoints_id, value=value, time_elapsed=time_elapsed)
    return datapoint


def data_setup_appliances():
    """
    Setup the generic data models for the Appliances
    :return: List of the IDs created
    """
    appliance_list = []
    appliance_list.append(helper_setup_appliances(APPLIANCE_TYPE_NAME_BASIC, "appliance1", gpio_pin_id=None))
    appliance_list.append(helper_setup_appliances(APPLIANCE_TYPE_NAME_BASIC, "appliance2", gpio_pin_id=None))
    appliance_list.append(helper_setup_appliances(APPLIANCE_TYPE_NAME_BASIC, "appliance3", gpio_pin_id=None))
    appliance_list.append(helper_setup_appliances(APPLIANCE_TYPE_NAME_BASIC, "appliance4", gpio_pin_id=None))
    appliance_list.append(helper_setup_appliances(APPLIANCE_TYPE_NAME_BASIC, "appliance5", gpio_pin_id=None))
    appliance_list.append(helper_setup_appliances(APPLIANCE_TYPE_NAME_RELAY, "gpio_appliance1", gpio_pin_id=13))
    appliance_list.append(helper_setup_appliances(APPLIANCE_TYPE_NAME_RELAY, "gpio_appliance2", gpio_pin_id=15))
    return appliance_list

if __name__ == "__main__":
    """
    Creates all standard Sensors, Appliances and Datapoints Models in the database
    """
    with app.app_context():
        sensor_ids = data_setup_sensors()
        datapoints_ids = data_setup_datapoints()
        appliance_ids = data_setup_appliances()
    print "Sensors: " + str(sensor_ids) + "\nDatapoints: " + str(datapoints_ids) + "\nAppliances: " + str(appliance_ids)
