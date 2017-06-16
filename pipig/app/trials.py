from time import sleep
from time import time
from pipig import app
from pipig.binders.models import BindDatapointsAppliances, BindDatapointsSensors
from pipig.controller.controller_api import ControllerApi
from pipig.curing_sessions.models import CuringSession
from recipes.models import Recipe
from pipig.pi_gpio.raspberry_pi import BaseRaspberryPi, PI_2_MODEL_B
from abc import abstractmethod, ABCMeta


class BaseTrialCreator:
    """
    Collates all the components and binds the entire application together.

    """
    __metaclass__ = ABCMeta

    def __init__(self, pi_model):
        """

         :param trial_name:
         :param list_of_sensor_binder_tuples:
         :param list_of_appliance_binder_tuples:
         """
        self.pi_model = pi_model



        # Create the high level objects
        self.build_high_level_objects()

        # Binder Tuple Storage
        self.list_of_sensor_binder_tuples = list_of_sensor_binder_tuples
        self.list_of_appliance_binder_tuples = list_of_appliance_binder_tuples

        # Build Binder objects
        self.list_of_sensor_binders = self.__define_bind_datapoints_sensors(self.list_of_sensor_binder_tuples)
        self.list_of_appliance_binders = self.__define_bind_datapoints_appliances(self.list_of_appliance_binder_tuples)

        # Init Interaction objects
        self.get_controller()
        self.get_rasp_pi(pi_model)

    @abstractmethod
    def build_high_level_objects(self):
        pass

    @abstractmethod
    def define_sensor_binders(self):
        return None

    @abstractmethod
    def define_appliance_binders(self):
        return None


class TrialCreatorFromRecipe(BaseTrialCreator):
    def __init__(self, pi_model, recipe_id):
        BaseTrialCreator.__init__(self, pi_model)
        self.recipe_id = recipe_id

    """
    BUILDERS
    """

    def build_high_level_objects(self):
        # Create the high level objects
        self.recipe = Recipe.get(id=self.recipe_id)
        self.session = CuringSession.create(name=self.recipe.get_name(), start_time=time())


class TrialCreatorFromValuePairs(BaseTrialCreator):
    def __init__(self, pi_model, trial_name, list_of_sensor_binder_tuples=[], list_of_appliance_binder_tuples=[]):
        BaseTrialCreator.__init__(self, pi_model)
        self.trial_name = trial_name
        self.list_of_sensor_binder_tuples = list_of_sensor_binder_tuples
        self.list_of_appliance_binder_tuples = list_of_appliance_binder_tuples

    """
    BUILDERS
    """
    def build_high_level_objects(self, trial_name=None):
        # Create the high level objects

        self.recipe = Recipe.create(name="recipe_" + trial_name)
        self.session = CuringSession.create(name="session_" + trial_name, start_time=time())



class TrialCreatorNew:
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

        # Create the high level objects
        self.build_high_level_objects()

        # Init Interaction objects
        self.get_controller()
        self.get_rasp_pi(pi_model)

    """
    BUILDERS
    """

    def build_high_level_objects(self):
        # Create the high level objects
        self.recipe = Recipe.get(id=self.recipe_id)
        self.session = CuringSession.create(name=self.recipe.get_name(), start_time=time())


    """
    GETTERS
    """
    def get_recipe_id(self):
        return self.recipe.get_id()

    def get_session_id(self):
        return self.session.get_id()

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
            self.controller = ControllerApi(self.get_recipe_id(), self.get_session_id())
        return self.controller

    def get_rasp_pi(self, pi_model):
        if self.rasp_pi is None:
            sensor_objs = self.get_controller().get_sensor_objects()
            appliance_objs = self.get_controller().get_appliance_objects()

            # Build list of GPIO ids to configure the Raspberry Pi
            sensor_gpio_list = []
            for sensor in sensor_objs:
                sensor_gpio_list.append(sensor.get_gpio_pin_id())

            appliance_gpio_list = []
            for appliance in appliance_objs:
                appliance_gpio_list.append(appliance.get_gpio_pin_id())

            self.rasp_pi = BaseRaspberryPi(pi_model=pi_model)
            self.rasp_pi.configure_application(input_pin_list=sensor_gpio_list, output_pin_list=appliance_gpio_list)
        return self.rasp_pi

    """
    Internal configuration
    """
    def __define_bind_datapoints_sensors(self, list_of_sensor_binder_tuples):
        """
        list_of_sensor_binder_tuples: (datapoints_id, sensor_id)
        Example: [(1,2), (2,2), (1,1))

        A list of the IDs for the relevant Sensors Binders to use in the trial
        :return: list_of_sensor_binder_ids
        """
        list_of_sensor_binder = []
        for binder_tuple in list_of_sensor_binder_tuples:
            binder = BindDatapointsSensors.create(recipe_id=self.recipe.get_id(), datapoints_id=binder_tuple[0], sensor_id=binder_tuple[1])
            list_of_sensor_binder.append(binder.id)
        return list_of_sensor_binder

    def __define_bind_datapoints_appliances(self, list_of_appliance_binder_tuples):
        """
        list_of_appliance_binder_tuples: (datapoints_id, appliance_id, polarity)
        Example: [(1, 2, -1), (2, 4, 1), (1, 5, 1))

        A list of the IDs for the relevant Appliance Binders to use in the trial
        :return: list_of_sensor_binder_ids
        """
        list_of_appliance_binder = []
        for binder_tuple in list_of_appliance_binder_tuples:
            binder = BindDatapointsAppliances.create(recipe_id=self.recipe.get_id(), datapoints_id=binder_tuple[0],
                                                  appliance_id=binder_tuple[1])
            list_of_appliance_binder.append(binder.id)
        return list_of_appliance_binder


    """
    API
    """
    def run(self, duration=-1):
        if duration <= 0:
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

def define_bind_datapoints_sensors(recipe_id, list_of_sensor_binder_tuples):
    """
    list_of_sensor_binder_tuples: (datapoints_id, sensor_id)
    Example: [(1,2), (2,2), (1,1))

    A list of the IDs for the relevant Sensors Binders to use in the trial
    :return: list_of_sensor_binder_ids
    """
    list_of_sensor_binder = []
    for binder_tuple in list_of_sensor_binder_tuples:
        binder = BindDatapointsSensors.create(recipe_id=recipe_id, datapoints_id=binder_tuple[0], sensor_id=binder_tuple[1])
        list_of_sensor_binder.append(binder.id)
    return list_of_sensor_binder

def define_bind_datapoints_appliances(recipe_id, list_of_appliance_binder_tuples):
    """
    list_of_appliance_binder_tuples: (datapoints_id, appliance_id, polarity)
    Example: [(1, 2, -1), (2, 4, 1), (1, 5, 1))

    A list of the IDs for the relevant Appliance Binders to use in the trial
    :return: list_of_sensor_binder_ids
    """
    list_of_appliance_binder = []
    for binder_tuple in list_of_appliance_binder_tuples:
        binder = BindDatapointsAppliances.create(recipe_id=recipe_id, datapoints_id=binder_tuple[0],
                                              appliance_id=binder_tuple[1])
        list_of_appliance_binder.append(binder.id)
    return list_of_appliance_binder


def recipe_creator(recipe_name="", list_of_sensor_binder_tuples=[],
                            list_of_appliance_binder_tuples=[]):
    recipe = Recipe(recipe_name)
    # Binder Tuple Storage
    recipe_id = recipe.get_id()
    define_bind_datapoints_sensors(recipe_id, list_of_sensor_binder_tuples)
    define_bind_datapoints_appliances(recipe_id, list_of_appliance_binder_tuples)
    return recipe_id



if __name__ == "__main__":

    recipe_id = recipe_creator(recipe_name="Trial 3",
                               list_of_sensor_binder_tuples=[(2, 8), (2, 7)],
                               list_of_appliance_binder_tuples=[(1, 9, -1), (2, 12, 1), (2, 12, -1)])

    trial = TrialCreatorNew(pi_model=PI_2_MODEL_B, recipe_id=recipe_id)

    trial.run(10)


