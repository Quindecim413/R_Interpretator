from abc import abstractmethod
from R.Environment import Environment
from typing import List
from R.NonRObjs import *
import R.RuntimeErrors as errors
import R.Types as types

import warnings


class NoClassRegistered(Exception):
    def __init__(self, class_name):
        super(NoClassRegistered, self).__init__("No class {} registered".format(class_name))


class RError(Exception):
    def __init__(self, obj):
        super(Exception, self).__init__()
        self.obj: RObj = obj

    @staticmethod
    def create_simple(call, description):
        l: RObj = RObj.get_r_obj('ListObj')\
            .create([ListItem('call', call),
                     ListItem('message', RObj.get_r_obj('Atomic').create(description, types.CharacterType()))])
        l.set_attr('class', RObj.get_r_obj('Atomic').create('simpleError', types.CharacterType()))
        return l


def execute_item(executing_object, env):
    try:
        ret = executing_object.evaluate(env)
        return ret
    except errors.R_RuntimeError as e:
        r = RError.create_simple(executing_object, e.message)
        raise r


class RObj(object):
    def __init__(self, _type: types.BaseType):
        if not isinstance(_type, types.BaseType):
            raise Exception("invalid RObj type - {}".format(_type))
        self._type = _type
        self.attributes = dict()

    def get_attributes(self):
        return self.attributes

    def get_attr(self, name):
        return self.attributes.get(name, RObj.get_r_obj('NULLObj')())

    def set_attr(self, name, value):
        self.attributes[name] = value

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

    def get_class(self):
        r = self.attributes.get('class', None)
        if not r:
            ret = self.get_default_class()
            if not isinstance(ret, RObj) or ret.get_type().name != 'character':
                raise Exception('get_default_class() method in {} should return character RObj')
            return ret
        else:
            if not isinstance(r, RObj) or r.get_type().name != 'character':
                raise Exception('get_class() method found not character object in attributes[\'class\'] - {}'.format(r))
            return r

    def get_classes_as_python_list(self):
        cl = self.get_class()
        if isinstance(cl, RObj.get_r_obj('Atomic')):
            return [cl.value]
        else:
            res = []
            for item in self.items:
                res.append(item[1].value)
            return res

    @abstractmethod
    def get_default_class(self):
        raise NotImplementedError("{} should implement get_default_class() method".format(type(self).__name__))

    @abstractmethod
    def show_self(self, *args, **kwargs):
        raise NotImplementedError("{} should implement show_self() method".format(type(self).__name__))

    @abstractmethod
    def show_self_for_print(self, *args, **kwargs):
        raise NotImplementedError("{} should implement show_self_for_print() method".format(type(self).__name__))

    def get_items(self):
        raise errors.ObjectNotSubSettable(self)

    def get_sub(self, key, options: List[Param]):
        raise errors.ObjectNotSubSettable(self)

    def set_sub(self, key, value):
        raise errors.ObjectNotSubSettable(self)

    def get_super_sub(self, key):
        raise errors.ObjectNotSubSettable(self)

    def set_super_sub(self, key,  options: List[Param]):
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

    def compute(self, env: Environment):
        raise errors.ApplyToNonFunction()

set_RObj(RObj)