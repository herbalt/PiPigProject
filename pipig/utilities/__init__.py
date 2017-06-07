def average_readings(list_to_average):
    """
    Calculate average reading of list
    :param list_to_average: list of floats
    :returns average result
    """
    sum_of_list = 0.0
    count_of_list = 0

    for reading_index in range(0, len(list_to_average)):
        if list_to_average[reading_index] is not None:
            sum_of_list += list_to_average[reading_index]
        count_of_list += 1

    if count_of_list == 0:
        return sum_of_list

    average_of_list = sum_of_list / count_of_list
    return average_of_list


def calculate_quantity_of_readings(timeframe_in_seconds, interval_between_readings):
    """
    Use to convert a seconds reading into the number of sensor readings that would occur
    :param timeframe_in_seconds:
    :param interval_between_readings:
    :return: An integer of the number of readings
    """
    if interval_between_readings == 0:
        return 1
    return int(round(timeframe_in_seconds / interval_between_readings, 0))


def debug_messenger(message):
    from pipig.app_config import config_class
    if config_class.DEBUG == True:
        print str(message)