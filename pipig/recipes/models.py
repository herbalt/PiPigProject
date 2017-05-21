from pipig.data import db, CRUDMixin


class Recipe(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)

    def __init__(self, name):
        self.name = name

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_sensor_datapoints_binding_ids(self):
        return []

    def get_appliance_datapoints_binding_ids(self):
        return []









