from binding_session.models import BindSessionsSensors, BindSessionAppliances
from pipig import app


class SessionSensorBinder:
    def __init__(self, session_sensor_id):
        self.session_sensor_id = session_sensor_id

    def obj_session_sensor(self):
        with app.app_context():
            obj = BindSessionsSensors.query.filter_by(id=self.session_sensor_id).first()
        return obj

    def get_id(self):
        return self.obj_session_sensor().get_id()

    def get_session_id(self):
        return self.obj_session_sensor().get_session_id()

    def get_sensor_id(self):
        return self.obj_session_sensor().get_sensor_id()




class SessionApplianceBinder():
    def __init__(self, session_appliance_id):
        self.session_appliance_id = session_appliance_id

    def obj_session_sensor(self):
        with app.app_context():
            obj = BindSessionAppliances.query.filter_by(id=self.session_appliance_id).first()
        return obj

    def get_id(self):
        return self.obj_session_sensor().get_id()

    def get_session_id(self):
        return self.obj_session_sensor().get_session_id()

    def get_appliance_id(self):
        return self.obj_session_sensor().get_appliance_id()