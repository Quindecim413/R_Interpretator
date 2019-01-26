from abc import abstractmethod
from R.Environment import Environment
from typing import List
import  R.Utils as utils
import R.RuntimeErrors as errors
import R.Types as types

import warnings


class NoClassRegistered(Exception):
    def __init__(self, class_name):
        super(NoClassRegistered, self).__init__("No class {} registered".format(class_name))


class RError(Exception):
    def __init__(self, call, description):
        self.call = call
        self.description = description


class RObj(object):
    def __init__(self, _type: types.BaseType):
        if not isinstance(_type, types.BaseType):
            raise Exception("invalid RObj type - {}".format(_type))
        self._type = _type
        # self.get_sub = utils.format_call_error(self, self.get_sub)
        # self.set_sub = utils.format_call_error(self, self.set_sub)
        # self.get_super_sub = utils.format_call_error(self, self.get_super_sub)
        # self.set_super_sub = utils.format_call_error(self, self.set_super_sub)
        # self.get_dlr = utils.format_call_error(self, self.get_dlr)
        # self.set_dlr = utils.format_call_error(self, self.set_dlr)
        # self.evaluate = utils.format_call_error(self, self.evaluate)
        self.attributes = dict()

    # def get_class(self):
    #     if 'class' in self.attributes:
    #         return
    #     return

    def set_value(self, value, env: Environment):
        raise errors.InvalidLeftHandAssignment()

    subs = dict()

    @classmethod
    def register_r_obj(cls, r_obj):
        if not issubclass(r_obj, RObj):
            raise Exception(r_obj.__name__ + " should be inherited from RObj")
        if r_obj.__name__ in cls.subs:
            warnings.warn("RObj \"{}\" has been registered again".format(r_obj.__name__))
        cls.subs[r_obj.__name__] = r_obj
        return r_obj

    @classmethod
    def get_r_obj(cls, name):
        sub = cls.subs.get(name, None)
        if sub is None:
            raise NoClassRegistered(name)

        return sub

    def get_type(self):
        return self._type

    def get_default_class(self):
        if self._type.name == 'list':
            return 'list'
        elif self._type.name == 'character':
            return 'character'
        elif self._type.name == 'double':
            return 'numeric'
        elif self._type.name == 'integer':
            return 'integer'
        elif self._type.name == 'closure':
            return 'function'

    @abstractmethod
    def show_self(self):
        raise NotImplementedError("{} should implement show_self() method".format(type(self).__name__))

    def get_sub(self, key, options: List[utils.NamedOption]):
        raise errors.ObjectNotSubSettable(self)

    def set_sub(self, key, value):
        raise errors.ObjectNotSubSettable(self)

    def get_super_sub(self, key):
        raise errors.ObjectNotSubSettable(self)

    def set_super_sub(self, key,  options: List[utils.NamedOption]):
        raise errors.ObjectNotSubSettable(self)

    def get_dlr(self, key):
        raise errors.ObjectNotSubSettable(self)

    def set_dlr(self, key, value):
        raise errors.ObjectNotSubSettable(self)

    @abstractmethod
    def create(self, *args, **kwargs):
        raise NotImplementedError("{} should implement create() method".format(type(self).__name__))

    @abstractmethod
    def evaluate(self, env: Environment):
        raise NotImplementedError("{} should implement evaluate() method".format(type(self).__name__))





class Arg(object):
    def __init__(self, name, value):
        if not name:
            raise Exception('Arg name should always be set')
        self.name = name
        if value is not None:
            if not isinstance(value, RObj):
                raise Exception('Arg accepts only RObj value. Got {}'.format(value))

        self.value: RObj = value

class Param(object):
    def __init__(self, name, value):
        self.name = name
        if value is None:
            raise Exception('Param value should always be set')
        if not isinstance(value, RObj):
            raise Exception('Param accepts only RObj value. Got {}'.format(value))

        self.value: RObj = value



utils.set_base(RObj)
