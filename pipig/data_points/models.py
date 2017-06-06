
from pipig.data import db, CRUDMixin
from pipig import app

class DataPoint(db.Model, CRUDMixin):
    """
    A single Data Point for a DataPoints object
    """
    __tablename__ = "data_point_binding"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data_points_id = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float)
    time_elapsed = db.Column(db.Float)

    def __init__(self, data_points_id, value, time_elapsed):
        self.data_points_id = data_points_id
        self.value = value
        self.time_elapsed = time_elapsed

    def __str__(self):
        return "DataPointsID: %d, Value: %f, TimeElapsed: %f" % (self.data_points_id, self.value, self.time_elapsed)

    def get_id(self):
        return self.id

    def get_data_points_id(self):
        """

        :return: ID of the Data Point set this point is connected to
        """
        return self.data_points_id

    def get_value(self):
        """

        :return: The value of the Data Point
        """
        return self.value

    def get_time_elapsed(self):
        """

        :return: The time elapsed value of the Data Point
        """
        return self.time_elapsed

    def get_data_point_tuple(self):
        """

        :return: Tuple: (DataPointsId, Value, TimeElapsed)
        """
        return self.get_data_points_id(), self.get_value(), self.get_time_elapsed()

    def set_value(self, value=None):
        if value is not None:
            self.update(value=value)
        return self.get_value()

    def set_time_elapsed(self, time_elapsed=None):
        if time_elapsed is not None:
            self.update(time_elapsed=time_elapsed)
        return self.get_time_elapsed()


class DataPoints(db.Model, CRUDMixin):
    """
    A series of Data Point objects that will be used to trigger appliances based on sensor inputs
    """
    __tablename__ = "data_points"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)

    def __init__(self, name):
        self.name = name

    def get_id(self):
        return self.id

    def get_type_id(self):
        return 0

    def get_points(self):
        """
        Query the Data Point Binding to get all the related Data Point IDs
        Query the Data Point to get the objects from the Data Point IDs
        This should be an ordered list based on time elapsed values
        :return: List of DataPoints
        """
        data_point_id_list = DataPoint.query.filter_by(data_points_id=self.id).order_by(DataPoint.time_elapsed).all()
        return data_point_id_list

    def process_data_point_list_to_single_point(self, list_of_data_point_objects=None):
        """
        Takes a list of Data Point Objects and averages the values,
        then creates a new DataPoint with:
            latest timestamp, the new value, and the original data_points_id
        :return: Data Point Object
        """
        if list_of_data_point_objects is None or list_of_data_point_objects == []:
            return None

        value_sum = 0

        for data_point in list_of_data_point_objects:
            value_sum += data_point.value

        last_point = list_of_data_point_objects[-1]

        try:
            average_value = value_sum / len(list_of_data_point_objects)
            return DataPoint(last_point.data_points_id, average_value, last_point.time_elapsed)
        except ZeroDivisionError:
            return None


    def get_point(self, time_elapsed):
        """
        Returns the Data Point corresponding to a given time.
        If no Data Point at a given time, then retrieve points either side of time and average the readings
        :param datapoints_id: Database ID for the Data Point at a given time.
        :return: Data Point Object
        """

        # Processes DataPoints if multiple readings at time_elapsed
        # with app.app_context():
        initial_query = DataPoint.query.filter_by(time_elapsed=time_elapsed).all()
        if initial_query is not None:
            initial_result = self.process_data_point_list_to_single_point(initial_query)
            if initial_result is not None:
                return initial_result

        # Get the list of points associated with the DataPoints Object
        all_points = self.get_points()
        if len(all_points) == 0:
            return None

        # These two variables track the current closet time values to the time_elapsed variable
        low_data_point = None
        high_data_point = None

        # Loop through the data points list to assess each against the tracking variables
        for index in range(0, len(all_points)):
            # Populate the low variable if currently not set and has a elapsed value less than the input
            if low_data_point is None and all_points[index].get_time_elapsed() <= time_elapsed:
                    low_data_point = all_points[index]

            # Populate the high variable if currently not set and has a elapsed value greater than the input
            if high_data_point is None and all_points[index].get_time_elapsed() >= time_elapsed:
                    high_data_point = all_points[index]

            # Populate the low variable if has a elapsed value less than the input and greater than the current low variable
            if all_points[index].get_time_elapsed() <= time_elapsed and all_points[index].get_time_elapsed() > low_data_point.get_time_elapsed():
                    low_data_point = all_points[index]

            # Populate the high variable if has a elapsed value less than the input and less than the current low variable
            if all_points[index].get_time_elapsed() >= time_elapsed and all_points[index].get_time_elapsed() < high_data_point.get_time_elapsed():
                    high_data_point = all_points[index]

        # Attempt to process all values at the low variable's elapsed
        try:
            low_data_point = self.get_point(low_data_point.get_time_elapsed())
        except AttributeError:
            # If time_elapsed input is before any DataPoint
            first_data_point = all_points[0]
            first_data_point.time_elapsed = time_elapsed
            return first_data_point

        # Attempt to process all values at the high variable's elapsed
        try:
            high_data_point = self.get_point(high_data_point.get_time_elapsed())
        except AttributeError:
            # If time_elapsed input is after any DataPoint
            last_data_point = all_points[-1]
            last_data_point.time_elapsed = time_elapsed
            return last_data_point

        # Average the low and high variable values and set with the time_elapsed input
        processed_data_point = self.process_data_point_list_to_single_point([low_data_point, high_data_point])
        processed_data_point.time_elapsed = time_elapsed
        return processed_data_point

    def get_point_by_id(self, id):
        """
        Returns the Data Point corresponding to the Database ID
        :param id: The Data Point ID from the Database
        :return: Data Point Object
        """
        return DataPoint.query.filter_by(id=id).first()


    def update_point(self, datapoint_id=None, value=None, time_elapsed=None):
        """
        Updates or Adds a Data Point

        :param datapoint_id: Data Point to Edit. If None, then adding a new Data Point
        :param value: Value to write to the Data Point
        :param time_elapsed: Time Elapsed value to write to the Data Point
        :return: Data Point Object
        """
        if datapoint_id is None:
            # Use DataPointID = None to add a new data point
            if value is None or time_elapsed is None:
                return None

            data_point = DataPoint.create(data_points_id=self.id, value=value, time_elapsed=time_elapsed)
            # db.session.commit()
        else:
            # with app.app_context():
            # data_point = DataPoint.query.filter_by(id=datapoint_id).first()
            data_point = DataPoint.get(id=datapoint_id)
            data_point.set_value(value)
            data_point.set_time_elapsed(time_elapsed)
            # if value is not None:
            #     data_point.value = value

            # if time_elapsed is not None:
            #    data_point.time_elapsed = time_elapsed

            # db.session.commit()

        return data_point

    def delete_point(self, data_point_id=None):
        """
        Deletes a Data Point from the database

        :param data_point_id: The ID
        :return: Boolean based on the success of the Delete action
        """
        if data_point_id is not None:
            # with app.app_context():
            data_point = DataPoint.query.filter_by(id=data_point_id).first()
            db.session.delete(data_point)
            db.session.commit()
            return True
        return False

    def delete_all_data_points(self):
        """
        Deletes all Data Points corresponding to the Data Points Object
        :return: Boolean based on the success of the Delete points action
        """
        all_points = self.get_points()
        for data_point in all_points:
            self.delete_point(data_point.get_id())
        return True


