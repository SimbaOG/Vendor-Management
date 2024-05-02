def update_vals(base, update_with):
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
