from typing import List
from abc import abstractmethod
import R.Types as types

from R.Environment import Environment
from R.Function import FunctionObj, RObj, Arg, DotsObj, Param
from R.AtomicObjs import ListItem, ListObj, VectorObj, VectorItem, EmptyParamObj, NULLObj
import R.RuntimeErrors as errors
from R.Atomics import *


built_in_env: Environment = Environment(None)


class BuiltInFun(FunctionObj):
    def __init__(self, name, input_args):
        super(BuiltInFun, self).__init__(input_args, None)
        self._type = types.BuiltInType()
        self.name = name

    @staticmethod
    @abstractmethod
    def create(*args):
        pass

    @abstractmethod
    def compute(self, env: Environment):
        pass


def cast_vector_items(items, python_type, r_type):
    ret = [VectorItem(item[0], Atomic(python_type(item[1].value), r_type())) for item in items]
    return ret


def register_built_in_function(cls):
    fun = cls.create()
    built_in_env.add(fun.name, fun)
    return  cls


def concat_vectors(v1, v2):
    v1_len = len(v1)
    v2_len = len(v2)

    if v1_len > v2_len:
        res = []
        times = v1_len // v2_len
        more = v1_len - v2_len*times
        for i in range(times):
            res.extend(v2)
        res.extend(v2[:more])
        ret = list(zip(v1, res))
        return ret
    else:
        res = []
        times = v2_len // v1_len
        more = v2_len - v1_len*times
        for i in range(times):
            res.extend(v1)
        res.extend(v1[:more])
        ret = list(zip(res, v2))
        return ret


@RObj.register_r_obj
class ArrowDefaultAssignFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = '<-'
        args = [Arg('x', None), Arg('value', None)]
        return ArrowDefaultAssignFun(name, args)

    def compute(self, env: Environment):
        try:
            x: RObj = env.find_object_locally('x')
        except:
            raise errors.InvalidLeftHandAssignment()
        try:
            value: RObj = env.find_object_locally('value')
        except:
            raise errors.InvalidLeftHandAssignment()

        if x.get_type().name == 'symbol':
            val_value = value.evaluate(env)
            if val_value.get_type().name == 'call':
                val_value = val_value.compute(env)
            env.parent_env.add(x.name, val_value)
            return val_value
        raise errors.InvalidLeftHandAssignment()


register_built_in_function(ArrowDefaultAssignFun)


@RObj.register_r_obj
class VectorFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = 'c'
        args = [Arg('...', None)]
        return VectorFun(name, args)

    def compute(self, env: Environment):
        dots: DotsObj = env.find_object('...')

        if dots.get_type().name == 'NULL':
            return NULLObj()

        items = dots.items
        if len(items) == 0:
            return NULLObj()

        items_types = set(map(lambda i: i[1].get_type().name, items))
        casts = ['list', 'character', 'double', 'integer', 'logical']
        if set(casts).issubset(items_types):
            list_fun: FunctionObj = built_in_env.find_function('list')
            ret = list_fun.compute(env)
            return ret

        flat_items = []
        for item in items:
            if isinstance(item[1], Atomic):
                flat_items.append(VectorItem(item[0], item[1]))
            elif isinstance(item[1], VectorObj):
                flat_items.extend(item[1].items)
            else:
                raise Exception('Invalid item in c function - {}'.format(item))

        if 'character' in items_types:
            if len(items_types) > 1:
                flat_items = cast_vector_items(flat_items, str, types.CharacterType)
        elif 'double' in items_types:
            if len(items_types) > 1:
                flat_items = cast_vector_items(flat_items, float, types.DoubleType)
        elif 'integer' in items_types:
            if len(items_types) > 1:
                flat_items = cast_vector_items(flat_items, int, types.IntegerType)
        elif 'logical' in items_types:
            if len(items_types) > 1:
                flat_items = cast_vector_items(flat_items, bool, types.LogicalType)
        else:
            raise Exception("unknown vector type in types - {}".format(items_types))

        return VectorObj.create(flat_items)


register_built_in_function(VectorFun)


@RObj.register_r_obj
class CharacterFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = 'character'
        args = [Arg('length', Atomic(0, types.IntegerType()))]
        return CharacterFun(name, args)

    def compute(self, env: Environment):
        ln: VectorObj = env.find_object('length')
        if ln.get_type().name not in ['double', 'integer']:
            raise errors.InvalidArg('length')

        if len(ln.items) != 1:
            raise errors.InvalidArg('length')

        val = ln.items[0][1]

        if val.is_inf:
            raise errors.R_RuntimeError('vector size cannot be infinite')
        elif val.is_na:
            raise errors.InvalidArg('length')
        elif val.is_nan:
            raise errors.R_RuntimeError('vector size cannot be NA/NaN')

        count = val.value

        items = [VectorItem(None, Atomic('', types.CharacterType())) for _ in range(int(count) * (-1 if val.is_neg else 1))]

        ret = VectorObj(items, types.CharacterType())
        return ret


register_built_in_function(CharacterFun)


@RObj.register_r_obj
class NumericFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = 'numeric'
        args = [Arg('length', Atomic(0, types.IntegerType()))]
        return NumericFun(name, args)

    def compute(self, env: Environment):
        ln: VectorObj = env.find_object('length')
        if ln.get_type().name not in ['double', 'integer']:
            raise errors.InvalidArg('length')

        if len(ln.items) != 1:
            raise errors.InvalidArg('length')

        val = ln.items[0][1]

        if val.is_inf:
            raise errors.R_RuntimeError('vector size cannot be infinite')
        elif val.is_na:
            raise errors.InvalidArg('length')
        elif val.is_nan:
            raise errors.R_RuntimeError('vector size cannot be NA/NaN')

        count = val.value

        items = [VectorItem(None, Atomic(0, types.DoubleType())) for _ in range(int(count) * (-1 if val.is_neg else 1))]

        ret = VectorObj(items, types.DoubleType())
        return ret


register_built_in_function(NumericFun)


@RObj.register_r_obj
class IntegerFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = 'integer'
        args = [Arg('length', Atomic(0, types.IntegerType()))]
        return IntegerFun(name, args)

    def compute(self, env: Environment):
        ln: VectorObj = env.find_object('length')
        if ln.get_type().name not in ['double', 'integer']:
            raise errors.InvalidArg('length')

        if len(ln.items) != 1:
            raise errors.InvalidArg('length')

        val = ln.items[0][1]

        if val.is_inf:
            raise errors.R_RuntimeError('vector size cannot be infinite')
        elif val.is_na:
            raise errors.InvalidArg('length')
        elif val.is_nan:
            raise errors.R_RuntimeError('vector size cannot be NA/NaN')

        count = val.value

        items = [VectorItem(None, Atomic(0, types.IntegerType())) for _ in range(int(count) * (-1 if val.is_neg else 1))]

        ret = VectorObj(items, types.IntegerType())
        return ret


register_built_in_function(IntegerFun)


@RObj.register_r_obj
class LogicalFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = 'logical'
        args = [Arg('length', Atomic(0, types.IntegerType()))]
        return LogicalFun(name, args)

    def compute(self, env: Environment):
        ln: VectorObj = env.find_object('length')
        if ln.get_type().name not in ['double', 'integer']:
            raise errors.InvalidArg('length')

        if len(ln.items) != 1:
            raise errors.InvalidArg('length')

        val = ln.items[0][1]

        if val.is_inf:
            raise errors.R_RuntimeError('vector size cannot be infinite')
        elif val.is_na:
            raise errors.InvalidArg('length')
        elif val.is_nan:
            raise errors.R_RuntimeError('vector size cannot be NA/NaN')

        count = val.value

        items = [VectorItem(None, Atomic(False, types.LogicalType())) for _ in range(int(count) * (-1 if val.is_neg else 1))]

        ret = VectorObj(items, types.LogicalType())
        return ret


register_built_in_function(LogicalFun)


@RObj.register_r_obj
class ListFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = 'list'
        args = [Arg('...', None)]
        return ListFun(name, args)

    def compute(self, env: Environment):
        dots: DotsObj = env.find_object('...')
        items = dots.items
        list_items = []
        for item in items:
            itm = ListItem(item.name, item.value)
            list_items.append(itm)
        return ListObj(list_items)


register_built_in_function(ListFun)


def perform_op_on_vector_or_atomic(e1, e2, operation):
    res = []
    if isinstance(e1, Atomic) and not isinstance(e2, Atomic):
        for v in e2.items:
            res.append(operation(e1, v[1]))
    elif not isinstance(e1, Atomic) and isinstance(e2, Atomic):
        for v in e1.items:
            res.append(operation(v, e2[1]))
    elif isinstance(e1, Atomic) and isinstance(e2, Atomic):
        res.append(operation(e1, e2))
    else:
        if len(e1.items) == 0 or len(e2.items) == 0:
            return []
        for l, r in concat_vectors(e1.items, e2.items):
            res.append(operation(l[1], r[1]))
    return res


@RObj.register_r_obj
class AndAndFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = '&&'
        args = [Arg('x', None), Arg('y', None)]
        return AndAndFun(name, args)

    def compute(self, env: Environment):
        e1 = env.find_object('x')
        e2 = env.find_object('y')
        if e1.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('x', 'x && y')
        if e2.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('y', 'x && y')
        try:
            res = perform_op_on_vector_or_atomic(e1, e2, atomic_and)
        except UnsupportedVectorType as e:
            raise errors.InvalidArgTypeInArgs('x' if e.operand_index == 0 else 'y', 'x && y')

        res = [VectorItem(None, el) for el in res]

        ret = VectorObj.create(res)
        return ret


register_built_in_function(AndAndFun)


@RObj.register_r_obj
class AndFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = '&'
        args = [Arg('x', None), Arg('y', None)]
        return AndFun(name, args)

    def compute(self, env: Environment):
        e1: VectorObj = env.find_object('x')
        e2: VectorObj = env.find_object('y')
        if e1.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('x', 'x & y')
        if e2.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('y', 'x & y')
        res = VectorItem(None, atomic_and(e1.items[0][1], e2.items[0][1]))
        ret = VectorObj.create([res])
        return ret


# TODO all above

register_built_in_function(AndFun)


@RObj.register_r_obj
class OrOrFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = '||'
        args = [Arg('x', None), Arg('y', None)]
        return OrOrFun(name, args)

    def compute(self, env: Environment):
        e1 = env.find_object('x')
        e2 = env.find_object('y')
        if e1.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('x', 'x || y')
        if e2.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('y', 'x || y')

        res = perform_op_on_vector_or_atomic(e1, e2, lambda l, r: cast_atomic(atomic_power(l, r)))


        res = [VectorItem(None, el) for el in res]

        ret = VectorObj.create(res)
        return ret


register_built_in_function(OrOrFun)


@RObj.register_r_obj
class OrFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = '|'
        args = [Arg('x', None), Arg('y', None)]
        return OrFun(name, args)

    def compute(self, env: Environment):
        e1 = env.find_object('x')
        e2 = env.find_object('y')
        if e1.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('x', 'x | y')
        if e2.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('y', 'x | y')
        res = VectorItem(None, atomic_or(e1.items[0].value, e2.items[0].value))
        ret = VectorObj.create([res])
        return ret


register_built_in_function(OrFun)


@RObj.register_r_obj
class NotFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = '!'
        args = [Arg('x', None)]
        return NotFun(name, args)

    def compute(self, env: Environment):
        e1 = env.find_object('x')
        if e1.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgType()
        res = []
        if isinstance(e1, VectorObj):
            if len(e1.items) == 0:
                return VectorObj([], type(e1.get_type())())

            for item in e1.items:
                res.append(atomic_not(item[1]))
        else:
            res.append(atomic_not(e1))

        res = [VectorItem(None, el) for el in res]

        ret = VectorObj.create(res)
        return ret


register_built_in_function(NotFun)


@RObj.register_r_obj
class AddFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = '+'
        args = [Arg('e1', None), Arg('e2', None)]
        return AddFun(name, args)

    def compute(self, env: Environment):
        e1 = env.find_object('e1')
        e2 = env.find_object('e2')

        if isinstance(e2, EmptyParamObj):
            return e1.value

        if e1.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('x', 'x + y')
        if e2.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('y', 'x + y')
        res = []

        as_integer = False

        if e1.get_type().name == 'integer' and e2.get_type().name == 'integer':
            as_integer = True
        elif e1.get_type().name == 'integer' and e2.get_type().name == 'logical':
            as_integer = True
        elif e1.get_type().name == 'logical' and e2.get_type().name == 'integer':
            as_integer = True

        res = perform_op_on_vector_or_atomic(e1, e2,
                                             lambda l, r: cast_atomic(atomic_add(l, r),
                                                                      'integer' if as_integer else 'double'))

        res = [VectorItem(None, el) for el in res]

        if len(res) == 0:
            t = get_more_important_vector_type(e1.get_type(), e2.get_type())
            return VectorObj([], t)

        ret = VectorObj.create(res)
        return ret


register_built_in_function(AddFun)


@RObj.register_r_obj
class SubtractFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = '-'
        args = [Arg('e1', None), Arg('e2', None)]
        return SubtractFun(name, args)

    def compute(self, env: Environment):
        e1 = env.find_object('e1')
        e2 = env.find_object('e2')

        if isinstance(e2, EmptyParamObj):
            if e1.get_type().name not in ['double', 'logical', 'integer']:
                raise errors.InvalidArgTypeInArgs('x', '- x')

            res = []
            for item in e1.items:
                res.append(atomic_subtract(Atomic(False, types.LogicalType()), item.value))

            res = [VectorItem(None, el)
                   for el in res]

            ret = VectorObj(res)
            return ret

        if e1.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('x', 'x - y')
        if e2.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('y', 'x - y')

        as_integer = False

        if e1.get_type().name == 'integer' and e2.get_type().name == 'integer':
            as_integer = True
        elif e1.get_type().name == 'integer' and e2.get_type().name == 'logical':
            as_integer = True
        elif e1.get_type().name == 'logical' and e2.get_type().name == 'integer':
            as_integer = True

        res = perform_op_on_vector_or_atomic(e1, e2,
                                             lambda l, r: cast_atomic(atomic_subtract(l, r),
                                                                      'integer' if as_integer else 'double'))

        res = [VectorItem(None, el) for el in res]

        if len(res) == 0:
            t = get_more_important_vector_type(e1.get_type(), e2.get_type())
            return VectorObj([], t)

        ret = VectorObj.create(res)
        return ret


register_built_in_function(SubtractFun)


@RObj.register_r_obj
class MultiplyFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = '*'
        args = [Arg('e1', None), Arg('e2', None)]
        return MultiplyFun(name, args)

    def compute(self, env: Environment):
        e1 = env.find_object('e1')
        e2 = env.find_object('e2')

        if e1[1].get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('x', 'x * y')
        if e2[1].get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('y', 'x * y')

        as_integer = False

        if e1.get_type().name == 'integer' and e2.get_type().name == 'integer':
            as_integer = True
        elif e1.get_type().name == 'integer' and e2.get_type().name == 'logical':
            as_integer = True
        elif e1.get_type().name == 'logical' and e2.get_type().name == 'integer':
            as_integer = True

        res = perform_op_on_vector_or_atomic(e1, e2,
                                             lambda l, r: cast_atomic(atomic_multiply(l, r),
                                                                      'integer' if as_integer else 'double'))

        res = [VectorItem(None, el) for el in res]

        if len(res) == 0:
            t = get_more_important_vector_type(e1.get_type(), e2.get_type())
            return VectorObj([], t)

        ret = VectorObj.create(res)
        return ret


register_built_in_function(MultiplyFun)


@RObj.register_r_obj
class DivideFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = '/'
        args = [Arg('e1', None), Arg('e2', None)]
        return DivideFun(name, args)

    def compute(self, env: Environment):
        e1 = env.find_object('e1')
        e2 = env.find_object('e2')

        if e1.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('x', 'x / y')
        if e2.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('y', 'x / y')

        as_integer = False

        if e1.get_type().name == 'integer' and e2.get_type().name == 'integer':
            as_integer = True
        elif e1.get_type().name == 'integer' and e2.get_type().name == 'logical':
            as_integer = True
        elif e1.get_type().name == 'logical' and e2.get_type().name == 'integer':
            as_integer = True

        res = perform_op_on_vector_or_atomic(e1, e2,
                                             lambda l, r: cast_atomic(atomic_divide(l, r),
                                                                      'integer' if as_integer else 'double'))

        res = [VectorItem(None, el) for el in res]

        if len(res) == 0:
            t = get_more_important_vector_type(e1.get_type(), e2.get_type())
            return VectorObj([], t)

        ret = VectorObj.create(res)
        return ret


register_built_in_function(DivideFun)


@RObj.register_r_obj
class PowerFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = '^'
        args = [Arg('e1', None), Arg('e2', None)]
        return PowerFun(name, args)

    def compute(self, env: Environment):
        e1 = env.find_object('e1')
        e2 = env.find_object('e2')

        if e1.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('x', 'x ** y')
        if e2.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('y', 'x ** y')

        as_integer = False

        if e1.get_type().name == 'integer' and e2.get_type().name == 'integer':
            as_integer = True
        elif e1.get_type().name == 'integer' and e2.get_type().name == 'logical':
            as_integer = True
        elif e1.get_type().name == 'logical' and e2.get_type().name == 'integer':
            as_integer = True

        res = perform_op_on_vector_or_atomic(e1, e2,
                                             lambda l, r: cast_atomic(atomic_power(l, r),
                                                                      'integer' if as_integer else 'double'))

        res = [VectorItem(None, el) for el in res]

        if len(res) == 0:
            t = get_more_important_vector_type(e1.get_type(), e2.get_type())
            return VectorObj([], t)

        ret = VectorObj.create(res)
        return ret


register_built_in_function(PowerFun)


@RObj.register_r_obj
class DivModFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = '%%'
        args = [Arg('e1', None), Arg('e2', None)]

        return DivModFun(name, args)

    def compute(self, env: Environment):
        e1 = env.find_object('e1')
        e2 = env.find_object('e2')

        if e1.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('x', 'x ** y')
        if e2.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('y', 'x ** y')

        as_integer = False

        if e1.get_type().name == 'integer' and e2.get_type().name == 'integer':
            as_integer = True
        elif e1.get_type().name == 'integer' and e2.get_type().name == 'logical':
            as_integer = True
        elif e1.get_type().name == 'logical' and e2.get_type().name == 'integer':
            as_integer = True

        res = perform_op_on_vector_or_atomic(e1, e2,
                                             lambda l, r: cast_atomic(atomic_mod(l, r),
                                                                      'integer' if as_integer else 'double'))

        res = [VectorItem(None, el) for el in res]

        if len(res) == 0:
            t = get_more_important_vector_type(e1.get_type(), e2.get_type())
            return VectorObj([], t)

        ret = VectorObj.create(res)
        return ret


register_built_in_function(PowerFun)


@RObj.register_r_obj
class CatFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = 'cat'
        args = [Arg('...', None)]
        return PowerFun(name, args)

    def compute(self, env: Environment):
        e: DotsObj = env.find_object('...')

        for index, param in enumerate(e.items):
            if param[1].get_type().name not in ['character', 'double', 'integer', 'logical']:
                raise errors.ArgumentCannotBeHandledByFun(index+1, param[1].get_type().name, 'cat')
            for atom in param[1].items:
                rep = atom.show_self()
                print(rep)

        return NULLObj()


register_built_in_function(CatFun)


# @RObj.register_r_obj
# class IsTrue(BuiltInFun):
#
#     @staticmethod
#     def create(*args):
#         name = 'isTRUE'
#         args = [Arg('x', None)]
#         return IsTrue(name, args)
#
#     def compute(self, params: List[Param], env: Environment):
#         args = self.arrange_args(params)
#         e: Param = args['e']
#         itm: VectorObj = e.value
#         res = itm.get_type().name == 'logical' and len(itm.items) == 1 \
#               and not itm.items[0].value.is_nan and not itm.items[0].value.is_na
#         return VectorObj.create([VectorItem(None, Atomic(res, types.LogicalType()))])


# Arg('i', None), Arg('j', None), Arg('...', None)


# class PlainAssignFun(FunctionObj):
#
#     def compute(self, params: List[RObj], env: Environment):
#         args = self.arrange_args(params)

