RObj = None

def set_RObj(r_obj):
    global RObj
    RObj = r_obj


# class VectorItem(object):
#     def __init__(self, name, value):
#         self.name = name if name is not None else ''
#         if not isinstance(value, RObj.get_r_obj('Atomic')):
#             raise Exception('VectorItem accepts only Atomic value. Got {}'.format(value))
#         self.value = value

def VectorItem(name, value):
    if not isinstance(value, RObj.get_r_obj('Atomic')):
        raise Exception('VectorItem accepts only Atomic value. Got {}'.format(value))
    return name if name is not None else '', value


# class ListItem(object):
#     def __init__(self, name, value: RObj):
#         self.name = name if name is not None else ''
#         if not isinstance(value, RObj):
#             raise Exception('ListItem accepts only RObj value. Got {}'.format(value))
#         self.value: RObj = value

def ListItem(name, value):
    if not isinstance(value, RObj):
        raise Exception('ListItem accepts only RObj value. Got {}'.format(value))
    return name if name is not None else '', value


# class Arg(object):
#     def __init__(self, name, value):
#         if not name:
#             raise Exception('Arg name should always be set')
#         self.name = name
#         if value is not None:
#             if not isinstance(value, RObj):
#                 raise Exception('Arg accepts only RObj value. Got {}'.format(value))
#
#         self.value: RObj = value

def Arg(name, value):
    if not name:
        raise Exception('Arg name should always be specified')
    if value is not None:
        if not isinstance(value, RObj):
            raise Exception('Arg accepts only RObj value. Got {}'.format(value))
    return name if name is not None else '', value


# class Param(object):
#     def __init__(self, name, value):
#         self.name = name
#         if value is None:
#             raise Exception('Param value should always be set')
#         if not isinstance(value, RObj):
#             raise Exception('Param accepts only RObj value. Got {}'.format(value))
#
#         self.value: RObj = value

def Param(name, value):
    if value is None:
        raise Exception('Param value should always be set')
    if not isinstance(value, RObj):
        raise Exception('Param accepts only RObj value. Got {}'.format(value))
    return name if name is not None else '', value
