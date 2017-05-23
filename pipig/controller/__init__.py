from pipig.sessions.models import Session


class Controller:
    """
    Container for creating and binding all the Objects in a Recipe
    Input Queue takes Processed Sensor readings
    Processes the Queue by comparing against datapoints to build a New Reading for the Appliance
    Pass the Appliance Reading to another Queue that is pushes results to the relevant appliances
    """
    def __init__(self, recipe_id, session_id=None):
        self.recipe_id = recipe_id
        self.session_id = session_id
        self.build_controller()

    """
    GET Methods
    """
    def get_recipe_id(self):
        return self.recipe_id

    def get_session_id(self):
        return self.session_id

    def get_recipe_obj(self):
        pass

    def get_session_obj(self):
        if self.get_session_id() is None:
            return Session("GenericSession")
        else:
            session = Session.get(self.get_session_id())
            if session is None:
                return Session("GenericSession")
            return Session.get(self.get_session_id())

    """
    Build Methods
    """
    def build_controller(self):
        """
        Main method to call from init to construct the environment
        :return: 
        """
        self.build_objects()
        self.bind_objects()

    def build_objects(self):
        pass

    def bind_objects(self):
        pass

    """
    Interactions
    """