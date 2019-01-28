import Execution.Types as types
import Execution.Classes as classes
import Execution.RuntimeErrors as errors

from Execution.Environment import Environment, NextLoopCommand, BreakLoopCommand, ReturnCommand
from typing import List, FrozenSet
from Execution.BaseObject import RObject, CallObj, SubSettable, Assignable
import Execution.AtomicObjects as atomic


class VariableObj(RObject, Assignable):
    def __init__(self, name):
        super(VariableObj, self).__init__(classes.NameClass(), types.SymbolType())
        self._name = name

    def set_value(self, value, env: Environment):
        env.add(self._name, value)
        return value

    def get_name(self):
        return self._name

    @staticmethod
    def create(name):
        return VariableObj(name)

    def evaluate(self, env: Environment):
        return env.find_object(self._name)


class DLRObj(CallObj, Assignable):
    def __init__(self, base_obj, name):
        super(DLRObj, self).__init__()
        self._base_obj: RObject = base_obj
        self._name = name

    @staticmethod
    def create(base_obj, name):
        return DLRObj(base_obj, name)

    def set_value(self, value, env: Environment):
        val_base_obj: SubSettable = self.__eval_base__(env)
        val_base_obj.set_item_buy(self._name, value)

    def __eval_base__(self, env: Environment):
        val_base_obj = self._base_obj.evaluate(env)
        if not isinstance(val_base_obj, SubSettable):
            raise errors.DLRAppliedNotToSubsettable(self._name)

        return val_base_obj


    def evaluate(self, env: Environment):
        val_base_obj: SubSettable = self.__eval_base__(env)
        try:
            obj: RObject = val_base_obj.get_item_buy(self._name)
            return obj
        except errors.ObjectNotFound:
            return atomic.NULLObj()


# class SimpleAssignValueObj(CallObj):
#     def __init__(self, item, value):
#         super(SimpleAssignValueObj, self).__init__()
#         self._item:RObject = item
#         self._value:RObject = value
#
#     def create(item, value):
#         return AssignValueObj(item, value)
#
#     def evaluate(self, env: Environment):

class AssignValueObj(CallObj):
    def __init__(self, item, value, type):
        super(AssignValueObj, self).__init__()
        self._item: RObject = item
        self._value: RObject = value
        self._type = type
        self._evaluated_item: RObject = None

    def get_type(self):
        return self._type

    def get_item(self):
        return self._item

    def get_item_evaluated(self):
        return self._evaluated_item

    @staticmethod
    def create(item, value, type: str):
        if type not in ['plain', 'simple', 'super']:
            raise Exception('invalid assignment typing - {}'.format(type))
        return AssignValueObj(item, value, type)

    def evaluate(self, env: Environment):
        if self._item.get_type().name == 'symbol':
            self._evaluated_item = self._item
        elif isinstance(self._item, atomic.AtomicItem):
            if self._item.get_type().name == "character":
                self._evaluated_item: VariableObj = VariableObj.create(self._item.get_value())
                val_value = self._value.evaluate(env)
                return self._evaluated_item.set_value(val_value, env)

# class SuperAssignValueObj(CallObj):
#     def __init__(self, item, value):
#         super(SuperAssignValueObj, self).__init__()
#         self._item: RObject = item
#         self._value: RObject = value
#
#     def create(item, value):
#         return AssignValueObj(item, value)
#
#     def evaluate(self, env: Environment):
#         pass


# class IndexingObj(CallObj):
#     def __init__(self):
#         super(IndexingObj, self).__init__()


class IndexingCallObj(CallObj, Assignable):
    def __init__(self, base_obj, passed_args):
        super(IndexingCallObj, self).__init__()
        self._base_obj = base_obj
        self._passed_args:List[RObject] = passed_args

    @staticmethod
    def create(base_obj, passed_args):
        return IndexingCallObj(base_obj, passed_args)

    def set_value(self, value, env: Environment):
        val_base: SubSettable = self.__eval_base__(env)
        val_base.set_item_buy(self._passed_args, value)

    def __eval_base__(self, env: Environment):
        val_base_obj = self._base_obj.evaluate(env)
        if not isinstance(val_base_obj, SubSettable):
            raise errors.ObjectNotSubSettable("some indexing [] object")

        return val_base_obj

    def evaluate(self, env: Environment):
        values = []
        for arg in self._passed_args:
            val = arg.evaluate(env)
            values.append(val)
        val_base: SubSettable = self.__eval_base__(env)
        ret = val_base.get_item_buy(values)
        return ret


class SuperIndexingCallObj(CallObj, Assignable):
    def __init__(self, base_obj, passed_arg):
        super(SuperIndexingCallObj, self).__init__()
        self._base_obj = base_obj
        self._passed_arg: RObject = passed_arg

    @staticmethod
    def create(base_obj, passed_arg):
        return IndexingCallObj(base_obj, passed_arg)

    def set_value(self, value, env: Environment):
        val_base: SubSettable = self.__eval_base__(env)
        val_base.set_item_buy(self._passed_arg, value)

    def __eval_base__(self, env: Environment):
        val_base_obj = self._base_obj.evaluate(env)
        if not isinstance(val_base_obj, SubSettable):
            raise errors.ObjectNotSubSettable("some indexing [[]] object")

        return val_base_obj

    def evaluate(self, env: Environment):
        val_arg = self._passed_arg.evaluate(env)
        val_base: SubSettable = self.__eval_base__(env)
        ret = val_base.subscript_item(val_arg)
        return ret


class Suite(RObject):
    def __init__(self, children):
        super(Suite, self).__init__(classes.SuiteClass(), types.LanguageType())
        self._children: List[RObject] = children

    @staticmethod
    def create(children):
        return Suite(children)

    def evaluate(self, env: Environment):
        last = None
        for ch in self._children:
            last = ch.evaluate(env)
        return last


class RepeatClass(CallObj):
    def __init__(self, body):
        super(RepeatClass, self).__init__()
        self._body:RObject = body

    @staticmethod
    def create(body):
        return RepeatClass(body)

    def evaluate(self, env: Environment):
        while True:
            try:
                self._body.evaluate(env)
            except NextLoopCommand:
                continue
            except BreakLoopCommand:
                return atomic.NULLObj()


class WhileClass(CallObj):
    def __init__(self, argument, body):
        super(WhileClass, self).__init__()
        self._body: RObject = body
        self._argument: RObject = argument

    @staticmethod
    def create(argument, body):
        return WhileClass(argument, body)

    def evaluate(self, env: Environment):
        arg_val: RObject = self._argument.evaluate(env)
        while True:
            if not arg_val.get_native_class().inherits("vector"):
                raise errors.ArgNotInterpretableAsLogical()




# class AdditionObj(CallObj):
#     def __init__(self, left:RObject, right: RObject):
#         super(AdditionObj, self).__init__()
#         self._left = left
#         self._right = right
#
#     def evaluate(self, env: Environment):
#         val_left: RObject = self._left.evaluate(env)
#         val_right: RObject = self._right.evaluate(env)
#
#         if val_left.get_type().name in ['']


