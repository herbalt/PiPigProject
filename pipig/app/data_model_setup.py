from pipig.appliances.models import Appliance
from pipig.data_points.models import DataPoints, DataPoint
from pipig.sensors.models import Sensor
from pipig import app
from pipig.appliances.data_setup import helper_setup_appliances
from pipig.sensors.data_setup import helper_setup_sensors
from pipig.factories.factory import APPLIANCE_TYPE_NAME_RELAY, APPLIANCE_TYPE_NAME_BASIC, SENSOR_TYPE_NAME_BASIC, SENSOR_TYPE_NAME_DHT22_CELSIUS



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
    datapoints_1 = DataPoints.create(name="datapoints1")
    datapoints_1_id = datapoints_1.get_id()
    DataPoint.create(data_points_id=datapoints_1_id, value=10, time_elapsed=0)
    DataPoint.create(data_points_id=datapoints_1_id, value=5, time_elapsed=1)
    DataPoint.create(data_points_id=datapoints_1_id, value=15, time_elapsed=2)
    DataPoint.create(data_points_id=datapoints_1_id, value=5, time_elapsed=3)

    datapoints_2 = DataPoints.create(name="datapoints2")
    datapoints_2_id = datapoints_2.get_id()
    DataPoint.create(data_points_id=datapoints_2_id, value=1, time_elapsed=0)
    DataPoint.create(data_points_id=datapoints_2_id, value=2, time_elapsed=0.5)
    DataPoint.create(data_points_id=datapoints_2_id, value=3, time_elapsed=1.0)
    DataPoint.create(data_points_id=datapoints_2_id, value=4, time_elapsed=1.5)

    return [datapoints_1.get_id(), datapoints_2.get_id()]

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
