from R.Environment import Environment, NextLoopCommand, BreakLoopCommand
from R.RObj import RObj, RError
import R.Types as types
import R.RuntimeErrors as errors
import R.AtomicObjs as atomics
import R.Function as function
from typing import List
from R.Atomics import *


# def init_if_atomic(maybe_atomic):
#     if isinstance(maybe_atomic, RObj.get_r_obj('Atomic')):
#         ret = RObj.get_r_obj('VectorObj')([atomics.VectorItem(None, maybe_atomic)])
#         return ret
#     else:
#         return maybe_atomic


@RObj.register_r_obj
class AssignObj(RObj):
    def __init__(self, item, value, mode):
        super(AssignObj, self).__init__(types.LanguageType())
        self.item: RObj = item
        self.value: RObj = value
        self.mode = mode

    def show_self(self):
        val_item = self.item.show_self()
        val_val = self.show_self()

        val_op = ' = ' if self.mode == 'plain' else ( ' <- ' if self.mode == 'simple' else ' <<- ')

        ret = val_item + val_op + val_val
        return ret

    show_self_for_print = show_self

    @staticmethod
    def create(item, value, mode: str):
        if mode not in ['plain', 'simple', 'super']:
            raise Exception('Invalid assignment mode - \"{}\"'.format(mode))
        return AssignObj(item, value, mode)


    def evaluate(self, env: Environment):
        if self.mode == 'super':
            env = env.global_env
            if self.item.get_type().name == 'symbol':
                val_value: RObj = self.value.evaluate(env)
                name = self.item.name
                env.add(name, val_value)
                return val_value
            elif isinstance(self.item, RObj.get_r_obj('Atomic')):
                if self.item.get_type().name == "character":
                    name = self.item.value
                    val_value: RObj = self.value.evaluate(env)
                    env.add(name, val_value)
                    return val_value
                else:
                    raise errors.InvalidLeftHandAssignment()
            else:
                val_value: RObj = self.value.evaluate(env)
                ret = self.item.set_value(val_value, env)
                return ret
            # if env == env.global_env:
            #     if self.item.get_type().name == 'symbol':
            #         val_value: RObj = self.init_if_atomic(self.value.evaluate(env))
            #         name = self.item.name
            #         env.add(name, val_value)
            #         return val_value
            #     elif isinstance(self.item, RObj.get_r_obj('Atomic')):
            #         if self.item.get_type().name == "character":
            #             name = self.item.value
            #             val_value: RObj = self.init_if_atomic(self.value.evaluate(env))
            #             env.add(name, val_value)
            #             return val_value
            #         else:
            #             raise errors.InvalidLeftHandAssignment()
            #     else:
            #         val_value: RObj = self.init_if_atomic(self.value.evaluate(env))
            #         ret = self.item.set_value(val_value, env)
            #         return ret
            # else:
            #     if self.item.get_type().name == 'symbol':
            #         val_value: RObj = self.init_if_atomic(self.value.evaluate(env))
            #         name = self.item.name
            #         env.add(name, val_value)
            #         env.global_env.add(name, val_value)
            #         return val_value
            #     elif isinstance(self.item, RObj.get_r_obj('Atomic')):
            #         if self.item.get_type().name == "character":
            #             name = self.item.value
            #             val_value: RObj = self.init_if_atomic(self.value.evaluate(env))
            #             env.add(name, val_value)
            #             env.global_env.add(name, val_value)
            #             return val_value
            #         else:
            #             raise errors.InvalidLeftHandAssignment()
            #     else:
            #         raise errors.InvalidLeftHandAssignment()
        else:
            if self.item.get_type().name == 'symbol':
                val_value: RObj = self.value.evaluate(env)
                name = self.item.name
                env.add(name, val_value)
                return val_value
            elif isinstance(self.item, RObj.get_r_obj('Atomic')):
                if self.item.get_type().name == "character":
                    name = self.item.value
                    val_value: RObj = self.value.evaluate(env)
                    env.add(name, val_value)
                    return val_value
                else:
                    raise errors.InvalidLeftHandAssignment()
            else:
                val_value: RObj = self.value.evaluate(env)
                ret = self.item.set_value(val_value, env)
                return ret


@RObj.register_r_obj
class AndObj(RObj):
    def __init__(self, x: RObj, y: RObj):
        super(AndObj, self).__init__(types.BuiltInType())
        self.x: RObj = x
        self.y: RObj = y

    def show_self(self):
        val_x = self.x.show_self()
        val_y = self.y.show_self()
        ret = val_x + ' & ' + val_y
        return ret

    show_self_for_print = show_self

    @staticmethod
    def create(x: RObj, y: RObj):
        return AndObj(x, y)

    def evaluate(self, env: Environment):
        x, y = self.x.evaluate(env), self.y.evaluate(env)
        func: function.FunctionObj = env.find_function('&')
        ret = func.compute([function.Param('x', x), function.Param('y', y)], env)
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

    @staticmethod
    def create(x: RObj, y: RObj):
        return AndAndObj(x, y)

    def evaluate(self, env: Environment):
        x, y = self.x.evaluate(env), self.y.evaluate(env)
        func: function.FunctionObj = env.find_function('&&')
        ret = func.compute([function.Param('x', x), function.Param('y', y)], env)
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

    @staticmethod
    def create(x: RObj, y: RObj):
        return OrObj(x, y)

    def evaluate(self, env: Environment):
        x, y = self.x.evaluate(env), self.y.evaluate(env)
        func: function.FunctionObj = env.find_function('|')
        ret = func.compute([function.Param('x', x), function.Param('y', y)], env)
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

    @staticmethod
    def create(x: RObj, y: RObj):
        return OrOrObj(x, y)

    def evaluate(self, env: Environment):
        x, y = self.x.evaluate(env), self.y.evaluate(env)
        func: function.FunctionObj = env.find_function('||')
        ret = func.compute([function.Param('x', x), function.Param('y', y)], env)
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

    @staticmethod
    def create(x: RObj):
        return NotObj(x)

    def evaluate(self, env: Environment):
        x, y = self.x.evaluate(env), self.y.evaluate(env)
        func: function.FunctionObj = env.find_function('!')
        ret = func.compute([function.Param('x', x)], env)
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

    @staticmethod
    def create(e1: RObj, e2: RObj):
        return AddObj(e1, e2)

    def evaluate(self, env: Environment):
        e1, e2 = self.e1.evaluate(env), self.e2.evaluate(env)
        func: function.FunctionObj = env.find_function('+')
        ret = func.compute([function.Param('e1', e1), function.Param('e2', e2)], env)
        return ret


@RObj.register_r_obj
class AddUnaryObj(RObj):
    def __init__(self, e: RObj):
        super(AddUnaryObj, self).__init__(types.BuiltInType())
        self.e = e

    def show_self(self):
        val_e = self.e1.show_self()
        ret = '+' + val_e
        return ret

    show_self_for_print = show_self

    @staticmethod
    def create(e: RObj):
        return AddUnaryObj(e)

    def evaluate(self, env: Environment):
        e = self.e.evaluate(env)
        func: function.FunctionObj = env.find_function('+')
        ret = func.compute([function.Param('e1', e)], env)
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

    @staticmethod
    def create(e1: RObj, e2: RObj):
        return SubtractObj(e1, e2)

    def evaluate(self, env: Environment):
        e1, e2 = self.e1.evaluate(env), self.e2.evaluate(env)
        func: function.FunctionObj = env.find_function('-')
        ret = func.compute([function.Param('e1', e1), function.Param('e2', e2)], env)
        return ret


@RObj.register_r_obj
class SubtractUnaryObj(RObj):
    def __init__(self, e: RObj):
        super(SubtractUnaryObj, self).__init__(types.BuiltInType())
        self.e = e

    def show_self(self):
        val_e = self.e1.show_self()
        ret = '-' + val_e
        return ret

    show_self_for_print = show_self

    @staticmethod
    def create(e: RObj):
        return SubtractUnaryObj(e)

    def evaluate(self, env: Environment):
        e = self.e.evaluate(env)
        func: function.FunctionObj = env.find_function('-')
        ret = func.compute([function.Param('e1', e)], env)
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

    @staticmethod
    def create(e1: RObj, e2: RObj):
        return MultiplyObj(e1, e2)

    def evaluate(self, env: Environment):
        e1, e2 = self.e1.evaluate(env), self.e2.evaluate(env)
        func: function.FunctionObj = env.find_function('*')
        ret = func.compute([function.Param('e1', e1), function.Param('e2', e2)], env)
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

    @staticmethod
    def create(e1: RObj, e2: RObj):
        return DivideObj(e1, e2)

    def evaluate(self, env: Environment):
        e1, e2 = self.e1.evaluate(env), self.e2.evaluate(env)
        func: function.FunctionObj = env.find_function('/')
        ret = func.compute([function.Param('e1', e1), function.Param('e2', e2)], env)
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

    @staticmethod
    def create(e1: RObj, e2: RObj, op_name):
        return SpecialObj(e1, e2, op_name)

    def evaluate(self, env: Environment):
        e1, e2 = self.e1.evaluate(env), self.e2.evaluate(env)
        func: function.FunctionObj = env.find_function(self.op_name)
        ret = func.compute([function.Param('e1', e1), function.Param('e2', e2)], env)
        return ret


@RObj.register_r_obj
class SequenceObj(RObj):
    def __init__(self, e1: RObj, e2: RObj, op_name):
        super(SequenceObj, self).__init__(types.BuiltInType())
        self.e1 = e1
        self.e2 = e2
        self.op_name = op_name

    def show_self(self):
        val_e1 = self.e1.show_self()
        val_e2 = self.e2.show_self()
        ret = val_e1 + ':' + val_e2
        return ret

    show_self_for_print = show_self

    @staticmethod
    def create(e1: RObj, e2: RObj, op_name):
        return SequenceObj(e1, e2, op_name)

    def evaluate(self, env: Environment):
        e1, e2 = self.e1.evaluate(env), self.e2.evaluate(env)
        func: function.FunctionObj = env.find_function(':')
        ret = func.compute([function.Param('e1', e1), function.Param('e2', e2)], env)
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

    @staticmethod
    def create(e1: RObj, e2: RObj, op_name):
        return SequenceObj(e1, e2, op_name)

    def evaluate(self, env: Environment):
        e1, e2 = self.e1.evaluate(env), self.e2.evaluate(env)
        func: function.FunctionObj = env.find_function('^')
        ret = func.compute([function.Param('e1', e1), function.Param('e2', e2)], env)
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

    def create(self, items):
        return SuiteObj(items)

    def evaluate(self, env: Environment):
        last = atomics.NULLObj()
        for item in self.items:
            last = item.evaluate(env)
        return last


@RObj.register_r_obj
class WhileObj(RObj):
    def __init__(self, argument, body):
        super(WhileObj, self).__init__(types.LanguageType())
        self.argument: RObj = argument
        self.body: RObj = body

    @staticmethod
    def create(self, argument: RObj, body: RObj):
        ret = WhileObj(argument, body)
        return ret

    def show_self(self):
        val_arg = self.argument.show_self()
        val_body = self.body.show_self()
        ret = 'while ('+val_arg+')' + \
              (val_body if isinstance(self.body, RObj.get_r_obj('SuiteObj')) else ' {}'.format(val_body))
        return ret

    show_self_for_print = show_self

    def evaluate(self, env: Environment):
        while True:
            val_arg: RObj = self.argument.evaluate()
            if val_arg.get_type().name not in ['double', 'numeric', 'logical']:
                raise errors.ArgNotInterpretableAsLogical()
            else:
                if isinstance(val_arg, atomics.VectorObj):
                    if len(val_arg.items) == 0:
                        raise RError(self, 'argument is of length zero')

                r = as_boolean(val_arg)
                if r:
                    try:
                        self.body.evaluate(env)
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
                self.body.evaluate(env)
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









