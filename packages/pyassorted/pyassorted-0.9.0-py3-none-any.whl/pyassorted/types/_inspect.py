from typing import get_type_hints


def is_instance_of_typed_dict(obj, typed_dict_class):
    type_hints = get_type_hints(typed_dict_class)
    if not isinstance(obj, dict):
        return False
    for key, value_type in type_hints.items():
        if key in obj:
            if not isinstance(obj[key], value_type):
                return False
        elif typed_dict_class.__total__:
            return False
    return True
