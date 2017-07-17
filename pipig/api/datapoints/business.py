from pipig.data_points.models import DataPoints, DataPoint


def create_datapoints(data):
    name = data.get('name')
    datapoints = DataPoints.create(name=name)
    return datapoints

def update_datapoints(datapoints_id, data):
    """
    Warning, this function will over-write existing Datapoints points.
    :param datapoints_id:
    :param data:
    :return:
    """

    model_datapoints = DataPoints.get(datapoints_id)
    model_original_points = model_datapoints.get_points()
    model_datapoints.delete_all_data_points()

    for point_in_json in data['list of points']:
        jspt_id = point_in_json['id']
        if jspt_id == 0:
            jspt_id= None
        jspt_time = point_in_json['time elapsed']
        jspt_value = point_in_json['value']
        try:
            model_datapoints.update_point(datapoint_id=jspt_id, value=jspt_value, time_elapsed=jspt_time)
        except AttributeError:
            for point in model_original_points:
                model_datapoints.update_point(datapoint_id=point.get_id(), value=point.get_value(), time_elapsed=point.get_time_elapsed())
            return DataPoints.get(datapoints_id).get_json(), 400
    return DataPoints.get(datapoints_id).get_json(), 201


"""
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
"""