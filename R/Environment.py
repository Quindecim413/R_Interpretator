from typing import List

_global_env_ = None


class CommandException(Exception):
    pass


class BreakLoopCommand(CommandException):
    pass


class NextLoopCommand(CommandException):
    pass


class ReturnCommand(CommandException):
    def __init__(self, returned_value):
        self._returned_value = returned_value

    def get_value(self):
        return self._returned_value


class FailToFindFunction(Exception):
    pass


class Environment(object):
    _global_env = None
    @property
    def global_env(self):
        return self._global_env

    @classmethod
    def set_global(cls, env):
        if cls._global_env is not None:
            raise Exception('attempting to reset global environment')
        cls._global_env = env

    def __init__(self, parent_env):
        self.parent_env: Environment = parent_env
        self.__container__ = dict()

    def add(self, name, val):
        self.__container__[name] = val

    @property
    def container(self):
        return self.__container__

    def clear(self):
        self.__container__ = dict()

    def find_object(self, name):
        if name in self.__container__:
            return self.__container__[name]
        if self.parent_env is None:
            raise errors.ObjectNotFound(name)
        return self.parent_env.find_object(name)

    def find_function(self, func_name: str, classes_names: List=[]):
        if func_name.endswith('.default'):
            name = func_name.split('.default')[0]
            try:
                fun = self._find_function_for_class(name)
                return fun
            except FailToFindFunction:
                raise errors.FailedToFindFunction(func_name)
        elif len(classes_names) == 0:
            try:
                fun = self._find_function_for_class(func_name)
                return fun
            except FailToFindFunction:
                raise errors.FailedToFindFunction(func_name)
        else:
            for cls_name in classes_names:
                try:
                    fun = self._find_function_for_class(func_name+'.'+cls_name)
                    return fun
                except FailToFindFunction:
                    continue
            else:
                try:
                    fun = self._find_function_for_class(func_name)
                    return fun
                except FailToFindFunction:
                    raise errors.FailedToFindFunction(func_name)


        # if func_name in self.__container__:
        #     r = self.__container__[func_name]
        #     if r.get_type().name not in ['closure', 'builtin']:
        #         if self.parent_env is None:
        #             raise errors.FailedToFindFunction(func_name)
        #         return self.parent_env.find_function(func_name)
        #     return r
        # if self.parent_env is None:
        #     raise errors.FailedToFindFunction(func_name)
        # return self.parent_env.find_function(func_name)

    def _find_function_for_class(self, func_name):
        if func_name in self.__container__:
            r = self.__container__[func_name]
            if r.get_type().name not in ['closure', 'builtin']:
                if self.parent_env is None:
                    raise errors.FailedToFindFunction(func_name)
                return self.parent_env.find_function(func_name)
            return r
        if self.parent_env is None:
            raise errors.FailedToFindFunction(func_name)
        return self.parent_env.find_function(func_name)

    def emit_exception(self, e):
        raise e

    def emit_return(self, value):
        raise ReturnCommand(value)

    def emit_break(self):
        raise BreakLoopCommand()

    def emit_next(self):
        raise NextLoopCommand()












