from abc import ABCMeta

from pipig.controller.controller_api import ControllerApi
from time import sleep
from pipig import app

from pipig.curing_sessions.models import CuringSession
from pipig.binders.models import BindDatapointsAppliances, BindDatapointsSensors
from time import time

from recipes.models import Recipe


class TrialCreator:
    __metaclass__ = ABCMeta

    def __init__(self, trial_name, list_of_sensor_binder_tuples=[], list_of_appliance_binder_tuples=[]):
        self.recipe = Recipe(trial_name)
        self.recipe = Recipe.create(name="recipe_" + trial_name)
        self.session = CuringSession.create(name="session_" + trial_name, start_time=time())


        self.list_of_sensor_binder_tuples = list_of_sensor_binder_tuples
        self.list_of_appliance_binder_tuples = list_of_appliance_binder_tuples

        self.list_of_sensor_binders = self.define_bind_datapoints_sensors(list_of_sensor_binder_tuples)
        self.list_of_appliance_binders = self.define_bind_datapoints_appliances(list_of_appliance_binder_tuples)

    def get_recipe_id(self):
        return self.recipe.get_id()

    def get_session_id(self):
        return self.session.get_id()

    def get_sensor_ids(self):
        sensor_list = []
        for binder in self.list_of_sensor_binder_tuples:
            object_id = binder[1]
            if not sensor_list.__contains__(object_id):
             sensor_list.append(object_id)
        return sensor_list

    def get_datapoints_ids(self):
        datapoints_list = []
        for binder in self.list_of_appliance_binder_tuples:
            object_id = binder[1]
            if not datapoints_list.__contains__(object_id):
                datapoints_list.append(object_id)

        for binder in self.list_of_sensor_binder_tuples:
            object_id = binder[1]
            if not datapoints_list.__contains__(object_id):
                datapoints_list.append(object_id)

        return datapoints_list

    def get_appliance_ids(self):
        appliance_list = []
        for binder in self.list_of_appliance_binder_tuples:
            object_id = binder[1]
            if not appliance_list.__contains__(object_id):
                appliance_list.append(binder[1])
        return appliance_list

    def get_sensor_binder_tuples(self):
        return self.list_of_sensor_binder_tuples

    def get_appliance_binder_tuples(self):
        return self.list_of_appliance_binder_tuples

    def define_bind_datapoints_sensors(self, list_of_sensor_binder_tuples):
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

    def define_bind_datapoints_appliances(self, list_of_appliance_binder_tuples):
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


def trial_run(name="", sensor_binders_tuples=[], appliance_binders_tuples=[], duration=10):
    with app.app_context():
        trial = TrialCreator(name, sensor_binders_tuples, appliance_binders_tuples)
        controller = ControllerApi(trial.get_recipe_id(), trial.get_session_id())
        controller.start()

        sleep(duration)

        controller.stop()

if __name__ == "__main__":

    trial_run("Trial 1", [(1, 2), (2, 2)], [(1, 2, -1), (1, 2, 1), (2, 2, -1)], 1000)

