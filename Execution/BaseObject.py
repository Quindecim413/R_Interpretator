from abc import abstractmethod
from typing import List

import Execution.Types as types
import Execution.Classes as classes
from Execution.Environment import Environment


# class Meta(object):
#     def __init__(self, _type: types.BaseType, _class: classes.BaseClass,
#                  subscriptable=False, ):
#         pass


class RObject:
    def __init__(self, _class: classes.BaseClass, _type: types.BaseType, subscriptable: bool):
        self._class = _class
        self._type = _type
        self._subscriptable = subscriptable
        self.__attributes__ = {}

    @staticmethod
    @abstractmethod
    def create(*args, **kwargs):
        pass

    @abstractmethod
    def evaluate(self, env: Environment):
        pass

    def get_type(self)->types.BaseType:
        return self._type.name

    def get_native_class(self):
        return self._class.name

    def get_class(self)->classes.BaseClass:
        if 'class' in self.__attributes__:
            return self.__attributes__['class']
        return self._class.name

    def get_attributes(self):
        return self.__attributes__

    def get_attribute(self, name):
        return self.__attributes__.get(name, None)


class AtomicItem(object):
    def __init__(self, value, type: types.BaseType, name:str):
        self._value = value
        self._type = type
        self._name: str = name

    def get_value(self):
        return self._value

    def get_type(self):
        return self._type

    def get_name(self):
        return self._name

    def set_value(self, value, type: types.BaseType):
        self._value = value
        self._type = type


class Param(object):
    def __init__(self, name, value):
        self._name = name
        self._value = value

    def get_name(self):
        return self._name

    def get_value(self):
        return self._value

    def fits(self, other_param):
        return other_param._name == self._name

    @staticmethod
    def create(name, value):
        return Param(name, value)


class Assignable(object):
    @abstractmethod
    def set_value(self, value, env: Environment):
        pass


class CallObj(RObject):
    def __init__(self):
        super(CallObj, self).__init__(classes.CallClass(), types.LanguageType())

    @abstractmethod
    def evaluate(self, env: Environment):
        pass


class SubSettable(object):
    @abstractmethod
    def get_item_buy(self, key) -> RObject:
        pass


    @abstractmethod
    def set_item_buy(self, key, value: RObject) -> RObject:
        pass

    @abstractmethod
    def get_subscript_item(self, key: RObject) -> RObject:
        pass

    @abstractmethod
    def set_subscript_item(self, key:RObject, value: RObject) -> RObject:
        pass






