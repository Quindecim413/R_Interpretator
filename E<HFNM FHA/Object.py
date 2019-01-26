from .Types import *
import Object
class Object:
    def __init__(self, _value, _class, _type):
        self._value = _value
        self._class = _class
        self._type = _type
        self.__attributes__ = {}

    def get_value(self):
        return self._value

    def get_type(self):
        return self._type

    def get_class(self):
        if 'class' in self.__attributes__:
            return self.__attributes__['class']
        return self._type._class

