from test_helpers.test_generics import run_equals_test, unwritten_test
from test_helpers.test_base import BaseTestCase

from utilities import average_readings, calculate_quantity_of_readings


class UtilityTests(BaseTestCase):
    def test_average_readings(self):
        """
        Calculate average reading of list
        :params list_to_average
        :returns average result
        """
        list_to_test = [1.0, 2.0, 3.0, 4.0, 5.0]
        result = average_readings(list_to_test)
        expected = 3.0
        run_equals_test( self, result, expected, "Average Readings", "Float readings" )

        list_to_test = [1.0, 2.0, 3.0, 4.0]
        result = average_readings(list_to_test)
        expected = 2.5
        run_equals_test( self, result, expected, "Average Readings", "Float readings return decimal" )

        list_to_test = [1, 2, 3, 4]
        result = average_readings(list_to_test)
        expected = 2.5
        run_equals_test( self, result, expected, "Average Readings", "Interger readings return decimal" )

    def helper_calculate_quantity_of_readings(self, timeframe, interval, expected):
        message = '%d should be the result when timeframe is %d and interval is %d' % (expected, timeframe, interval)
        self.assertTrue(calculate_quantity_of_readings(timeframe, interval) == expected, message)

    def test_calculate_quantity_of_readings(self):
        """
        # return int(round(timeframe_in_seconds / interval_between_readings, 0))
        :return:
        """
        self.helper_calculate_quantity_of_readings(10, 5, 2)
        self.helper_calculate_quantity_of_readings(10, 3, 3)
        self.helper_calculate_quantity_of_readings(10, 6, 1)

