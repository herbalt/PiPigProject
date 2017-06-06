from test_helpers.test_base import BaseTestCase

from pipig.data_points.models import DataPoint, DataPoints

#________________________________________________________________
#
# Test Helpers
#________________________________________________________________

def compare_data_point(first, second):
    if first is None or second is None:
        return False
    data_points_id = first.data_points_id == second.data_points_id
    value = first.value == second.value
    time_elapsed = first.time_elapsed == second.time_elapsed
    return data_points_id and value and time_elapsed
#________________________________________________________________
#
# Unit Tests
#________________________________________________________________


class DataPointsObjectTestsDataPoint(BaseTestCase):

    def test_get_data_points_id(self):
        """

        :return: ID of the Data Point set this point is connected to
        """
        data_point = DataPoint(1, 2, 3.0)
        result = data_point.get_data_points_id()
        expected = 1
        self.assertTrue(result == expected, "DataPointID should be %d, but is %d" % (result, expected))

    def test_get_value(self):
        """

        :return: The value of the Data Point
        """
        data_point = DataPoint(1, 2, 3.0)
        result = data_point.get_value()
        expected = 2
        self.assertTrue(result == expected, "DataPoint Value should be %d, but is %d" % (result, expected))

    def test_get_time_elapsed(self):
        """

        :return: The time elapsed value of the Data Point
        """
        data_point = DataPoint(1, 2, 3.0)
        result = data_point.get_time_elapsed()
        expected = 3.0
        self.assertTrue(result == expected, "DataPoint Time Elapsed should be %d, but is %d" % (result, expected))

    def test_get_data_point_tuple(self):
        """

        :return: Tuple: (DataPointsId, Value, TimeElapsed)
        """
        data_point = DataPoint(1, 2, 3.0)
        result = data_point.get_data_point_tuple()
        expected = (1, 2, 3.0)
        self.assertTrue(result == expected, "DataPoint Time Elapsed should be %s, but is %s" % (str(result), str(expected)))


class DataPointsObjectTests(BaseTestCase):
    def test_get_data_point_list_no_sorting_needed(self):
        data_points = DataPoints("test_get_data_point_list_no_sorting_needed")
        expected = self.populate_with_mock_data_points_no_sort_required()
        self.helper_test_get_data_point_list(data_points, expected)

    def test_get_data_point_list_is_sorted(self):
        data_points = DataPoints("test_get_data_point_list_is_sorted")
        expected = self.populate_with_mock_data_points()
        self.helper_test_get_data_point_list(data_points, expected)

    def test_update_point_new(self):
        data_points = DataPoints(name="test_update_point_new")
        data_points.id = 1
        data_point = data_points.update_point(datapoint_id=None, value=1, time_elapsed=100)

        expected_data_point = DataPoint(data_points_id=1, value=1, time_elapsed=100)

        self.assertTrue(compare_data_point(data_point, expected_data_point),
                        "Failed adding a new Data Point to %s" % data_points.name)

    def test_update_point_existing(self):
        data_points = DataPoints(name="TestDataPoints")
        data_points.id = 1
        existing_data_point = data_points.update_point(datapoint_id=None, value=1, time_elapsed=100)
        expected_data_point = DataPoint(data_points_id=1, value=2, time_elapsed=50)

        data_point = data_points.update_point(datapoint_id=1, value=2, time_elapsed=50)

        self.assertTrue(compare_data_point(data_point, expected_data_point),
                        "Failed adding a new Data Point to %s" % data_points.name)

    def test_delete_point(self):
        data_points = DataPoints.create(name="test_delete_point")

        data_point = DataPoint.create(data_points_id=1, value=0, time_elapsed=0)

        prep_list = data_points.get_point_by_id(id=1)
        self.assertIsNotNone(prep_list, "%s has an error in the setup for the test" % (data_points.name))

        data_points.delete_point(data_point_id=data_point.get_id())
        result = data_points.get_point_by_id(id=data_point.get_id())
        self.assertIsNone(result, "%s should have no Points" % (data_points.name))

    def test_delete_all_data_points(self):
        data_points = DataPoints.create(name="test_delete_all_data_points")
        self.populate_with_mock_data_points()

        prep_list = data_points.get_points()
        self.assertTrue(len(prep_list) > 0, "%s has an error in the setup for the test" % (data_points.name))

        data_points.delete_all_data_points()
        result = data_points.get_points()
        expected = []

        self.assertListEqual(result, expected, "%s should produce an empty list" % (data_points.name))

    def test_get_data_point_by_id(self):
        data_points = DataPoints("test_get_data_point_by_id")
        self.populate_with_mock_data_points()

        self.helper_test_get_data_point_by_id(1, DataPoint(1, 0, 0), data_points)
        self.helper_test_get_data_point_by_id(4, DataPoint(1, 200, 40), data_points)
        self.helper_test_get_data_point_by_id(5, DataPoint(1, 150, 30), data_points)

    def test_get_data_point_time_does_not_exist(self):
        data_points = DataPoints(name="test_get_data_point_time_does_not_exist")
        data_points.id = 1
        self.populate_with_mock_data_points()
        self.helper_test_get_data_point(5, DataPoint(1, 25, 5), data_points)

    def test_get_data_point_time_after_last_point(self):
        data_points = DataPoints(name="test_get_data_point_time_after_last_point")
        data_points.id = 1
        self.populate_with_mock_data_points()
        self.helper_test_get_data_point(50, DataPoint(1, 200, 50), data_points)

    def test_get_data_point_time_exists(self):
        data_points = DataPoints("test_get_data_point_time_exists")
        self.populate_with_mock_data_points()

        self.helper_test_get_data_point(0, DataPoint(1, 0, 0), data_points)
        self.helper_test_get_data_point(40, DataPoint(1, 200, 40), data_points)
        self.helper_test_get_data_point(30, DataPoint(1, 150, 30), data_points)

    def populate_with_mock_data_points_no_sort_required(self):
        list_of_data_points = []
        list_of_data_points.append(DataPoint.create(data_points_id=1, value=0, time_elapsed=0))
        list_of_data_points.append(DataPoint.create(data_points_id=1, value=50, time_elapsed=10))
        list_of_data_points.append(DataPoint.create(data_points_id=1, value=100, time_elapsed=20))

        list_of_data_points.sort(key=lambda data_point: data_point.get_time_elapsed())
        return list_of_data_points

    def populate_with_mock_data_points(self):
        list_of_data_points = []
        list_of_data_points.append(DataPoint.create(data_points_id=1, value=0, time_elapsed=0))
        list_of_data_points.append(DataPoint.create(data_points_id=1, value=50, time_elapsed=10))
        list_of_data_points.append(DataPoint.create(data_points_id=1, value=100, time_elapsed=20))
        list_of_data_points.append(DataPoint.create(data_points_id=1, value=200, time_elapsed=40))
        list_of_data_points.append(DataPoint.create(data_points_id=1, value=150, time_elapsed=30))

        list_of_data_points.sort(key=lambda data_point: data_point.get_time_elapsed())
        return list_of_data_points

    def helper_test_get_data_point(self, time_elapsed, expected, data_points):
        result = data_points.get_point(time_elapsed=time_elapsed)
        self.assertTrue(compare_data_point(expected, result),
                        "%s should produce a result of: %s, for time_elapsed %d, but is %s " % (
                        data_points.name, str(expected), time_elapsed, str(result)))

    def helper_test_get_data_point_by_id(self, id, expected, data_points):
        result = data_points.get_point_by_id(id=id)
        self.assertTrue(compare_data_point(expected, result),
                        "%s should produce a result of: %s, for id %d, but is %s " % (
                        data_points.name, str(expected), id, str(result)))

    def helper_test_get_data_point_list(self, data_points, expected):
        result = data_points.get_points()

        for index in range(1, len(result)):
            self.assertTrue(compare_data_point(expected[index], result[index]),
                            "%s result should be: %s, however is %s"
                            % (data_points.name, str(expected[index]), str(result[index])))



#________________________________________________________________
#
# Test Objects
#________________________________________________________________
def build_datapoints_model(base_name, list_of_points_as_tuples):
    datapoints = DataPoints.create(name=base_name)

    for point in list_of_points_as_tuples:
        datapoints.update_point(None, point[0], point[1])
    return datapoints