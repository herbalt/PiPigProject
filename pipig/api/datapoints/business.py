from pipig.data_points.models import DataPoints, DataPoint


def create_datapoints(data):
    name = data.get('name')
    datapoints = DataPoints.create(name=name)
    return datapoints


def create_datapoint(datapoints_id, data):
    value = data.get('value')
    time_elapsed = data.get('time_elapsed')

    datapoint = DataPoint.create(data_points_id=datapoints_id, value=value, time_elapsed=time_elapsed)
    return datapoint

def update_datapoint(datapoints_id, data):
    datapoint_id = data.get('id')
    value = data.get('value')
    time_elapsed = data.get('time_elapsed')
    datapoint = DataPoint.get(datapoint_id)
    datapoint.update(datapoint_id, datapoints_id=datapoints_id, value=value, time_elapsed=time_elapsed)
    return DataPoint.get(datapoint_id)