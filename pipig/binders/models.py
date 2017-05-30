from pipig.data import db, CRUDMixin




class BindDatapoitnsSensors(db.Model, CRUDMixin):
    """
    Binds a Sensor to a Session
    """
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    recipe_id = db.Column(db.Integer, nullable=False)
    datapoints_id = db.Column(db.Integer, nullable=False)
    sensor_id = db.Column(db.Integer, nullable=False)

    def __init__(self, recipe_id, datapoints_id, sensor_id):
        self.recipe_id = recipe_id
        self.datapoints_id = datapoints_id
        self.sensor_id = sensor_id

    def __str__(self):
        return "Binder ID: " + str(self.get_id()) + "\nRecipe ID: " + str(self.get_recipe_id()) + "\nDatapoints ID: " + str(self.get_datapoints_id()) + "\nSensor ID: " + str(self.get_sensor_id())

    def get_id(self):
        return self.id

    def get_recipe_id(self):
        return self.recipe_id

    def get_datapoints_id(self):
        return self.datapoints_id

    def get_sensor_id(self):
        return self.sensor_id


class BindDatapoitnsAppliances(db.Model, CRUDMixin):
    """
    Binds a Sensor to a Session
    """
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    recipe_id = db.Column(db.Integer, nullable=False)
    datapoints_id = db.Column(db.Integer, nullable=False)
    appliance_id = db.Column(db.Integer, nullable=False)
    polarity = db.Column(db.Integer, nullable=True)

    def __init__(self, recipe_id, datapoints_id, appliance_id, polarity=1):
        self.recipe_id = recipe_id
        self.datapoints_id = datapoints_id
        self.appliance_id = appliance_id
        self.polarity = polarity

    def __str__(self):
        return "Binder ID: " + str(self.get_id()) + "\nRecipe ID: " + str(self.get_recipe_id()) + "\nDatapoints ID: " + str(self.get_datapoints_id()) + "\nAppliance ID: " + str(self.get_appliance_id())

    def get_id(self):
        return self.id

    def get_recipe_id(self):
        return self.recipe_id

    def get_datapoints_id(self):
        return self.datapoints_id

    def get_appliance_id(self):
        return self.appliance_id

    def get_polarity(self):
        polarity = self.polarity
        if polarity is None:
            return 1
        elif polarity >= 1:
            return 1
        elif polarity < 0:
            return -1
        else:
            return 0







