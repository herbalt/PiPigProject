from appliances.factory import FactoryAppliance
from processors.processors import build_processor_chain
from sensors.factory import FactorySensor
from sessions.models import Session
from sensors.sensor import BaseSensor
from appliances.appliance import BaseAppliance
from data_points.models import DataPoints

from binding_session.models import BindSessionsSensors, BindSessionAppliances
from binding_session.session_binding import SessionSensorBinder, SessionApplianceBinder

from bindings_datapoints.models import BindDataPointsSensors, BindDataPointsAppliances
from bindings_datapoints.datapoint_binding import DataPointsSensorBinder, DataPointsApplianceBinder

def build_and_bind_objects_from_session(session_id):
    session = Session.get(session_id)

    binder_session_sensor_list = []
    binder_session_appliance_list = []

    binder_datapoints_sensor_list = []
    binder_datapoints_appliance_list = []

    sensor_list = []
    appliance_list = []
    datapoints_list = []

    # Build Session Binders
    session_sensors_models = BindSessionsSensors.query.filter_by(session_id=session_id).all()
    session_appliances_models = BindSessionAppliances.query.filter_by(session_id=session_id).all()

    for model in session_sensors_models:
        binder_session_sensor_list.append(SessionSensorBinder(model.get_id()))

    for model in session_appliances_models:
        binder_session_appliance_list.append(SessionApplianceBinder(model.get_id()))


    # Build Datapoint Binders
    datapoints_sensors_models = BindDataPointsSensors.query.filter_by(session_id=session_id).all()
    datapoints_appliance_models = BindDataPointsAppliances.query.filter_by(session_id=session_id).all()

    for model in datapoints_sensors_models:
        binder_datapoints_sensor_list.append(DataPointsSensorBinder(model.get_id()))

    for model in datapoints_appliance_models:
        binder_datapoints_appliance_list.append(DataPointsApplianceBinder(model.get_id()))

    # Build Base Objects

    sensor_factory = FactorySensor()
    for sensor_obj in binder_session_sensor_list:
        sensor = sensor_factory.build_object(sensor_obj.get_sensor_id())

        # ADD PROCESSORS
        processor = build_processor_chain(average=True)
        # TODO Replace the hard coded 10 with a variable to select the delay time for the processor
        processor.update_delay_quantity_by_time(10, sensor.get_interval_between_readings())
        sensor.attach(processor)

        sensor_list.append(sensor)

    appliance_factory = FactoryAppliance()
    for appliance_obj in binder_session_appliance_list:
        appliance = appliance_factory.build_object(appliance_obj.get_appliance_id())

        # ADD PROCESSORS
        processor = build_processor_chain(delay_quantity=1, average=False)
        appliance.attach(processor)

        appliance_list.append(appliance)

    for bind_db_sensor_obj in binder_datapoints_sensor_list:
        # obj = DataPoints.query.filter_by(datapoints_id=datapoints_obj.get_datapoints_id()).first()
        # BUILD MATRIX OF SENSORS AND DATAPOINTS

        # datapoints_list.append(obj)
        for bind_db_appliance_obj in binder_datapoints_appliance_list:
            if bind_db_sensor_obj.get_datapoints_id() == bind_db_appliance_obj.get_datapoints_id():
                bind_db_sensor_obj.attach(bind_db_appliance_obj)
                for app_obj in appliance_list:
                    if app_obj.get_id() == bind_db_appliance_obj.get_appliance_id():
                        bind_db_appliance_obj.attach(app_obj)


