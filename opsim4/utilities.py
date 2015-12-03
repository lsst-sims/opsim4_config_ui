import importlib

def load_class(instance_obj):
    """Dynamically load a class from a string.

    This function was taken from the following blog:
    http://thomassileo.com/blog/2012/12/21/dynamically-load-python-modules-or-classes/

    Args:
        full_class_string (str): A standard import like call.

    Returns:
        instance: An instance of the class.
    """
    full_class_string = str(type(instance_obj)).split('\'')[1]

    class_data = full_class_string.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]

    module = importlib.import_module(module_path)
    # Finally, we retrieve the Class
    return getattr(module, class_str)

def title(tab_name):
    """Create a title for a tab.

    Args:
        tab_name (str): A potential title for a tab.

    Returns:
        str: A normalized tab title.
    """
    values = tab_name.split('_')
    for i, value in enumerate(values):
        if value == "lsst":
            values[i] = value.upper()
        else:
            values[i] = value.capitalize()
    return " ".join(values)
