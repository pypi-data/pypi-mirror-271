from functools import wraps


def singleton(cls):
    """
    A decorator that makes a class a singleton.
    :param cls: the class to be decorated
    :return: a decorated class
    """
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        """
        Wrap the invocation in singleton.
        :param args: args passed to the invocation
        :param kwargs: kwargs passed to the invocation
        :return: a singleton invocation
        """
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
