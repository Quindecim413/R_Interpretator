from R.Environment import Environment, NextLoopCommand, BreakLoopCommand
from R.RObj import RObj
import R.Types as types
import R.RuntimeErrors as errors
import R.AtomicObjs as atomics
import R.Function as function
from typing import List


def init_if_atomic(maybe_atomic):
    if isinstance(maybe_atomic, RObj.get_r_obj('Atomic')):
        ret = RObj.get_r_obj('VectorObj')([atomics.VectorItem(None, maybe_atomic)])
        return ret
    else:
        return maybe_atomic


@RObj.register_r_obj
class AssignObj(RObj):
    def __init__(self, item, value, mode):
        super(AssignObj, self).__init__(types.LanguageType())
        self.item: RObj = item
        self.value: RObj = value
        self.mode = mode

    def show_self(self):
        pass

    @staticmethod
    def create(item, value, mode: str):
        if mode not in ['plain', 'simple', 'super']:
            raise Exception('Invalid assignment mode - \"{}\"'.format(mode))
        return AssignObj(item, value, mode)

    @staticmethod
    def init_if_atomic(maybe_atomic):
        return init_if_atomic(maybe_atomic)

    def evaluate(self, env: Environment):
        if self.mode == 'super':
            env = env.global_env
            if self.item.get_type().name == 'symbol':
                val_value: RObj = self.init_if_atomic(self.value.evaluate(env))
                name = self.item.name
                env.add(name, val_value)
                return val_value
            elif isinstance(self.item, RObj.get_r_obj('Atomic')):
                if self.item.get_type().name == "character":
                    name = self.item.value
                    val_value: RObj = self.init_if_atomic(self.value.evaluate(env))
                    env.add(name, val_value)
                    return val_value
                else:
                    raise errors.InvalidLeftHandAssignment()
            else:
                val_value: RObj = self.init_if_atomic(self.value.evaluate(env))
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
                val_value: RObj = self.init_if_atomic(self.value.evaluate(env))
                name = self.item.name
                env.add(name, val_value)
                return val_value
            elif isinstance(self.item, RObj.get_r_obj('Atomic')):
                if self.item.get_type().name == "character":
                    name = self.item.value
                    val_value: RObj = self.init_if_atomic(self.value.evaluate(env))
                    env.add(name, val_value)
                    return val_value
                else:
                    raise errors.InvalidLeftHandAssignment()
            else:
                val_value: RObj = self.init_if_atomic(self.value.evaluate(env))
                ret = self.item.set_value(val_value, env)
                return ret


@RObj.register_r_obj
class AndObj(RObj):
    def __init__(self, x: RObj, y: RObj):
        super(AndObj, self).__init__(types.BuiltInType())
        self.x = x
        self.y = y

    def show_self(self):
        pass

    @staticmethod
    def create(x: RObj, y: RObj):
        return AndObj(x, y)

    def evaluate(self, env: Environment):
        x, y = init_if_atomic(self.x.evaluate(env)), init_if_atomic(self.y.evaluate(env))
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
        pass

    @staticmethod
    def create(x: RObj, y: RObj):
        return AndAndObj(x, y)

    def evaluate(self, env: Environment):
        x, y = init_if_atomic(self.x.evaluate(env)), init_if_atomic(self.y.evaluate(env))
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
        pass

    @staticmethod
    def create(x: RObj, y: RObj):
        return OrObj(x, y)

    def evaluate(self, env: Environment):
        x, y = init_if_atomic(self.x.evaluate(env)), init_if_atomic(self.y.evaluate(env))
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
        pass

    @staticmethod
    def create(x: RObj, y: RObj):
        return OrOrObj(x, y)

    def evaluate(self, env: Environment):
        x, y = init_if_atomic(self.x.evaluate(env)), init_if_atomic(self.y.evaluate(env))
        func: function.FunctionObj = env.find_function('||')
        ret = func.compute([function.Param('x', x), function.Param('y', y)], env)
        return ret


@RObj.register_r_obj
class NotObj(RObj):
    def __init__(self, x: RObj):
        super(NotObj, self).__init__(types.BuiltInType())
        self.x = x

    def show_self(self):
        pass

    @staticmethod
    def create(x: RObj):
        return NotObj(x)

    def evaluate(self, env: Environment):
        x, y = init_if_atomic(self.x.evaluate(env)), init_if_atomic(self.y.evaluate(env))
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
        pass

    @staticmethod
    def create(e1: RObj, e2: RObj):
        return AddObj(e1, e2)

    def evaluate(self, env: Environment):
        e1, e2 = init_if_atomic(self.e1.evaluate(env)), init_if_atomic(self.e2.evaluate(env))
        func: function.FunctionObj = env.find_function('+')
        ret = func.compute([function.Param('e1', e1), function.Param('e2', e2)], env)
        return ret


@RObj.register_r_obj
class AddUnaryObj(RObj):
    def __init__(self, e1: RObj):
        super(AddUnaryObj, self).__init__(types.BuiltInType())
        self.e1 = e1

    def show_self(self):
        pass

    @staticmethod
    def create(e1: RObj):
        return AddUnaryObj(e1)

    def evaluate(self, env: Environment):
        e1 = init_if_atomic(self.e1.evaluate(env))
        func: function.FunctionObj = env.find_function('+')
        ret = func.compute([function.Param('e1', e1)], env)
        return ret


@RObj.register_r_obj
class SubtractObj(RObj):
    def __init__(self, e1: RObj, e2: RObj):
        super(SubtractObj, self).__init__(types.BuiltInType())
        self.e1 = e1
        self.e2 = e2

    def show_self(self):
        pass

    @staticmethod
    def create(e1: RObj, e2: RObj):
        return SubtractObj(e1, e2)

    def evaluate(self, env: Environment):
        e1, e2 = init_if_atomic(self.e1.evaluate(env)), init_if_atomic(self.e2.evaluate(env))
        func: function.FunctionObj = env.find_function('-')
        ret = func.compute([function.Param('e1', e1), function.Param('e2', e2)], env)
        return ret


@RObj.register_r_obj
class SubtractUnaryObj(RObj):
    def __init__(self, e1: RObj):
        super(SubtractUnaryObj, self).__init__(types.BuiltInType())
        self.e1 = e1

    def show_self(self):
        pass

    @staticmethod
    def create(e1: RObj):
        return SubtractUnaryObj(e1)

    def evaluate(self, env: Environment):
        e1, e2 = init_if_atomic(self.e1.evaluate(env)), init_if_atomic(self.e2.evaluate(env))
        func: function.FunctionObj = env.find_function('-')
        ret = func.compute([function.Param('e1', e1)], env)
        return ret

@RObj.register_r_obj
class MultiplyObj(RObj):
    def __init__(self, e1: RObj, e2: RObj):
        super(MultiplyObj, self).__init__(types.BuiltInType())
        self.e1 = e1
        self.e2 = e2

    def show_self(self):
        pass

    @staticmethod
    def create(e1: RObj, e2: RObj):
        return MultiplyObj(e1, e2)

    def evaluate(self, env: Environment):
        e1, e2 = init_if_atomic(self.e1.evaluate(env)), init_if_atomic(self.e2.evaluate(env))
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
        pass

    @staticmethod
    def create(e1: RObj, e2: RObj):
        return DivideObj(e1, e2)

    def evaluate(self, env: Environment):
        e1, e2 = init_if_atomic(self.e1.evaluate(env)), init_if_atomic(self.e2.evaluate(env))
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
        pass

    @staticmethod
    def create(e1: RObj, e2: RObj, op_name):
        return SpecialObj(e1, e2, op_name)

    def evaluate(self, env: Environment):
        e1, e2 = init_if_atomic(self.e1.evaluate(env)), init_if_atomic(self.e2.evaluate(env))
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
        pass

    @staticmethod
    def create(e1: RObj, e2: RObj, op_name):
        return SequenceObj(e1, e2, op_name)

    def evaluate(self, env: Environment):
        e1, e2 = init_if_atomic(self.e1.evaluate(env)), init_if_atomic(self.e2.evaluate(env))
        func: function.FunctionObj = env.find_function(':')
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
        pass

    def evaluate(self, env: Environment):
        pass






