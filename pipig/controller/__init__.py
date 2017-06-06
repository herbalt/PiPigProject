from controller_api import ControllerApi
from time import sleep
from app import data_setup as generics
from pipig import app

from pipig.recipes.models import Recipe
from pipig.curing_sessions.models import CuringSession
from pipig.sensors.models import Sensor
from pipig.data_points.models import DataPoints, DataPoint
from pipig.appliances.models import Appliance
from pipig.binders.models import BindDatapointsAppliances, BindDatapointsSensors
from datetime import datetime
if __name__ == "__main__":



    # generics.data_setup()

    with app.app_context():
        recipe = Recipe.create(name="InitRecipe")
        session = CuringSession.create(name="InitCuringSession", start_time=datetime.now())

        recipe_id = recipe.get_id()
        session_id = session.get_id()

        sensor_1 = Sensor.create(name="Sensor1", type_id=1, interval_between_readings=0.5, gpio_pin_id=None)
        sensor_2 = Sensor.create(name="Sensor2", type_id=1, interval_between_readings=0.25, gpio_pin_id=None)
        sensor_3 = Sensor.create(name="Sensor3", type_id=1, interval_between_readings=0.5, gpio_pin_id=None)

        datapoints_1 = DataPoints.create(name="datapoints1")
        datapoint_id = datapoints_1.get_id()
        DataPoint.create(data_points_id=datapoint_id, value=10, time_elapsed=0)
        DataPoint.create(data_points_id=datapoint_id, value=5, time_elapsed=1)
        DataPoint.create(data_points_id=datapoint_id, value=15, time_elapsed=2)
        DataPoint.create(data_points_id=datapoint_id, value=5, time_elapsed=3)

        datapoints_2 = DataPoints.create(name="datapoints2")
        datapoint_id = datapoints_2.get_id()
        DataPoint.create(data_points_id=datapoint_id, value=1, time_elapsed=0)
        DataPoint.create(data_points_id=datapoint_id, value=2, time_elapsed=0.5)
        DataPoint.create(data_points_id=datapoint_id, value=3, time_elapsed=1.0)
        DataPoint.create(data_points_id=datapoint_id, value=4, time_elapsed=1.5)

        appliance_1 = Appliance.create(name="appliance1", type_id=1, gpio_pin_id=None)
        appliance_2 = Appliance.create(name="appliance2", type_id=1, gpio_pin_id=None)
        appliance_3 = Appliance.create(name="appliance3", type_id=1, gpio_pin_id=None)
        appliance_4 = Appliance.create(name="appliance4", type_id=1, gpio_pin_id=None)
        appliance_5 = Appliance.create(name="appliance5", type_id=1, gpio_pin_id=None)

        sensor_binder_1 = BindDatapointsSensors.create(recipe_id=recipe_id, datapoints_id=1, sensor_id=1)
        sensor_binder_2 = BindDatapointsSensors.create(recipe_id=recipe_id, datapoints_id=1, sensor_id=2)
        sensor_binder_3 = BindDatapointsSensors.create(recipe_id=recipe_id, datapoints_id=2, sensor_id=2)

        appliance_binder_1 = BindDatapointsAppliances.create(recipe_id=recipe_id, datapoints_id=1, appliance_id=1, polarity=1)
        appliance_binder_2 = BindDatapointsAppliances.create(recipe_id=recipe_id, datapoints_id=1, appliance_id=2, polarity=-1)
        appliance_binder_3 = BindDatapointsAppliances.create(recipe_id=recipe_id, datapoints_id=2, appliance_id=3, polarity=-1)
        appliance_binder_4 = BindDatapointsAppliances.create(recipe_id=recipe_id, datapoints_id=2, appliance_id=4, polarity=-1)
        appliance_binder_5 = BindDatapointsAppliances.create(recipe_id=recipe_id, datapoints_id=2, appliance_id=5, polarity=0)

        controller = ControllerApi(recipe_id, session_id)

        controller.start()

        sleep(10)

        controller.stop()

