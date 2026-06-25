"""
https://towardsdatascience.com/level-up-your-code-with-python-decorators-c1966d78607
"""
import functools
import logging
import logging.config

from src._tools.filereader import get_data_file_from_package


def create_logger(package_name: str, yaml_package_path: str):
    """
    yaml_file = resource_filename("_config", f"logging.yaml")

    :param package_name:
    :param yaml_package_path:
    :return:
    """
    yaml_config_path = get_data_file_from_package(package_name, yaml_package_path)
    logging.config.dictConfig(yaml_config_path)
    
    return logging.getLogger('root')


def log_decorator(_logger):
    """

    :param _logger:
    :return:
    """
    def log_this(_function):
        @functools.wraps(_function)
        def wrapper_decorator(*args, **kwargs):
            _logger.debug(f"{_function.__name__} - {args} - {kwargs}")
            function_output = _function(*args, **kwargs)
            _logger.debug(f"{_function.__name__} returned: {function_output}")
            return function_output

        return wrapper_decorator

    return log_this


