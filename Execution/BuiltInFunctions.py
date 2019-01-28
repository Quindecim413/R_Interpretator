from abc import abstractmethod
from typing import List

import Execution.Types as types
import Execution.Classes as classes
from Execution import Environment
from Execution.BaseObject import RObject
from Execution.Environment import Environment
from Execution.BaseObject import AtomicItem

builtin_env: Environment = Environment(None)


class BuiltInFunctionObj(RObject):
    def __init__(self, arguments: List[RObject]):
        super(BuiltInFunctionObj, self).__init__(classes.FunctionClass(), types.BuiltInType())
        self.arguments: List[RObject] = arguments

    @abstractmethod
    def evaluate(self, env: Environment):
        pass


class IsTrue(BuiltInFunctionObj):
    @staticmethod
    def create():
        return IsTrue([AtomicItem(None, types.BaseType, )])


class IsCharacter()


class AsInteger(BuiltInFunctionObj):
    @staticmethod
    def create(arguments):
        ret = AsInteger(arguments)
        return ret

    def evaluate(self, env: Environment):
        if
