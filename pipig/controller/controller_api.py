from controller import Controller

class ControllerApi():
    def __init__(self, recipe_id, session_id=None):
        self.controller = Controller(recipe_id, session_id)

    def start(self):
        """
        Starts Sensors and Queues of the Controller
        :return: 
        """
        pass

    def stop(self):
        """
        Stops the Sensors and Queues of the Controller
        :return: 
        """
        pass

    def pause(self):
        """
        THIS MAY NOT BE NEEDED
        Stops the processing of Readings from entering the Queues
        :return: 
        """
        pass