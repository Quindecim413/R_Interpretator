import Execution.RuntimeErrors as errors

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


class Environment(object):
    @property
    def global_env(self):
        return _global_env_

    def __init__(self, parent_env):
        self.parent_env: Environment = parent_env
        self.__container__ = dict()

    def add(self, name, val):
        self.__container__[name] = val

    def clear(self):
        self.__container__ = dict()

    def find_object(self, name):
        if name in self.__container__:
            return self.__container__[name]
        if self.parent_env is None:
            raise errors.ObjectNotFound(name)
        return self.parent_env.find_object(name)

    def find_function(self, func_name):
        if func_name in self.__container__:
            r = self.__container__[func_name]
            if r.get_native_class().name != 'name' or r.evaluate(self).get_native_class().name != 'function':
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
