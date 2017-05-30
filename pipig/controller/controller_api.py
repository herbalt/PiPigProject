from controller import Controller

class ControllerApi():
    def __init__(self, recipe_id, session_id=None):
        self.controller = Controller(recipe_id, session_id)

    def start(self):
        """
        Starts Sensors and Queues of the Controller
        :return: 
        """
        self.controller.start_sensor_queue_processing()
        self.controller.start_appliance_queue_processing()
        self.controller.start_sensors()

    def stop(self):
        """
        Stops the Sensors and Queues of the Controller
        :return: 
        """
        self.controller.stop_sensors()
        self.controller.stop_sensor_queue_processing()
        self.controller.stop_appliance_queue_processing()
