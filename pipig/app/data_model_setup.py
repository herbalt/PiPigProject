from pipig.appliances.models import Appliance
from pipig.binders.models import BindDatapointsAppliances, BindDatapointsSensors
from pipig.curing_sessions.models import CuringSession
from pipig.data_points.models import DataPoints, DataPoint
from pipig.recipes.models import Recipe
from pipig.sensors.models import Sensor
from pipig import app

def data_setup_sensors():
    sensor_1 = Sensor.create(name="Sensor1", type_id=1, interval_between_readings=0.5, gpio_pin_id=None)
    sensor_2 = Sensor.create(name="Sensor2", type_id=1, interval_between_readings=0.25, gpio_pin_id=None)
    sensor_3 = Sensor.create(name="Sensor3", type_id=1, interval_between_readings=0.5, gpio_pin_id=None)

    return [sensor_1.get_id(), sensor_2.get_id(), sensor_3.get_id()]

def data_setup_datapoints():
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
    appliance_1 = Appliance.create(name="appliance1", type_id=1, gpio_pin_id=None)
    appliance_2 = Appliance.create(name="appliance2", type_id=1, gpio_pin_id=None)
    appliance_3 = Appliance.create(name="appliance3", type_id=1, gpio_pin_id=None)
    appliance_4 = Appliance.create(name="appliance4", type_id=1, gpio_pin_id=None)
    appliance_5 = Appliance.create(name="appliance5", type_id=1, gpio_pin_id=None)

    return [appliance_1.get_id(), appliance_2.get_id(), appliance_3.get_id(), appliance_4.get_id(), appliance_5.get_id()]

if __name__ == "__main__":
    with app.app_context():
        sensor_ids = data_setup_sensors()
        datapoints_ids = data_setup_datapoints()
        appliance_ids = data_setup_appliances()
    print "Sensors: " + str(sensor_ids) + "\nDatapoints: " + str(datapoints_ids) + "\nAppliances: " + str(appliance_ids)
