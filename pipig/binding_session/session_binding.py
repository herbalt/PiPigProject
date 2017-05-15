from binding_session.models import BindSessionsSensors, BindSessionAppliances
from pipig import app
from abc import abstractmethod, ABCMeta


class SessionBinder:
    "Base Class to retrieve objects that are bound to a session"
    __metaclass__ = ABCMeta

    def __init__(self, session_binder_id):
        self.session_binder_id = session_binder_id

    @abstractmethod
    def get_object(self):
        pass

    def get_id(self):
        return self.get_object().get_id()

    def get_session_id(self):
        return self.get_object().get_session_id()


class SessionSensorBinder(SessionBinder):
    objBindSessionsSensors = None

    def __init__(self, session_binder_id):
        SessionBinder.__init__(self, session_binder_id)

    def get_object(self):
        if self.objBindSessionsSensors is None:
            with app.app_context():
                # obj = BindSessionsSensors.query.filter_by(id=self.session_binder_id).first()
                obj = BindSessionsSensors.get(self.session_binder_id)
            return obj
        return self.objBindSessionsSensors

    def get_sensor_id(self):
        return self.get_object().get_sensor_id()


class SessionApplianceBinder(SessionBinder):
    objBindSessionAppliances = None

    def __init__(self, session_binder_id):
        SessionBinder.__init__(self, session_binder_id)

    def get_object(self):
        if self.objBindSessionAppliances is None:
            with app.app_context():
                # obj = BindSessionAppliances.query.filter_by(id=self.session_binder_id).first()
                obj = BindSessionAppliances.get(self.session_binder_id)
            return obj
        return self.objBindSessionAppliances

    def get_appliance_id(self):
        return self.get_object().get_appliance_id()