import yaml


def yaml_coerce(value):
    """
    This function is used to convert a dictionary string literal to a dictionary object.
    :param value:
    :return:
    """
    if isinstance(value, str):
        return yaml.load(f'dummy: {value}', Loader=yaml.SafeLoader)['dummy']

    return value
