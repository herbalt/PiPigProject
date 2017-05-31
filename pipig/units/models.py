from data import CRUDMixin
from pipig import db


class GenericUnits(db.Model, CRUDMixin):
    """
    Determines the Units of measures
    Example Celcius, Humidty, TestInteger
    """
    __tablename__ = "units"
    id = db.Column(db.Integer, primary_key= True, nullable=False)
    code_name = db.Column(db.String, nullable=False)
    display_units = db.Column(db.String(4), nullable=True)

    # TODO WHY IS TYPE HERE ?
    # type = db.Column(db.String(140))

    def __init__(self, code_name, display_units):
        self.code_name = code_name
        self.display_units = display_units


    def get_id(self):
        return self.id


    def get_code_name(self):
        return self.code_name


    def get_display_units(self):
        return self.display_units