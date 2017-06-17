from abc import abstractmethod, ABCMeta
from time import sleep
from time import time

from pipig import app
from pipig.binders.models import BindDatapointsAppliances, BindDatapointsSensors
from pipig.controller.controller_api import Controller
from pipig.curing_sessions.models import CuringSession
from pipig.pi_gpio.raspberry_pi import BaseRaspberryPi, PI_2_MODEL_B
from recipes.data_setup import recipe_creator
from recipes.models import Recipe

class TrialCreator:
    """
    Collates all the components and binds the entire application together.

    """

    controller = None
    rasp_pi = None

    def __init__(self, pi_model, recipe_id):
        """

        :param trial_name:
        :param list_of_sensor_binder_tuples:
        :param list_of_appliance_binder_tuples:
        """
        self.recipe_id = recipe_id
        with app.app_context():
            self.recipe = Recipe.get(id=self.recipe_id)
            self.session = CuringSession.create(name=self.recipe.get_name(), start_time=time())
            self.session_id = self.session.get_id()

        # Init Interaction objects
        self.get_controller()
        self.get_rasp_pi(pi_model)

    """
    GETTERS
    """
    def get_recipe_id(self):
        return self.recipe_id

    def get_session_id(self):
        return self.session_id

    def get_sensor_ids(self):
        sensor_list = []
        for binder in self.recipe.get_list_sensor_binder_id_tuples():
            object_id = binder[1]
            if not sensor_list.__contains__(object_id):
             sensor_list.append(object_id)
        return sensor_list

    def get_datapoints_ids(self):
        datapoints_list = []
        for binder in self.recipe.get_list_of_appliance_binder_tuples():
            object_id = binder[1]
            if not datapoints_list.__contains__(object_id):
                datapoints_list.append(object_id)

        for binder in self.recipe.get_list_sensor_binder_id_tuples():
            object_id = binder[1]
            if not datapoints_list.__contains__(object_id):
                datapoints_list.append(object_id)

        return datapoints_list

    def get_appliance_ids(self):
        appliance_list = []
        for binder in self.recipe.get_list_of_appliance_binder_tuples():
            object_id = binder[1]
            if not appliance_list.__contains__(object_id):
                appliance_list.append(binder[1])
        return appliance_list

    def get_controller(self):
        if self.controller is None:
            self.controller = Controller(self.get_recipe_id(), self.get_session_id())
        return self.controller

    def get_rasp_pi(self, pi_model):
        if self.rasp_pi is None:
            sensor_objs = self.get_controller().get_sensor_objects()
            appliance_objs = self.get_controller().get_appliance_objects()

            # Build list of GPIO ids to configure the Raspberry Pi
            sensor_gpio_list = []
            for sensor in sensor_objs:
                sensor_gpio_list.append(sensor.get_gpio_pin())

            appliance_gpio_list = []
            for appliance in appliance_objs:
                if appliance.get_gpio_pin() is not None:
                    appliance_gpio_list.append(appliance.get_gpio_pin())

            self.rasp_pi = BaseRaspberryPi(pi_model=pi_model)
            self.rasp_pi.configure_application(input_pin_list=sensor_gpio_list, output_pin_list=appliance_gpio_list)
        return self.rasp_pi

    """
    API
    """
    def run(self, duration=-1):
        if duration <= 0:
            with app.app_context():
                while True:
                    try:
                        self.get_controller().start()
                    except KeyboardInterrupt:
                        self.get_controller().stop()
        else:
            with app.app_context():
                self.get_controller().start()
                sleep(duration)
                self.get_controller().stop()


if __name__ == "__main__":

    with app.app_context():
        recipe_id = recipe_creator(recipe_name="Trial 3",
                                   list_of_sensor_binder_tuples=[(2, 8), (2, 7)],
                                   list_of_appliance_binder_tuples=[(1, 9, -1), (2, 8, 1), (2, 9, -1)])

        trial = TrialCreator(pi_model=PI_2_MODEL_B, recipe_id=recipe_id)

        trial.run(10)


