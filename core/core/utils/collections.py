def update_vals(base, update_with):
    """
    This function is used to update the settings module of the Django app, if any environment variables are provided.
    This is a helpers function and is used to deal with any environment values.
    :param base:
    :param update_with:
    :return:
    """
    for key, value in update_with.items():
        if isinstance(value, dict):
            base_value = base.get(key)

            if isinstance(base_value, dict):
                update_vals(base_value, value)
            else:
                base[key] = value
        else:
            base[key] = value
    return base
