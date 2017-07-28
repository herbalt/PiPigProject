from pipig.data import db, CRUDMixin
from recipes.models import Recipe
from pipig.pi_gpio.models import RaspberryPi
from pipig.controller.controller import Controller
from curing_sessions.models import CuringSession

class PiPigStatus():
    NOT_CONFIGURED = {'code': 0, 'name': 'Not Configured'}
    CONFIGURED = {'code': 1, 'name': 'Configured'}
    ACTIVE = {'code': 2, 'name': 'Active'}
    FINISHED = {'code': 3, 'name': 'Finished'}

    def get_status(self, status_code):
        if status_code == self.NOT_CONFIGURED.get('code'):
            return self.NOT_CONFIGURED
        elif status_code == self.CONFIGURED.get('code'):
            return self.CONFIGURED
        elif status_code == self.ACTIVE.get('code'):
            return self.ACTIVE
        elif status_code == self.FINISHED.get('code'):
            return self.FINISHED
        else:
            return self.NOT_CONFIGURED


class PiPig(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    recipe_id = db.Column(db.Integer, nullable=False)
    session_id = db.Column(db.Integer, nullable=True)
    pi_id = db.Column(db.Integer, nullable=True)

    def __init__(self, recipe_id, pi_id, session_name):
        self.session = None
        self.recipe = None
        self.pi = None
        self.controller = None

        self.status = PiPigStatus.NOT_CONFIGURED
        response_status = self.__configure(recipe_id, pi_id, session_name)
        if response_status == PiPigStatus.NOT_CONFIGURED:
            self.session = None
            self.recipe = None
            self.pi = None
            self.controller = None

    def __configure(self, recipe_id, pi_id, session_name):
        """
        Build the PiPig on the Server to allow the application to function
        :return:
        """

        self.session = CuringSession.create(name=session_name)
        if self.session is not None:
            self.session_id = self.session.get_id()


        self.recipe = Recipe.get(recipe_id)
        if self.recipe is not None:
            self.recipe_id = self.recipe.get_id()

        if self.session is None or self.recipe is None:
            return self.status

        self.controller = Controller(recipe_id=self.recipe_id, curing_session_id=self.session_id)
        self.__build_rasp_pi(pi_id, self.controller)

        self.status = PiPigStatus.CONFIGURED

    def __build_rasp_pi(self, pi_id, controller):
        self.pi = RaspberryPi.get(pi_id)
        if self.pi is not None:
            self.pi_id = self.pi.get_id()
            sensor_objs = controller.get_sensor_objects()
            appliance_objs = controller.get_appliance_objects()

            # Build list of GPIO ids to configure the Raspberry Pi
            sensor_gpio_list = []
            for sensor in sensor_objs:
                sensor_gpio_list.append(sensor.get_gpio_pin())

            appliance_gpio_list = []
            for appliance in appliance_objs:
                if appliance.get_gpio_pin() is not None:
                    appliance_gpio_list.append(appliance.get_gpio_pin())

            self.pi.configure_application(input_pin_list=sensor_gpio_list, output_pin_list=appliance_gpio_list)
        return self.pi

    def get_status(self):
        return self.status

    def start(self):
        """
        Set the Session Time
        Start the Queues
        Start the Sensors
        Set the PiPig Status
        :return:
        """
        from time import time
        self.session.set_start_time(time())

    def stop(self):
        """
        Set the End Time for the Session
        Stop the Sensors
        Stop the Queues
        Set the PiPig Status
        :return:
        """
