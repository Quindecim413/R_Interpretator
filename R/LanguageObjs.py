from R.Environment import Environment, NextLoopCommand, BreakLoopCommand
from R.RObj import RObj, RError, execute_item
import R.Types as types
import R.RuntimeErrors as errors
import R.AtomicObjs as atomics
import R.Function as function
from R.Function import arrange_params_with_function_args
from typing import List
from R.Atomics import *


# def init_if_atomic(maybe_atomic):
#     if isinstance(maybe_atomic, RObj.get_r_obj('Atomic')):
#         ret = RObj.get_r_obj('VectorObj')([atomics.VectorItem(None, maybe_atomic)])
#         return ret
#     else:
#         return maybe_atomic

@RObj.register_r_obj
class DLRObj(RObj):
    def __init__(self, x: RObj, key: RObj):
        super(DLRObj, self).__init__(types.LanguageType())
        self.x = x
        self.key = key

    def show_self(self):
        val_x = self.x.show_self()
        val_key = self.key.show_self()
        ret = val_x + '$' + val_key
        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('$', types.CharacterType())

    @staticmethod
    def create(base: RObj, item: RObj):
        return DLRObj(base, item)

    def evaluate(self, env: Environment):
        x, key = self.x.evaluate(env), self.key.evaluate(env)
        func: function.FunctionObj = env.find_function('$')
        new_env = arrange_params_with_function_args([function.Param('x', x), function.Param('key', key)], func, env)
        ret = func.compute(new_env)
        return ret


@RObj.register_r_obj
class IndexingObj(RObj):
    def __init__(self, x: RObj, keys: RObj):
        super(IndexingObj, self).__init__(types.LanguageType())
        self.x = x
        self.keys = keys

    def show_self(self):
        val_x = self.x.show_self()
        val_keys = [key.show_self() for key in self.keys]
        ret = val_x + '[' + ' ,'.join(val_keys) + ']'
        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('[', types.CharacterType())

    @staticmethod
    def create(base: RObj, items: RObj):
        return IndexingObj(base, items)

    def evaluate(self, env: Environment):
        x, key = self.x.evaluate(env), self.key.evaluate(env)
        func: function.FunctionObj = env.find_function('[')
        new_env = arrange_params_with_function_args([function.Param('x', x), function.Param('keys', key)], func, env)
        ret = func.compute(new_env)
        return ret


@RObj.register_r_obj
class SuperIndexingObj(RObj):
    def __init__(self, x: RObj, key: RObj):
        super(SuperIndexingObj, self).__init__(types.LanguageType())
        self.x = x
        self.key = key

    def show_self(self):
        val_x = self.x.show_self()
        val_key = self.key.show_self()
        ret = val_x + '[[' + val_key + ']]'
        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('[[', types.CharacterType())

    @staticmethod
    def create(base: RObj, item: RObj):
        return SuperIndexingObj(base, item)

    def evaluate(self, env: Environment):
        x, key = self.x.evaluate(env), self.key.evaluate(env)
        func: function.FunctionObj = env.find_function('[[')
        new_env = arrange_params_with_function_args([function.Param('x', x), function.Param('key', key)], func, env)
        ret = func.compute(new_env)
        return ret


@RObj.register_r_obj
class AssignObj(RObj):
    def __init__(self, item, value):
        super(AssignObj, self).__init__(types.LanguageType())
        self.item: RObj = item
        self.value: RObj = value

    def get_default_class(self):
        val_op = '='
        return RObj.get_r_obj('Atomic')(val_op, types.CharacterType())

    def show_self(self):
        val_item = self.item.show_self()
        val_val = self.value.show_self()

        val_op = ' = '

        ret = val_item + val_op + val_val
        return ret

    show_self_for_print = show_self

    @staticmethod
    def create(item, value):
        call = AssignObj(item, value)
        return call

    def evaluate(self, env: Environment):
        fun_to_find = '<-'

        if isinstance(self.item, DLRObj):
            fun_to_find = '$<-'
        elif isinstance(self.item, AssignObj):
            fun_to_find = '[<-'
        elif isinstance(self.item, SuperAssignObj):
            fun_to_find = '[[<-'

        func: function.FunctionObj = env.find_function(fun_to_find, self.item.get_classes_as_python_list())

        new_env = arrange_params_with_function_args(
            [function.Param('x', self.item), function.Param('value', self.value)],
            func, env)
        ret = func.compute(new_env)
        return ret



        # if self.mode == 'super':
        #     env = env.global_env
        #     if self.item.get_type().name == 'symbol':
        #         val_value: RObj = self.value.evaluate(env)
        #         name = self.item.name
        #         env.add(name, val_value)
        #         return val_value
        #     elif isinstance(self.item, RObj.get_r_obj('Atomic')):
        #         if self.item.get_type().name == "character":
        #             name = self.item.value
        #             val_value: RObj = self.value.evaluate(env)
        #             env.add(name, val_value)
        #             return val_value
        #         else:
        #             raise errors.InvalidLeftHandAssignment()
        #     else:
        #         val_value: RObj = self.value.evaluate(env)
        #         ret = self.item.set_value(val_value, env)
        #         return ret
        #     # if env == env.global_env:
        #     #     if self.item.get_type().name == 'symbol':
        #     #         val_value: RObj = self.init_if_atomic(self.value.evaluate(env))
        #     #         name = self.item.name
        #     #         env.add(name, val_value)
        #     #         return val_value
        #     #     elif isinstance(self.item, RObj.get_r_obj('Atomic')):
        #     #         if self.item.get_type().name == "character":
        #     #             name = self.item.value
        #     #             val_value: RObj = self.init_if_atomic(self.value.evaluate(env))
        #     #             env.add(name, val_value)
        #     #             return val_value
        #     #         else:
        #     #             raise errors.InvalidLeftHandAssignment()
        #     #     else:
        #     #         val_value: RObj = self.init_if_atomic(self.value.evaluate(env))
        #     #         ret = self.item.set_value(val_value, env)
        #     #         return ret
        #     # else:
        #     #     if self.item.get_type().name == 'symbol':
        #     #         val_value: RObj = self.init_if_atomic(self.value.evaluate(env))
        #     #         name = self.item.name
        #     #         env.add(name, val_value)
        #     #         env.global_env.add(name, val_value)
        #     #         return val_value
        #     #     elif isinstance(self.item, RObj.get_r_obj('Atomic')):
        #     #         if self.item.get_type().name == "character":
        #     #             name = self.item.value
        #     #             val_value: RObj = self.init_if_atomic(self.value.evaluate(env))
        #     #             env.add(name, val_value)
        #     #             env.global_env.add(name, val_value)
        #     #             return val_value
        #     #         else:
        #     #             raise errors.InvalidLeftHandAssignment()
        #     #     else:
        #     #         raise errors.InvalidLeftHandAssignment()
        # else:
        #     if self.item.get_type().name == 'symbol':
        #         val_value: RObj = self.value.evaluate(env)
        #         name = self.item.name
        #         env.add(name, val_value)
        #         return val_value
        #     elif isinstance(self.item, RObj.get_r_obj('Atomic')):
        #         if self.item.get_type().name == "character":
        #             name = self.item.value
        #             val_value: RObj = self.value.evaluate(env)
        #             env.add(name, val_value)
        #             return val_value
        #         else:
        #             raise errors.InvalidLeftHandAssignment()
        #     else:
        #         val_value: RObj = self.value.evaluate(env)
        #         ret = self.item.set_value(val_value, env)
        #         return ret


@RObj.register_r_obj
class SimpleAssignObj(RObj):
    def __init__(self, item, value):
        super(SimpleAssignObj, self).__init__(types.LanguageType())
        self.item: RObj = item
        self.value: RObj = value

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('<-', types.CharacterType())

    def show_self(self):
        val_item = self.item.show_self()
        val_val = self.value.show_self()

        ret = val_item + ' <- ' + val_val
        return ret

    show_self_for_print = show_self

    @staticmethod
    def create(item, value):
        call = SimpleAssignObj(item, value)
        return call

    def evaluate(self, env: Environment):
        fun_to_find = '<-'

        if isinstance(self.item, DLRObj):
            fun_to_find = '$<-'
        elif isinstance(self.item, AssignObj):
            fun_to_find = '[<-'
        elif isinstance(self.item, SuperAssignObj):
            fun_to_find = '[[<-'

        func: function.FunctionObj = env.find_function(fun_to_find, self.item.get_classes_as_python_list())

        new_env = arrange_params_with_function_args(
            [function.Param('x', self.item), function.Param('value', self.value)],
            func, env)
        ret = func.compute(new_env)
        return ret

        # try:
        #
        #
        #
        # if self.mode == 'super':
        #     env = env.global_env
        #     if self.item.get_type().name == 'symbol':
        #         val_value: RObj = self.value.evaluate(env)
        #         name = self.item.name
        #         env.add(name, val_value)
        #         return val_value
        #     elif isinstance(self.item, RObj.get_r_obj('Atomic')):
        #         if self.item.get_type().name == "character":
        #             name = self.item.value
        #             val_value: RObj = self.value.evaluate(env)
        #             env.add(name, val_value)
        #             return val_value
        #         else:
        #             raise errors.InvalidLeftHandAssignment()
        #     else:
        #         val_value: RObj = self.value.evaluate(env)
        #         ret = self.item.set_value(val_value, env)
        #         return ret
        # else:
        #     if self.item.get_type().name == 'symbol':
        #         val_value: RObj = self.value.evaluate(env)
        #         name = self.item.name
        #         env.add(name, val_value)
        #         return val_value
        #     elif isinstance(self.item, RObj.get_r_obj('Atomic')):
        #         if self.item.get_type().name == "character":
        #             name = self.item.value
        #             val_value: RObj = self.value.evaluate(env)
        #             env.add(name, val_value)
        #             return val_value
        #         else:
        #             raise errors.InvalidLeftHandAssignment()
        #     else:
        #         val_value: RObj = self.value.evaluate(env)
        #         ret = self.item.set_value(val_value, env)
        #         return ret


@RObj.register_r_obj
class SuperAssignObj(RObj):
    def __init__(self, item, value):
        super(SuperAssignObj, self).__init__(types.LanguageType())
        self.item: RObj = item
        self.value: RObj = value

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('<<-', types.CharacterType())

    def show_self(self):
        val_item = self.item.show_self()
        val_val = self.value.show_self()

        ret = val_item + ' <<- ' + val_val
        return ret

    show_self_for_print = show_self

    @staticmethod
    def create(item, value):
        call = function.CallObj.create_from_lang_obj(SuperAssignObj(item, value))
        return call

    def evaluate(self, env: Environment):
        return self

    def compute(self, env: Environment):
        fun_to_find = '<-'

        if isinstance(self.item, DLRObj):
            fun_to_find = '$<-'
        elif isinstance(self.item, AssignObj):
            fun_to_find = '[<-'
        elif isinstance(self.item, SuperAssignObj):
            fun_to_find = '[[<-'

        func: function.FunctionObj = env.global_env.find_function(fun_to_find, self.item.get_classes_as_python_list())

        new_env = arrange_params_with_function_args([function.Param('x', self.item), function.Param('value', self.value)],
                                                func, env.global_env)
        ret = func.compute(new_env)
        return ret


@RObj.register_r_obj
class AndObj(RObj):
    def __init__(self, x: RObj, y: RObj):
        super(AndObj, self).__init__(types.BuiltInType())
        self.x: RObj = x
        self.y: RObj = y

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('function', types.CharacterType())

    def show_self(self):
        val_x = self.x.show_self()
        val_y = self.y.show_self()
        ret = val_x + ' & ' + val_y
        return ret

    show_self_for_print = show_self

    @staticmethod
    def create(x: RObj, y: RObj):
        call = function.CallObj.create_from_lang_obj(AddObj(x, y))
        return call

    def evaluate(self, env: Environment):
        return self

    def compute(self, env: Environment):
        x, y = self.x.evaluate(env), self.y.evaluate(env)
        func: function.FunctionObj = env.find_function('&')
        new_env = arrange_params_with_function_args([function.Param('x', x), function.Param('y', y)], func, env)
        ret = func.compute(new_env)
        return ret


@RObj.register_r_obj
class AndAndObj(RObj):
    def __init__(self, x: RObj, y: RObj):
        super(AndAndObj, self).__init__(types.BuiltInType())
        self.x = x
        self.y = y

    def show_self(self):
        val_x = self.x.show_self()
        val_y = self.y.show_self()
        ret = val_x + ' && ' + val_y
        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('function', types.CharacterType())

    @staticmethod
    def create(x: RObj, y: RObj):
        call = function.CallObj.create_from_lang_obj(AndAndObj(x, y))
        return call

    def evaluate(self, env: Environment):
        return self

    def compute(self, env: Environment):
        x, y = self.x.evaluate(env), self.y.evaluate(env)
        func: function.FunctionObj = env.find_function('&&')
        new_env = arrange_params_with_function_args([function.Param('x', x), function.Param('y', y)], func, env)
        ret = func.compute(new_env)
        return ret


@RObj.register_r_obj
class OrObj(RObj):
    def __init__(self, x: RObj, y: RObj):
        super(OrObj, self).__init__(types.BuiltInType())
        self.x = x
        self.y = y

    def show_self(self):
        val_x = self.x.show_self()
        val_y = self.y.show_self()
        ret = val_x + ' | ' + val_y
        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('function', types.CharacterType())

    @staticmethod
    def create(x: RObj, y: RObj):
        call = function.CallObj.create_from_lang_obj(OrObj(x, y))
        return call

    def evaluate(self, env: Environment):
        return self

    def compute(self, env: Environment):
        x, y = self.x.evaluate(env), self.y.evaluate(env)
        func: function.FunctionObj = env.find_function('|')
        new_env = arrange_params_with_function_args([function.Param('x', x), function.Param('y', y)], func, env)
        ret = func.compute(new_env)
        return ret


@RObj.register_r_obj
class OrOrObj(RObj):
    def __init__(self, x: RObj, y: RObj):
        super(OrOrObj, self).__init__(types.BuiltInType())
        self.x = x
        self.y = y

    def show_self(self):
        val_x = self.x.show_self()
        val_y = self.y.show_self()
        ret = val_x + ' || ' + val_y
        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('function', types.CharacterType())

    @staticmethod
    def create(x: RObj, y: RObj):
        call = function.CallObj.create_from_lang_obj(OrOrObj(x, y))
        return call

    def evaluate(self, env: Environment):
        return self

    def compute(self, env: Environment):
        x, y = self.x.evaluate(env), self.y.evaluate(env)
        func: function.FunctionObj = env.find_function('||')
        new_env = arrange_params_with_function_args([function.Param('x', x), function.Param('y', y)], func, env)
        ret = func.compute(new_env)
        return ret


@RObj.register_r_obj
class NotObj(RObj):
    def __init__(self, x: RObj):
        super(NotObj, self).__init__(types.BuiltInType())
        self.x = x

    def show_self(self):
        val_x = self.x.show_self()
        return '!' + val_x

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('function', types.CharacterType())

    @staticmethod
    def create(x: RObj):
        call = function.CallObj.create_from_lang_obj(NotObj(x))
        return call

    def evaluate(self, env: Environment):
        return self

    def compute(self, env: Environment):
        x, y = self.x.evaluate(env), self.y.evaluate(env)
        func: function.FunctionObj = env.find_function('!')
        new_env = arrange_params_with_function_args([function.Param('x', x)], func, env)
        ret = func.compute(new_env)
        return ret

# TODO

@RObj.register_r_obj
class EqualObj(RObj):
    def __init__(self, x: RObj, y: RObj):
        super(EqualObj, self).__init__(types.BuiltInType())
        self.x = x
        self.y = y

    def show_self(self):
        val_x = self.x.show_self()
        val_y = self.y.show_self()
        ret = val_x + ' == ' + val_y
        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('function', types.CharacterType())

    @staticmethod
    def create(x: RObj, y: RObj):
        call = function.CallObj.create_from_lang_obj(EqualObj(x, y))
        return call

    def evaluate(self, env: Environment):
        return self

    def compute(self, env: Environment):
        x, y = self.x.evaluate(env), self.y.evaluate(env)
        func: function.FunctionObj = env.find_function('==')
        new_env = arrange_params_with_function_args([function.Param('x', x), function.Param('y', y)], func, env)
        ret = func.compute(new_env)
        return ret


@RObj.register_r_obj
class NotEqualObj(RObj):
    def __init__(self, x: RObj, y: RObj):
        super(NotEqualObj, self).__init__(types.BuiltInType())
        self.x = x
        self.y = y

    def show_self(self):
        val_x = self.x.show_self()
        val_y = self.y.show_self()
        ret = val_x + ' != ' + val_y
        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('function', types.CharacterType())

    @staticmethod
    def create(x: RObj, y: RObj):
        call = function.CallObj.create_from_lang_obj(NotEqualObj(x, y))
        return call

    def evaluate(self, env: Environment):
        return self

    def compute(self, env: Environment):
        x, y = self.x.evaluate(env), self.y.evaluate(env)
        func: function.FunctionObj = env.find_function('!=')
        new_env = arrange_params_with_function_args([function.Param('x', x), function.Param('y', y)], func, env)
        ret = func.compute(new_env)
        return ret


@RObj.register_r_obj
class GreaterObj(RObj):
    def __init__(self, x: RObj, y: RObj):
        super(GreaterObj, self).__init__(types.BuiltInType())
        self.x = x
        self.y = y

    def show_self(self):
        val_x = self.x.show_self()
        val_y = self.y.show_self()
        ret = val_x + ' > ' + val_y
        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('function', types.CharacterType())

    @staticmethod
    def create(x: RObj, y: RObj):
        call = function.CallObj.create_from_lang_obj(GreaterObj(x, y))
        return call

    def evaluate(self, env: Environment):
        return self

    def compute(self, env: Environment):
        x, y = self.x.evaluate(env), self.y.evaluate(env)
        func: function.FunctionObj = env.find_function('>')
        new_env = arrange_params_with_function_args([function.Param('x', x), function.Param('y', y)], func, env)
        ret = func.compute(new_env)
        return ret


@RObj.register_r_obj
class GreaterOrEqualObj(RObj):
    def __init__(self, x: RObj, y: RObj):
        super(GreaterOrEqualObj, self).__init__(types.BuiltInType())
        self.x = x
        self.y = y

    def show_self(self):
        val_x = self.x.show_self()
        val_y = self.y.show_self()
        ret = val_x + ' >= ' + val_y
        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('function', types.CharacterType())

    @staticmethod
    def create(x: RObj, y: RObj):
        call = function.CallObj.create_from_lang_obj(GreaterOrEqualObj(x, y))
        return call

    def evaluate(self, env: Environment):
        return self

    def compute(self, env: Environment):
        x, y = self.x.evaluate(env), self.y.evaluate(env)
        func: function.FunctionObj = env.find_function('>=')
        new_env = arrange_params_with_function_args([function.Param('x', x), function.Param('y', y)], func, env)
        ret = func.compute(new_env)
        return ret


@RObj.register_r_obj
class LessObj(RObj):
    def __init__(self, x: RObj, y: RObj):
        super(LessObj, self).__init__(types.BuiltInType())
        self.x = x
        self.y = y

    def show_self(self):
        val_x = self.x.show_self()
        val_y = self.y.show_self()
        ret = val_x + ' < ' + val_y
        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('function', types.CharacterType())

    @staticmethod
    def create(x: RObj, y: RObj):
        call = function.CallObj.create_from_lang_obj(LessObj(x, y))
        return call

    def evaluate(self, env: Environment):
        return self

    def compute(self, env: Environment):
        x, y = self.x.evaluate(env), self.y.evaluate(env)
        func: function.FunctionObj = env.find_function('<')
        new_env = arrange_params_with_function_args([function.Param('x', x), function.Param('y', y)], func, env)
        ret = func.compute(new_env)
        return ret


@RObj.register_r_obj
class LessOrEqualObj(RObj):
    def __init__(self, x: RObj, y: RObj):
        super(LessOrEqualObj, self).__init__(types.BuiltInType())
        self.x = x
        self.y = y

    def show_self(self):
        val_x = self.x.show_self()
        val_y = self.y.show_self()
        ret = val_x + ' <= ' + val_y
        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('function', types.CharacterType())

    @staticmethod
    def create(x: RObj, y: RObj):
        call = function.CallObj.create_from_lang_obj(LessOrEqualObj(x, y))
        return call

    def evaluate(self, env: Environment):
        return self

    def compute(self, env: Environment):
        x, y = self.x.evaluate(env), self.y.evaluate(env)
        func: function.FunctionObj = env.find_function('<=')
        new_env = arrange_params_with_function_args([function.Param('x', x), function.Param('y', y)], func, env)
        ret = func.compute(new_env)
        return ret


@RObj.register_r_obj
class AddObj(RObj):
    def __init__(self, e1: RObj, e2: RObj):
        super(AddObj, self).__init__(types.BuiltInType())
        self.e1 = e1
        self.e2 = e2

    def show_self(self):
        val_e1 = self.e1.show_self()
        val_e2 = self.e2.show_self()
        ret = val_e1 + ' + ' + val_e2
        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('function', types.CharacterType())

    @staticmethod
    def create(e1: RObj, e2: RObj):
        call = function.CallObj.create_from_lang_obj(AddObj(e1, e2))
        return call

    def evaluate(self, env: Environment):
        return self

    def compute(self, env: Environment):
        e1, e2 = self.e1.evaluate(env), self.e2.evaluate(env)
        func: function.FunctionObj = env.find_function('+')
        new_env = arrange_params_with_function_args([function.Param('e1', e1), function.Param('e2', e2)], func, env)
        ret = func.compute(new_env)
        return ret


@RObj.register_r_obj
class AddUnaryObj(RObj):
    def __init__(self, e: RObj):
        super(AddUnaryObj, self).__init__(types.BuiltInType())
        self.e = e

    def show_self(self):
        val_e = self.e.show_self()
        ret = '+' + val_e
        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('function', types.CharacterType())

    @staticmethod
    def create(e: RObj):
        call = function.CallObj.create_from_lang_obj(AddUnaryObj(e))
        return call

    def evaluate(self, env: Environment):
        return self

    def compute(self, env: Environment):
        e = self.e.evaluate(env)
        func: function.FunctionObj = env.find_function('+')
        new_env = arrange_params_with_function_args([function.Param('e1', e)], func, env)
        ret = func.compute(new_env)
        return ret


@RObj.register_r_obj
class SubtractObj(RObj):
    def __init__(self, e1: RObj, e2: RObj):
        super(SubtractObj, self).__init__(types.BuiltInType())
        self.e1 = e1
        self.e2 = e2

    def show_self(self):
        val_e1 = self.e1.show_self()
        val_e2 = self.e2.show_self()
        ret = val_e1 + ' - ' + val_e2
        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('function', types.CharacterType())

    @staticmethod
    def create(e1: RObj, e2: RObj):
        call = function.CallObj.create_from_lang_obj(SubtractObj(e1, e2))
        return call

    def evaluate(self, env: Environment):
        return self

    def compute(self, env: Environment):
        e1, e2 = self.e1.evaluate(env), self.e2.evaluate(env)
        func: function.FunctionObj = env.find_function('-')
        new_env = arrange_params_with_function_args([function.Param('e1', e1), function.Param('e2', e2)], func, env)
        ret = func.compute(new_env)
        return ret


@RObj.register_r_obj
class SubtractUnaryObj(RObj):
    def __init__(self, e: RObj):
        super(SubtractUnaryObj, self).__init__(types.BuiltInType())
        self.e = e

    def show_self(self):
        val_e = self.e.show_self()
        ret = '-' + val_e
        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('function', types.CharacterType())

    @staticmethod
    def create(e: RObj):
        call = function.CallObj.create_from_lang_obj(SubtractUnaryObj(e))
        return call

    def evaluate(self, env: Environment):
        return self

    def compute(self, env: Environment):
        e = self.e.evaluate(env)
        func: function.FunctionObj = env.find_function('-')
        new_env = arrange_params_with_function_args([function.Param('e1', e)], func, env)
        ret = func.compute(new_env)
        return ret


@RObj.register_r_obj
class MultiplyObj(RObj):
    def __init__(self, e1: RObj, e2: RObj):
        super(MultiplyObj, self).__init__(types.BuiltInType())
        self.e1 = e1
        self.e2 = e2

    def show_self(self):
        val_e1 = self.e1.show_self()
        val_e2 = self.e2.show_self()
        ret = val_e1 + ' * ' + val_e2
        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('function', types.CharacterType())

    @staticmethod
    def create(e1: RObj, e2: RObj):
        call = function.CallObj.create_from_lang_obj(MultiplyObj(e1, e2))
        return call

    def evaluate(self, env: Environment):
        return self

    def compute(self, env: Environment):
        e1, e2 = self.e1.evaluate(env), self.e2.evaluate(env)
        func: function.FunctionObj = env.find_function('*')
        new_env = arrange_params_with_function_args([function.Param('e1', e1), function.Param('e2', e2)], func, env)
        ret = func.compute(new_env)
        return ret


@RObj.register_r_obj
class DivideObj(RObj):
    def __init__(self, e1: RObj, e2: RObj):
        super(DivideObj, self).__init__(types.BuiltInType())
        self.e1 = e1
        self.e2 = e2

    def show_self(self):
        val_e1 = self.e1.show_self()
        val_e2 = self.e2.show_self()
        ret = val_e1 + ' / ' + val_e2
        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('function', types.CharacterType())

    @staticmethod
    def create(e1: RObj, e2: RObj):
        call = function.CallObj.create_from_lang_obj(DivideObj(e1, e2))
        return call

    def evaluate(self, env: Environment):
        return self

    def compute(self, env: Environment):
        e1, e2 = self.e1.evaluate(env), self.e2.evaluate(env)
        func: function.FunctionObj = env.find_function('/')
        new_env = arrange_params_with_function_args([function.Param('e1', e1), function.Param('e2', e2)], func, env)
        ret = func.compute(new_env)
        return ret


@RObj.register_r_obj
class SpecialObj(RObj):
    def __init__(self, e1: RObj, e2: RObj, op_name):
        super(SpecialObj, self).__init__(types.BuiltInType())
        self.e1 = e1
        self.e2 = e2
        self.op_name = op_name

    def show_self(self):
        val_e1 = self.e1.show_self()
        val_e2 = self.e2.show_self()
        ret = val_e1 + ' {} '.format(self.op_name) + val_e2
        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('function', types.CharacterType())

    @staticmethod
    def create(e1: RObj, e2: RObj, op_name):
        call = function.CallObj.create_from_lang_obj(SpecialObj(e1, e2, op_name))
        return call

    def evaluate(self, env: Environment):
        return self

    def compute(self, env: Environment):
        e1, e2 = self.e1.evaluate(env), self.e2.evaluate(env)
        func: function.FunctionObj = env.find_function(self.op_name)
        new_env = arrange_params_with_function_args([function.Param('e1', e1), function.Param('e2', e2)], func, env)
        ret = func.compute(new_env)
        return ret


@RObj.register_r_obj
class SequenceObj(RObj):
    def __init__(self, e1: RObj, e2: RObj):
        super(SequenceObj, self).__init__(types.BuiltInType())
        self.e1 = e1
        self.e2 = e2

    def show_self(self):
        val_e1 = self.e1.show_self()
        val_e2 = self.e2.show_self()
        ret = val_e1 + ':' + val_e2
        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('function', types.CharacterType())

    @staticmethod
    def create(e1: RObj, e2: RObj):
        call = function.CallObj.create_from_lang_obj(SequenceObj(e1, e2))
        return call

    def evaluate(self, env: Environment):
        return self

    def compute(self, env: Environment):
        e1, e2 = self.e1.evaluate(env), self.e2.evaluate(env)
        func: function.FunctionObj = env.find_function(':')
        new_env = arrange_params_with_function_args([function.Param('e1', e1), function.Param('e2', e2)], func, env)
        ret = func.compute(new_env)
        return ret


@RObj.register_r_obj
class PowerObj(RObj):
    def __init__(self, e1: RObj, e2: RObj):
        super(PowerObj, self).__init__(types.BuiltInType())
        self.e1 = e1
        self.e2 = e2

    def show_self(self):
        val_e1 = self.e1.show_self()
        val_e2 = self.e2.show_self()
        ret = val_e1 + '^' + val_e2
        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('function', types.CharacterType())

    @staticmethod
    def create(e1: RObj, e2: RObj):
        return function.CallObj.create_from_lang_obj(PowerObj(e1, e2))

    def evaluate(self, env: Environment):
        return self

    def compute(self, env: Environment):
        e1, e2 = self.e1.evaluate(env), self.e2.evaluate(env)
        func: function.FunctionObj = env.find_function('^')
        new_env = arrange_params_with_function_args([function.Param('e1', e1), function.Param('e2', e2)], func, env)
        ret = func.compute(new_env)
        return ret


@RObj.register_r_obj
class SuiteObj(RObj):
    def __init__(self, items):
        super(SuiteObj, self).__init__(types.LanguageType())
        self.items: List[RObj] = items

    def show_self(self):
        res = []
        for item in self.items:
            r = item.show_self()
            res.append('    ' + r)
        ret = '{' + '\n'.join(res) + '}'

        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('{', types.CharacterType())

    @staticmethod
    def create(items):
        return SuiteObj(items)

    def evaluate(self, env: Environment):
        last = atomics.NULLObj()
        for item in self.items:
            last = execute_item(item, env)
        return last


@RObj.register_r_obj
class NextObj(RObj):
    def __init__(self):
        super(NextObj, self).__init__(types.LanguageType())

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('call', types.CharacterType())

    def show_self(self, *args, **kwargs):
        return 'next'

    show_self_for_print = show_self

    @staticmethod
    def create(*args, **kwargs):
        return NextObj()

    def evaluate(self, env: Environment):
        raise NextLoopCommand()


@RObj.register_r_obj
class BreakObj(RObj):
    def __init__(self):
        super(BreakObj, self).__init__(types.LanguageType())

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('call', types.CharacterType())

    def show_self(self, *args, **kwargs):
        return 'break'

    show_self_for_print = show_self

    @staticmethod
    def create(*args, **kwargs):
        return BreakObj()

    def evaluate(self, env: Environment):
        raise BreakLoopCommand()

@RObj.register_r_obj
class IfElseObj(RObj):
    def __init__(self, argument, body, alterbody):
        super(IfElseObj, self).__init__(types.LanguageType())
        self.argument = argument
        self.body = body
        self.alterbody = alterbody

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('if', types.CharacterType())

    def show_self(self, *args, **kwargs):
        val_arg = self.argument.show_self()
        val_body = self.body.show_self()
        val_alterbody = self.alterbody.show_self() if self.alterbody is not None else None
        res = 'if ('+val_arg+')' + (val_body if isinstance(self.body, RObj.get_r_obj('SuiteObj')) else ' {}'.format(val_body)) + \
              ('' if val_alterbody is None else ('\nelse ' (val_alterbody if isinstance(self.alterbody, RObj.get_r_obj('SuiteObj')) else ' {}'.format(val_alterbody))))
        return res

    show_self_for_print = show_self

    @staticmethod
    def create(argument, body, alterbody):
        return IfElseObj(argument, body, alterbody)

    def evaluate(self, env: Environment):
        val_arg: RObj = self.argument.evaluate(env)
        if val_arg.get_type().name not in ['double', 'numeric', 'logical']:
            raise errors.ArgNotInterpretableAsLogical()
        else:
            if isinstance(val_arg, atomics.VectorObj):
                if len(val_arg.items) == 0:
                    raise RError.create_simple(self, 'argument is of length zero')

            r = as_boolean(val_arg)
            if r:
                ret = execute_item(self.body, env)
                return ret
            else:
                if self.alterbody is not None:
                    ret = execute_item(self.alterbody, env)
                    return ret
                else:
                    return atomics.NULLObj()


@RObj.register_r_obj
class WhileObj(RObj):
    def __init__(self, argument, body):
        super(WhileObj, self).__init__(types.LanguageType())
        self.argument: RObj = argument
        self.body: RObj = body

    @staticmethod
    def create(argument: RObj, body: RObj):
        ret = WhileObj(argument, body)
        return ret

    def show_self(self):
        val_arg = self.argument.show_self()
        val_body = self.body.show_self()
        ret = 'while ('+val_arg+')' + \
              (val_body if isinstance(self.body, RObj.get_r_obj('SuiteObj')) else ' {}'.format(val_body))
        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('while', types.CharacterType())

    def evaluate(self, env: Environment):

        while True:
            val_arg: RObj = self.argument.evaluate(env)
            if val_arg.get_type().name not in ['double', 'numeric', 'logical']:
                raise errors.ArgNotInterpretableAsLogical()
            else:
                if isinstance(val_arg, atomics.VectorObj):
                    if len(val_arg.items) == 0:
                        raise RError.create_simple(self, 'argument is of length zero')

                r = as_boolean(val_arg)
                if r:
                    try:
                        execute_item(self.body, env)
                    except BreakLoopCommand:
                        return atomics.NULLObj()
                    except NextLoopCommand:
                        continue
                else:
                    return atomics.NULLObj()


@RObj.register_r_obj
class ForLoopObj(RObj):
    def __init__(self, argument, iter_item, body):
        super(ForLoopObj, self).__init__(types.LanguageType())
        self.argument: RObj = argument
        self.iter_item: RObj = iter_item
        self.body: RObj = body

    def show_self(self):
        val_arg = self.argument.show_self()
        val_iter = self.iter_item.show_self()
        val_body = self.body.show_self()

        ret = 'for (' + val_arg + ' in ' + val_iter + ')' +\
              (val_body if isinstance(self.body, RObj.get_r_obj('SuiteObj')) else ' {}'.format(val_body))
        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('for', types.CharacterType())

    @staticmethod
    def create(argument, iter_item, body):
        return ForLoopObj(argument, iter_item, body)

    def evaluate(self, env: Environment):
        val_iter:RObj = self.iter_item.evaluate(env)
        items: List[RObj] = val_iter.get_items()

        if self.argument.get_type().name != 'symbol':
            raise Exception('unexpected for loop argument type - {}'.format(self.argument.get_type().name))
        for item in items:
            self.argument.set_value(item, env)
            try:
                execute_item(self.body, env)
            except BreakLoopCommand:
                return atomics.NULLObj()
            except NextLoopCommand:
                continue
        return atomics.NULLObj()


@RObj.register_r_obj
class RepeatLoopObj(RObj):
    def __init__(self, body):
        super(RepeatLoopObj, self).__init__(types.LanguageType())
        self.body: RObj = body

    def show_self(self):
        val_body = self.body.show_self()

        ret = 'repeat' + (val_body if isinstance(self.body, RObj.get_r_obj('SuiteObj'))
                          else ' {}'.format(val_body))
        return ret

    show_self_for_print = show_self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('repeat', types.CharacterType())

    @staticmethod
    def create(body):
        return RepeatLoopObj(body)

    def evaluate(self, env: Environment):
        while True:
            try:
                self.body.evaluate(env)
            except BreakLoopCommand:
                return atomics.NULLObj()
            except NextLoopCommand:
                continue









