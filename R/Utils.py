from functools import wraps
import R.RuntimeErrors as errors

base_obj = None


def set_base(_base_obj):
    global base_obj
    base_obj = _base_obj


# def format_call_error(obj, method):
#     @wraps(method)
#     def wrapper(*args, **kwargs):
#         try:
#             return method(*args, **kwargs)
#         except errors.R_RuntimeError as e:
#             new_e = RError('Error in ' + obj.show_self() + ' :\n' + e.message)
#             raise new_e
#     return wrapper


class NamedOption(object):
    def __init__(self, name, opt_value):
        self._name = name
        self._opt_value = opt_value

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._opt_value
