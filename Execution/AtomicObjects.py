from abc import abstractmethod
from typing import List

import Execution.Types as types
import Execution.Classes as classes
import Execution.RuntimeErrors as errors
from Execution.Environment import Environment, ReturnCommand
from Execution.BaseObject import RObject, SubSettable, CallObj, AtomicItem, Param

import Execution.LanguageObjects as language


# class LogicalObj(RObject, Atomic, SubSettable):
#     def __init__(self, boolean_values):
#         super(LogicalObj, self).__init__(classes.LogicalClass(), types.LogicalType())
#         self._boolean_values = boolean_values
#
#     @staticmethod
#     def create(boolean_values):
#         return LogicalObj(boolean_values)
#
#     def get_items(self):
#         return self._boolean_values
#
#     def evaluate(self, env: Environment):
#         return self
#
#
# class NumericObj(RObject, Atomic):
#     def __init__(self, numeric_values):
#         super(NumericObj, self).__init__(classes.NumericClass(), types.DoubleType())
#         self._numeric_values = numeric_values
#
#     @staticmethod
#     def create(numeric_values):
#         return NumericObj(numeric_values)
#
#     def get_items(self):
#         return self._numeric_values
#
#     def evaluate(self, env: Environment):
#         return self
#
#
# class IntegerObj(RObject, Atomic):
#     def __init__(self, integer_values):
#         super(IntegerObj, self).__init__(classes.IntegerClass(), types.IntegerType())
#         self._integer_values = integer_values
#
#     @staticmethod
#     def create(integer_values):
#         return IntegerObj(integer_values)
#
#     def get_items(self):
#         return self._integer_values
#
#     def evaluate(self, env: Environment):
#         return self
#
#
# class CharacterObj(RObject, Atomic):
#     def __init__(self, character_values):
#         super(CharacterObj, self).__init__(classes.CharacterClass(), types.CharacterType())
#         self._character_values = character_values
#
#     @staticmethod
#     def create(character_values):
#         return CharacterObj(character_values)
#
#     def get_items(self):
#         return self._character_values
#
#     def evaluate(self, env: Environment):
#         return self

def get_indexing(vector):
    if len(vector) == 0:
        return []
    items = vector.get_items()
    for item in items:
        val = item.get_value()



class ListItem(RObject):
    def __init__(self, value: RObject, name=''):
        super(ListItem, self).__init__(value.get_native_class(), value.get_type())
        self._name = name
        self._value = value

    @staticmethod
    def get_value(self):
        return self._value

    def get_name(self):
        return self._name


class ListObj(RObject, SubSettable):
    def get_item_buy(self, key: RObject) -> RObject:
        # if key.get_type().name not in ['']
        pass

    def set_item_buy(self, key: RObject, value: RObject) -> RObject:
        pass

    def get_subscript_item(self, key: RObject) -> RObject:
        pass

    def set_subscript_item(self, key: RObject, value: RObject) -> RObject:
        pass

    def __init__(self, values: List[RObject]):
        super(RObject, self).__init__(classes.ListClass(), types.ListType())
        self._values: List[ListItem] = values

    @staticmethod
    def create(values):
        return ListObj(values)

    def evaluate(self, env: Environment):
        return self


class VectorObj(RObject):
    def __init__(self, items):
        super(VectorObj, self).__init__(items[0].get_native_class(), items[0].get_type())
        itms = self._filter_nulls(items)
        self._items = []

    def get_items(self):
        return self._items

    @staticmethod
    def _filter_nulls(items: List[RObject]):
        ret = list(filter(lambda i: i.get_type().name != "NULL", items))
        return ret

    @staticmethod
    def create(items: List):
        types = {item.get_type().name for item in items}
        vectored = {'double', 'integer', 'logical', 'character'}
        if len(types.intersection(vectored)) > 0:
            return

    # def get_type(self):
    #     pass
    #
    # def get_value(self):
    #     pass
    #
    # def get_items(self):
    #     pass

    def set_items(self, items):
        self._items = self._filter_nulls(items)
        # if


class NULLObj(RObject):
    def __init__(self):
        super(NULLObj, self).__init__(classes.NULLClass(), types.NULLType())

    @staticmethod
    def create(self):
        return NULLObj()

    def evaluate(self, env: Environment):
        return self


# class VectorObj(RObject):
#     def create(children: List[RObject]):
#         not_null = list(filter(lambda ch: ch.get_type().name != 'NULL', children))
#         if len(not_null) == 0:
#             return NULLObj()


class DotsObj(RObject):
    def __init__(self, args):
        super(DotsObj, self).__init__(classes.DotsClass(), types.DotsType())
        self._args = args

    @staticmethod
    def create(args):
        return DotsObj(args)

    def evaluate(self, env: Environment):
        return self



class FunctionObj(RObject):
    def __init__(self, arguments: List[Param], body, parse_args_for_list=False):
        super(FunctionObj, self).__init__(classes.FunctionClass(), types.ClosureType())
        self._arguments: List[Param] = arguments
        self._body: RObject = body
        self._parse_args_for_list = parse_args_for_list

    @staticmethod
    def create(arguments, body):
        return FunctionObj(arguments, body)

    def parse_passed_args(self, passed_args: List[RObject], env: Environment):
        new_env: Environment = Environment(env)
        not_defaulted_func_params = {param.get_name(): None for param in self._arguments if param.get_value() is not None}

        named_args = []

        unnamed_values = []

        for arg in passed_args:
            if isinstance(arg, language.AssignValueObj):
                arg: language.AssignValueObj = arg
                if arg.get_type() == 'plain':
                    val = arg.evaluate(new_env)
                    if arg.get_item_evaluated().get_type().name != 'symbol':
                        raise errors.UnexpectedPlainAssignment()
                    arg.get_item_evaluated().set_value(val, new_env)
                    name = arg.get_item_evaluated().get_name()
                    named_args.append(name)
                    continue

                if arg.get_type() == 'simple':
                    val = arg.evaluate(new_env)
                    if arg.get_item_evaluated().get_type().name != 'symbol':
                        raise errors.UnexpectedSimpleAssignment()
                    arg.get_item_evaluated().set_value(val, new_env)
                    if self._parse_args_for_list:
                        arg.get_item_evaluated().set_value(val, env.global_env)
                    name = arg.get_item_evaluated().get_name()
                    named_args.append(name)
                    continue

                if arg.get_type() == 'super':
                    val = arg.get_type()
                    if arg.get_item_evaluated().get_type().name != 'symbol':
                        raise errors.UnexpectedSuperAssignment()

                    arg.get_item_evaluated().set_value(val, new_env)
                    arg.get_item_evaluated().set_value(val, env.global_env)
                    name = arg.get_item_evaluated().get_name()
                    named_args.append(name)
                    continue
            else:
                val = arg.evaluate(env)
                unnamed_values.append(val)
        i = 0
        c = 0
        ln = len(unnamed_values)
        for k, v in not_defaulted_func_params:
            if i == ln:
                raise errors.UnusedArguments(len(not_defaulted_func_params) - c)
            c = c + 1
            if k == '...':
                not_defaulted_func_params[k] = DotsObj.create(unnamed_values[i:])
                break
            else:
                not_defaulted_func_params[k].append(unnamed_values[i])
                i = i + 1

        return new_env


    def get_arguments(self):
        return self._arguments

    def get_body(self):
        return self._body

    def evaluate(self, env: Environment):
        try:
            return self._body.evaluate(env)
        except ReturnCommand as r:
            return r.get_value()


class FunctionCallObj(CallObj):
    def __init__(self, passed_args, func: FunctionObj):
        super(FunctionCallObj, self).__init__()
        self._passed_args = passed_args
        self._func: FunctionObj = func

    @staticmethod
    def create(passed_args, func: FunctionObj):
        return FunctionObj(passed_args, func)

    def evaluate(self, env: Environment):
        new_env = self._func.parse_passed_args(self._passed_args, env)

        return self._func.evaluate(new_env)


