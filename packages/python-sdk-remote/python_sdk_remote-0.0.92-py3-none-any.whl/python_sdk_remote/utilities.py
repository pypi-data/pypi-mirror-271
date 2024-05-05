import os
from datetime import date, datetime, time, timedelta
from dotenv import load_dotenv
from url_remote.environment_name_enum import EnvironmentName
from urllib.parse import urlparse

from .http_response import (create_authorization_http_headers, get_user_jwt_from_event,  # noqa - used for backwards compatibility
                            create_return_http_headers, create_error_http_response, create_ok_http_response,
                            create_http_body)
from .mini_logger import MiniLogger as logger

load_dotenv()


def timedelta_to_time_format(time_delta: timedelta) -> str:
    """
    Convert a timedelta to a time format in HH:MM:SS.

    Parameters:
        time_delta (datetime.timedelta): The timedelta to be converted.

    Returns:
        str: A string in HH:MM:SS format representing the time duration.

    Example:
        Usage of timedelta_to_time_format:

        >>> from datetime import timedelta
        >>> duration = timedelta(hours=2, minutes=30, seconds=45)
        >>> formatted_time = timedelta_to_time_format(duration)
        >>> print(formatted_time)
        "02:30:45"
    """
    TIMEDELTA_TO_TIME_FORMAT_METHOD_NAME = "timedelta_to_time_format"
    logger.start(TIMEDELTA_TO_TIME_FORMAT_METHOD_NAME, object={'time_delta': time_delta})

    # Calculate the total seconds and convert to HH:MM:SS format
    total_seconds = int(time_delta.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # Format as "HH:MM:SS"
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    logger.end(TIMEDELTA_TO_TIME_FORMAT_METHOD_NAME,
               object={'formatted_time': formatted_time})
    return formatted_time


def is_valid_time_range(time_range: tuple) -> bool:
    """
    Validate that the time range is in the format 'HH:MM:SS'.
    """
    logger.start(object={"time_range": time_range.__str__()})
    if len(time_range) != 2:
        logger.end(object={"is_valid_time_range_result": False, "reason": "len(time_range) != 2"})
        return False

    for time_obj in time_range:
        if not isinstance(time_obj, time):
            logger.end(object={
                "is_valid_time_range_result": False, "reason": "time_range contains non-time objects"})
            return False
        time_str = time_obj.strftime('%H:%M:%S')
        if time_obj.strftime('%H:%M:%S') != time_str:
            logger.end(object={
                "is_valid_time_range_result": False, "reason": "time_range contains invalid time format"})
            return False

    logger.end(object={"is_valid_time_range_result": True})
    return True


# TODO shall we also use Url type and not only str? - Strongly Type which I prefer
#   (if yes we should change it also in all the calls to this function)
def validate_url(url: str):
    logger.start(object={"url": url})
    if url is not None or url != "":
        parsed_url = urlparse(url)
        is_valid_url = parsed_url.scheme and parsed_url.netloc
    else:
        is_valid_url = True
    logger.end(object={"is_valid_url": is_valid_url})
    return is_valid_url


def is_valid_date_range(date_range: tuple) -> bool:
    """
    Validate that the date range is in the format 'YYYY-MM-DD'.
    """
    logger.start(object={"date_range": date_range.__str__()})
    if len(date_range) != 2:
        logger.end(object={"is_valid_date_range_result": False, "reason": "len(date_range) != 2"})
        return False

    for date_obj in date_range:
        if not isinstance(date_obj, date):
            logger.end(object={
                "is_valid_date_range_result": False, "reason": "date_range contains non-date objects"})
            return False
    logger.end(object={"is_valid_date_range_result": True})
    return True


def is_valid_datetime_range(datetime_range: tuple) -> bool:
    """
    Validate that the datetime range is in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    logger.start(object={"datetime_range": datetime_range.__str__()})
    if len(datetime_range) != 2:
        logger.end(object={"is_valid_datetime_range_result": False, "reason": "len(datetime_range) != 2"})
        return False

    for datetime_obj in datetime_range:
        if not isinstance(datetime_obj, datetime):
            logger.end(object={"is_valid_datetime_range_result": False, "reason": "datetime_range contains non-datetime objects"})
            return False
    logger.end(object={"is_valid_datetime_range_result": True})
    return True


def is_list_of_dicts(obj: object) -> bool:
    """
    Check if an object is a list of dictionaries.

    Parameters:
        obj (object): The object to be checked.

    Returns:
        bool: True if the object is a list of dictionaries, False otherwise.

    Example:
        Usage of is_list_of_dicts:

        >>> is_list_of_dicts([{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}])
        True

        >>> is_list_of_dicts([1, 2, 3])
        False

        >>> is_list_of_dicts(1)
        False
    """
    logger.start(object={"obj": obj})
    try:
        if not isinstance(obj, list):
            is_list_of_dicts_result = False
            logger.end(object={"is_list_of_dicts_result": is_list_of_dicts_result})
            return is_list_of_dicts_result
        for item in obj:
            if not isinstance(item, dict):
                is_list_of_dicts_result = False
                logger.end(object={
                    "is_list_of_dicts_result": is_list_of_dicts_result})
                return is_list_of_dicts_result
        is_list_of_dicts_result = True
        logger.end(object={
            "is_list_of_dicts_result": is_list_of_dicts_result})
        return is_list_of_dicts_result
    except Exception as exception:
        logger.exception(object=exception)
        logger.end()
        raise


def is_time_in_time_range(check_time: time, time_range: tuple) -> bool:
    """
    Check if the given time is within the specified time range.

    Parameters:
        check_time (str): The time to check in 'HH:MM:SS' format.
        time_range (tuple): A tuple containing start and end times in 'HH:MM:SS' format.

    Returns:
        bool: True if the check_time is within the time range, False otherwise.
    """
    logger.start(object={
        "check_time": check_time.__str__(), "time_range": time_range.__str__()})
    if not is_valid_time_range(time_range) or not isinstance(check_time, time):
        logger.end(object={
            "is_time_in_time_range_result": False})
        return False
    start_time, end_time = time_range
    logger.end(object={
        "is_time_in_time_range_result": start_time <= check_time <= end_time})
    return start_time <= check_time <= end_time


def is_date_in_date_range(check_date: date, date_range: tuple) -> bool:
    """
    Check if the given date is within the specified date range.

    Parameters:
        check_date (str): The date to check in 'YYYY-MM-DD' format.
        date_range (tuple): A tuple containing start and end dates in 'YYYY-MM-DD' format.

    Returns:
        bool: True if the check_date is within the date range, False otherwise.
    """
    logger.start(object={
        "check_date": check_date.__str__(), "date_range": date_range.__str__()})
    if not is_valid_date_range(date_range) or not isinstance(check_date, date):
        logger.end(object={
            "is_date_in_date_range_result": False})
        return False

    start_date, end_date = date_range
    logger.end(object={
        "is_date_in_date_range_result": start_date <= check_date <= end_date})
    return start_date <= check_date <= end_date


def is_datetime_in_datetime_range(check_datetime: datetime, datetime_range: tuple) -> bool:
    """
    Check if the given datetime is within the specified datetime range.

    Parameters:
        check_datetime (str): The datetime to check in 'YYYY-MM-DD HH:MM:SS' format.
        datetime_range (tuple): A tuple containing start and end datetimes in 'YYYY-MM-DD HH:MM:SS' format.

    Returns:
        bool: True if the check_datetime is within the datetime range, False otherwise.
    """
    logger.start()
    if not is_valid_datetime_range(datetime_range) or not isinstance(check_datetime, datetime):
        logger.end(object={
            "is_valid_datetime_range": False})
        return False

    start_datetime, end_datetime = datetime_range
    is_datetime_in_datetime_range_result = start_datetime <= check_datetime <= end_datetime
    logger.end(object={
        "is_datetime_in_datetime_range_result": is_datetime_in_datetime_range_result})
    return is_datetime_in_datetime_range_result


def get_brand_name() -> str:
    return our_get_env("BRAND_NAME")


def get_environment_name() -> str:
    environment_name = our_get_env("ENVIRONMENT_NAME")
    EnvironmentName(environment_name)  # if invalid, raises ValueError: x is not a valid EnvironmentName
    return environment_name


def our_get_env(key: str, default: str = None, raise_if_not_found: bool = True) -> str:
    logger.start(object={"key": key, "default": default, "raise_if_not_found": raise_if_not_found})
    env_var = os.getenv(key, default)
    if raise_if_not_found and env_var is None:
        raise Exception(f"Environment variable {key} not found")
    logger.end(object={"env_var": env_var})
    return env_var


def get_sql_hostname() -> str:
    return our_get_env("RDS_HOSTNAME")


def get_sql_username() -> str:
    return our_get_env("RDS_USERNAME")


def get_sql_password() -> str:
    return our_get_env("RDS_PASSWORD")


def remove_digits(text: str) -> str:
    return ''.join([i for i in text if not i.isdigit()])
