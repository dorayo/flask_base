from functools import wraps
import math


def args_str2int(arg: str, default=None) -> int:
    """
    Converts a string argument to an integer with error handling.

    Args:
        arg: The string argument to convert.
        default: The default value to return if conversion fails.

    Returns:
        The converted integer or the default value.
    """
    try:
        return int(arg) if arg is not None else default
    except ValueError:
        return default

def args_split2list(arg: str) -> list:
    """
    Splits a comma-separated string into a list of strings.

    Args:
        arg: The comma-separated string.

    Returns:
        A list of strings.
    """
    return arg.split(',') if arg else []

def value_to_float(value) -> float:
    """
    Converts a value to a float and rounds it to two decimal places.

    Args:
        value: The value to convert.

    Returns:
        The rounded float.
    """
    return round(float(value), 2) if value is not None else 0.0

def get_model_page_data(models, page: int, page_count: int):
    """
    Paginates data models.

    Args:
        models: The query object of the data models.
        page: Current page number.
        page_count: Number of items per page.

    Returns:
        A tuple containing the list of items and total pages.
    """
    model_page = models.paginate(page=page, per_page=page_count, error_out=False)
    return model_page.items, model_page.pages

def get_page_data_list(datas: list, page: int, page_count: int):
    """
    Paginates a list of data.

    Args:
        datas: List of data items.
        page: Current page number.
        page_count: Number of items per page.

    Returns:
        A tuple of the sliced data list and total pages.
    """
    total_page = math.ceil(len(datas) / page_count)
    start = (page - 1) * page_count
    end = min(start + page_count, len(datas))
    return datas[start:end], total_page

def model_to_dict(model) -> dict:
    """
    Converts a SQLAlchemy model into a dictionary while removing internal state attributes.

    Args:
        model: The SQLAlchemy model instance.

    Returns:
        A dictionary representation of the model.
    """
    return {key: value for key, value in model.__dict__.items() if key != '_sa_instance_state'}

def dict_assignment_to_model(data_dict: dict, model) -> object:
    """
    Assigns dictionary values to model attributes if they exist in the model.

    Args:
        data_dict: A dictionary of data to assign.
        model: The model object to which data will be assigned.

    Returns:
        The model with updated attributes.
    """
    for key, value in data_dict.items():
        if hasattr(model, key) and value is not None:
            setattr(model, key, value)
    return model