import importlib

def load_class(instance_obj):
    """
    Dynamically load a class from a string. Taken from the following blog:
    http://thomassileo.com/blog/2012/12/21/
           dynamically-load-python-modules-or-classes/
    @param full_class_string: A standard import like call.
    @return: An instance of the class.
    """
    full_class_string = str(type(instance_obj)).split('\'')[1]

    class_data = full_class_string.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]

    module = importlib.import_module(module_path)
    # Finally, we retrieve the Class
    return getattr(module, class_str)
