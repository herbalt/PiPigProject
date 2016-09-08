def unwritten_test(test_case):
    """

    :param test_case: Unit Test Class
    :return:
    """
    test_case.fail("Test has not been written")


def run_equals_test(test_case, result, expected, test_title, test_message):
    """

    :param test_case: Unit Test Class
    :param result:
    :param expected:
    :param test_title:
    :param test_message:
    :return:
    """
    test_case.assertEquals(result, expected, test_title + "\n" + test_message + "\nResult:\n" + str(result) + "\nExpected:\n" + str(expected) + "\n")