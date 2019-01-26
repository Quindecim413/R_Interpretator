from typing import List
from abc import abstractmethod
import R.Types as types

from R.Environment import Environment
from R.Function import FunctionObj, RObj, Arg, DotsObj, Param
from R.AtomicObjs import ListItem, ListObj, VectorObj, VectorItem, Atomic, EmptyParamObj, NULLObj
import R.RuntimeErrors as errors


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
    def compute(self, params: List[Param], env: Environment):
        pass


def cast_vector_items(items, python_type, r_type):
    ret = [VectorItem(item.name, Atomic(python_type(item.value.value), r_type())) for item in items]
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
class VectorFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = 'c'
        args = [Arg('...', None)]
        return VectorFun(name, args)

    def compute(self, params: List[Param], env: Environment):
        args = self.arrange_args(params)
        dots: DotsObj = args['...']
        items = dots.items
        if len(items) == 0:
            return RObj.get_r_obj('NULLObj').create()

        items_types = set(map(lambda i: i.value.get_type().name, items))
        casts = ['list', 'character', 'double', 'integer', 'logical']
        if set(casts).issubset(items_types):
            list_fun: FunctionObj = built_in_env.find_function('list')
            ret = list_fun.compute(params, env)
            return ret

        flat_items = []
        for item in items:
            if isinstance(item.value, Atomic):
                flat_items.append(VectorItem(item.name, item.value))
            elif isinstance(item.value, VectorObj):
                flat_items.extend(item.value.items)
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
class ListFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = 'list'
        args = [Arg('...', None)]
        return ListFun(name, args)

    def compute(self, params: List[Param], env: Environment):
        args = self.arrange_args(params)
        dots: DotsObj = args['...']
        items = dots.items
        list_items = []
        for item in items:
            itm = ListItem(item.name, item.value)
            list_items.append(itm)
        return ListObj(list_items)


register_built_in_function(ListFun)


class UnsupportedVectorType(Exception):
    def __init__(self, invalid_type, operand_index):
        super(UnsupportedVectorType, self).__init__('unsupported vector type - {}'.format(invalid_type))
        self.operand_index = operand_index


def get_more_important_vector_type(type1, type2):
    tps = [type1.name, type2.name]
    # if 'list' in tps:
    #     return types.ListType()
    if 'character' in tps:
        return types.CharacterType()
    elif 'double' in tps:
        return types.DoubleType()
    elif 'integer' in tps:
        return types.IntegerType()
    elif 'logical' in tps:
        return types.LogicalType()
    first = tps[0] not in ['character', 'double', 'integer', 'logical']
    raise UnsupportedVectorType(tps, operand_index=0 if first else 1)


def atomic_add(e1: Atomic, e2: Atomic):
    type = get_more_important_vector_type(e1.get_type(), e2.get_type())

    if type.name == 'character':
        raise errors.NonNumericToBinary()

    is_nan = e1.is_nan or e2.is_nan
    is_na = e2.is_na or e2.is_na or (e1.is_inf and e2.is_inf and (e1.is_neg != e2.is_neg))
    is_inf = (e1.is_inf or e2.is_inf)
    is_neg = (e1.is_inf and not e2.is_inf and e1.is_neg) or (not e1.is_inf and e2.is_inf and e2.is_neg)

    if is_nan:
        return Atomic(None, type, is_nan=True)
    elif is_na:
        return Atomic(None, type, is_na=True)
    elif is_inf:
        return Atomic(None, type, is_inf=True, is_neg=is_neg)

    if type.name == 'double':
        val = float(e1.value) * (-1 if e1.is_neg else 1) + float(e2.value) * (-1 if e2.is_neg else 1)
    elif type.name == 'integer':
        val = int(int(e1.value) * (-1 if e1.is_neg else 1) + int(e2.value) * (-1 if e2.is_neg else 1))
    elif type.name == 'logical':
        val = int(int(e1.value) * (-1 if e1.is_neg else 1) + int(e2.value) * (-1 if e2.is_neg else 1))
        type = types.IntegerType()
    else:
        raise Exception('invalid vector type - {}'.format(type.name))

    if val < 0:
        return Atomic(-val, type, is_neg=True)
    else:
        return Atomic(val, type)


def atomic_subtract(e1: Atomic, e2: Atomic):
    type = get_more_important_vector_type(e1.get_type(), e2.get_type())

    if type.name == 'character':
        raise errors.NonNumericToBinary()
    new_e2 = Atomic(e2.value, e2.type, is_na=e2.is_na, is_nan=e2.is_nan, is_inf=e2.is_inf, is_neg=not e2.is_neg)

    ret = atomic_add(e1, new_e2)
    return ret


def atomic_multiply(e1: Atomic, e2: Atomic):
    type = get_more_important_vector_type(e1.get_type(), e2.get_type())

    if type.name == 'character':
        raise errors.NonNumericToBinary()

    is_nan = e1.is_nan or e2.is_nan
    is_na = e1.is_na or e2.is_na or ((e1.is_inf or e2.is_inf) and (e1.value == 0 or e2.value == 0))
    is_inf = (e1.is_inf or e2.is_inf)
    is_neg = e1.is_neg != e2.is_neg

    if is_nan:
        return Atomic(None, type, is_nan=True)
    elif is_na:
        return Atomic(None, type, is_na=True)
    elif is_inf:
        return Atomic(None, type, is_inf=True, is_neg=is_neg)

    if type.name == 'double':
        val = float(e1.value) * float(e2.value) * (-1 if e1.is_neg != e2.is_neg else 1)
    elif type.name == 'integer':
        val = int(int(e1.value) * int(e2.value) * (-1 if e1.is_neg != e2.is_neg else 1))
    elif type.name == 'logical':
        val = int(e1.value) * int(e2.value) * (-1 if e1.is_neg != e2.is_neg else 1)
        type = types.IntegerType()
    else:
        raise Exception('invalid vector type - {}'.format(type.name))

    if val < 0:
        return Atomic(-val, type, is_neg=True)
    else:
        return Atomic(val, type)


def atomic_divide(e1: Atomic, e2: Atomic):
    type = get_more_important_vector_type(e1.get_type(), e2.get_type())

    if type.name == 'character':
        raise errors.NonNumericToBinary()

    if e2.is_inf:
        new_e2 = Atomic(False, types.LogicalType(), is_inf=False, is_neg=e2.is_neg)
    else:
        if e2.value == 0 and not e2.is_na and not e2.is_nan:
            new_e2 = Atomic(None, e2.type, is_na=False, is_nan=False, is_inf=True, is_neg=e2.is_neg)
        elif not e2.is_na and not e2.is_nan:
            new_e2 = Atomic(1 / e2.value, e2.type, is_na=e2.is_na, is_nan=e2.is_nan, is_inf=e2.is_inf, is_neg=e2.is_neg)
        else:
            new_e2 = e2
    ret = atomic_multiply(e1, new_e2)
    return ret


def atomic_power(e1: Atomic, e2: Atomic):
    type = get_more_important_vector_type(e1.get_type(), e2.get_type())

    if type.name == 'character':
        raise errors.NonNumericToBinary()

    is_na = e1.is_na and not (e2.value == 0)
    is_nan = (e1.is_nan and e2.is_na) or (e1.is_nan and (e2.value == 0)) or ((e1.value == 0) and e2.is_nan)
    is_inf = (e1.is_inf and not e2.is_inf and e2.is_neg) or (e1.is_inf and e2.value != 0)

    if is_na:
        return Atomic(None, type, is_na=True)
    elif is_nan:
        return Atomic(None, type, is_nan=True)
    elif is_inf:
        return Atomic(None, type, is_inf=True)
    elif e1.value == 1 and e1.is_neg and e2.value == 0:
        return Atomic(1, type)
    elif e1.is_neg and e2.value == int(e2.value):
        ret = Atomic(e1.value ** e2.value, type)
        return ret

    if type.name == 'double':
        val = (float(e1.value) * (-1 if e1.is_neg else 1)) ** (float(e2.value) * (-1 if e1.is_neg else 1))
    elif type.name == 'integer':
        val = int((int(e1.value) * (-1 if e1.is_neg else 1)) ** (int(e2.value) * (-1 if e1.is_neg else 1)))
    elif type.name == 'logical':
        val = (int(e1.value) * (-1 if e1.is_neg else 1)) ** (int(e2.value) * (-1 if e1.is_neg else 1))
        type = types.IntegerType()
    else:
        raise Exception('invalid vector type - {}'.format(type.name))

    if isinstance(val, complex):
        return Atomic(None, type, is_nan=True)

    if val < 0:
        return Atomic(-val, type, is_neg=True)
    else:
        return Atomic(val, type)

# TODO

def atomic_mod(e1: Atomic, e2: Atomic):
    type = get_more_important_vector_type(e1.get_type(), e2.get_type())

    if type.name == 'character':
        raise errors.NonNumericToBinary()

    is_na = e1.is_na and not (e2.value == 0)
    is_nan = (e1.is_nan and e2.is_na) or (e1.is_nan and (e2.value == 0)) or ((e1.value == 0) and e2.is_nan)
    is_inf = (e1.is_inf and not e2.is_inf and e2.is_neg) or (e1.is_inf and e2.value != 0)

    if is_na:
        return Atomic(None, type, is_na=True)
    elif is_nan:
        return Atomic(None, type, is_nan=True)
    elif is_inf:
        return Atomic(None, type, is_inf=True)
    elif e1.value == 1 and e1.is_neg and e2.value == 0:
        return Atomic(1, type)
    elif e1.is_neg and e2.value == int(e2.value):
        ret = Atomic(e1.value ** e2.value, type)
        return ret

    if type.name == 'double':
        val = (float(e1.value) * (-1 if e1.is_neg else 1)) ** (float(e2.value) * (-1 if e1.is_neg else 1))
    elif type.name == 'integer':
        val = int((int(e1.value) * (-1 if e1.is_neg else 1)) ** (int(e2.value) * (-1 if e1.is_neg else 1)))
    elif type.name == 'logical':
        val = (int(e1.value) * (-1 if e1.is_neg else 1)) ** (int(e2.value) * (-1 if e1.is_neg else 1))
        type = types.IntegerType()
    else:
        raise Exception('invalid vector type - {}'.format(type.name))

    if isinstance(val, complex):
        return Atomic(None, type, is_nan=True)

    if val < 0:
        return Atomic(-val, type, is_neg=True)
    else:
        return Atomic(val, type)


def atomic_not(e: Atomic):
    if e.type.name == 'character':
        raise errors.InvalidArgType()

    if e.is_inf:
        ret = Atomic(False, types.LogicalType())
        return ret
    elif e.is_na or e.is_nan:
        return Atomic(None, e.type, is_na=True)
    ret = Atomic(not bool(e.value), types.LogicalType())
    return ret


def atomic_and(e1: Atomic, e2: Atomic):
    type = get_more_important_vector_type(e1.get_type(), e2.get_type())

    if e1.is_na or e2.is_na:
        return Atomic(None, types.LogicalType(), is_na=True)
    if e1.is_nan or e2.is_nan:
        return Atomic(None, types.LogicalType(), is_na=True)
    if e1.is_inf and e2.is_inf:
        return Atomic(True, types.LogicalType())
    if (e1.is_inf and e2.value == 0) or (e1.value == 0 and e2.is_inf):
        return Atomic(False, types.LogicalType())

    if type.name == 'character':
        val = str(e1.value) and str(e2.value)
    elif type.name == 'double':
        val = float(e1.value) * (-1 if e1.is_neg else 1) and float(e2.value) * (-1 if e2.is_neg else 1)
    elif type.name == 'integer':
        val = int(e1.value) * (-1 if e1.is_neg else 1) and int(e2.value) * (-1 if e2.is_neg else 1)
    elif type.name == 'logical':
        val = bool(e1.value) and bool(e2.value)
    else:
        raise Exception('invalid vector type - {}'.format(type.name))

    return Atomic(bool(val), types.LogicalType())


def atomic_or(e1: Atomic, e2: Atomic):
    type = get_more_important_vector_type(e1.get_type(), e2.get_type())

    if e1.is_na or e2.is_na:
        return Atomic(None, types.LogicalType(), is_na=True)
    if e1.is_nan or e2.is_nan:
        return Atomic(None, types.LogicalType(), is_na=True)
    if e1.is_inf or e2.is_inf:
        return Atomic(True, types.LogicalType())
    if (e1.is_inf and e2.value == 0) or (e1.value == 0 and e2.is_inf):
        return Atomic(False, types.LogicalType())

    if type.name == 'character':
        val = str(e1.value) or str(e2.value)
    elif type.name == 'double':
        val = float(e1.value) * (-1 if e1.is_neg else 1) or float(e2.value) * (-1 if e2.is_neg else 1)
    elif type.name == 'integer':
        val = int(e1.value) * (-1 if e1.is_neg else 1) or int(e2.value) * (-1 if e2.is_neg else 1)
    elif type.name == 'logical':
        val = bool(e1.value) or bool(e2.value)
    else:
        raise Exception('invalid vector type - {}'.format(type.name))

    return Atomic(bool(val), types.LogicalType())


def atomic_is_equal(e1: Atomic, e2: Atomic):
    type = get_more_important_vector_type(e1.get_type(), e2.get_type())
    if e1.is_na or e2.is_na:
        return Atomic(None, types.LogicalType(), is_na=True)
    if e1.is_nan or e2.is_nan:
        return Atomic(None, types.LogicalType(), is_na=True)
    if e1.is_inf and e2.is_inf:
        return Atomic(e1.value == e2.value, types.LogicalType())

    if type.name == 'character':
        return Atomic(str(e1.value) == str(e2.value), types.LogicalType())
    elif type.name == 'double':
        return Atomic(float(e1.value) == float(e2.value), types.LogicalType())
    elif type.name == 'integer':
        return Atomic(int(e1.value) == int(e2.value), types.LogicalType())
    elif type.name == 'logical':
        return Atomic(bool(e1.value) == bool(e2.value), types.LogicalType())
    else:
        raise Exception('invalid vector type - {}'.format(type.name))


def atomic_is_not_equal(e1: Atomic, e2: Atomic):
    res = atomic_is_equal(e1, e2)
    if res.get_type().name == 'logical':
        res.value = not res.value
    return res


def atomic_is_greater(e1: Atomic, e2: Atomic):
    type = get_more_important_vector_type(e1.get_type(), e2.get_type())
    if e1.is_na or e2.is_na:
        return Atomic(None, types.LogicalType(), is_na=True)
    if e1.is_nan or e2.is_nan:
        return Atomic(None, types.LogicalType(), is_na=True)
    if e1.is_inf and e2.is_inf:
        return Atomic(e1.is_neg < e2.is_neg, types.LogicalType())
    if e1.is_inf != e2.is_inf:
        return Atomic(e1.is_inf and not e1.is_neg or e2.is_inf and e2.is_neg, types.LogicalType())

    if type.name == 'character':
        return Atomic(str(e1.value) > str(e2.value), types.LogicalType())
    elif type.name == 'double':
        return Atomic(float(e1.value) * (-1 if e1.is_neg else 1) > float(e2.value) * (-1 if e2.is_neg else 1),
                      types.LogicalType())
    elif type.name == 'integer':
        return Atomic(int(e1.value) * (-1 if e1.is_neg else 1) > int(e2.value) * (-1 if e2.is_neg else 1),
                      types.LogicalType())
    elif type.name == 'logical':
        return Atomic(bool(e1.value) > bool(e2.value), types.LogicalType())
    else:
        raise Exception('invalid vector type - {}'.format(type.name))


def atomic_is_less(e1: Atomic, e2: Atomic):
    ret = atomic_is_greater(e2, e1)
    return ret


def atomic_is_equal_or_greater(e1: Atomic, e2: Atomic):
    type = get_more_important_vector_type(e1.get_type(), e2.get_type())
    if e1.is_na or e2.is_na:
        return Atomic(None, types.LogicalType(), is_na=True)
    if e1.is_nan or e2.is_nan:
        return Atomic(None, types.LogicalType(), is_na=True)
    if e1.is_inf and e2.is_inf:
        return Atomic(e1.is_neg < e2.is_neg, types.LogicalType())
    if e1.is_inf != e2.is_inf:
        return Atomic(e1.is_inf and not e1.is_neg or e2.is_inf and e2.is_neg, types.LogicalType())

    if type.name == 'character':
        return Atomic(str(e1.value) >= str(e2.value), types.LogicalType())
    elif type.name == 'double':
        return Atomic(float(e1.value) * (-1 if e1.is_neg else 1) >= float(e2.value) * (-1 if e2.is_neg else 1),
                      types.LogicalType())
    elif type.name == 'integer':
        return Atomic(int(e1.value) * (-1 if e1.is_neg else 1) >= int(e2.value) * (-1 if e2.is_neg else 1),
                      types.LogicalType())
    elif type.name == 'logical':
        return Atomic(bool(e1.value) >= bool(e2.value), types.LogicalType())
    else:
        raise Exception('invalid vector type - {}'.format(type.name))


def atomic_is_less_or_greater(e1: Atomic, e2: Atomic):
    ret = atomic_is_equal_or_greater(e2, e1)
    return ret


def cast_atomic(e: Atomic, type_name):
    if e.get_type().name == type_name:
        return e
    elif type_name == 'character':
        ret = Atomic(bool(e.value), types.CharacterType(), is_na=e.is_na, is_nan=e.is_nan, is_inf=e.is_inf,
                     is_neg=e.is_neg)
        return ret
    elif type_name == 'double':
        ret = Atomic(float(e.value), types.DoubleType(), is_na=e.is_na, is_nan=e.is_nan, is_inf=e.is_inf,
                     is_neg=e.is_neg)
        return ret
    elif type_name == 'integer':
        ret = Atomic(int(e.value), types.IntegerType(), is_na=e.is_na, is_nan=e.is_nan, is_inf=e.is_inf,
                     is_neg=e.is_neg)
        return ret
    elif type_name == 'logical':
        ret = Atomic(bool(e.value), types.LogicalType(), is_na=e.is_na, is_nan=e.is_nan, is_inf=e.is_inf,
                     is_neg=e.is_neg)
        return ret
    else:
        raise Exception('unsupported vector cast type - {}'.format(type_name))



@RObj.register_r_obj
class AndAndFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = '&&'
        args = [Arg('x', None), Arg('y', None)]
        return AndAndFun(name, args)

    def compute(self, params: List[Param], env: Environment):
        args = self.arrange_args(params)
        e1: Param = args['x']
        e2: Param = args['y']
        if e1.value.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('x', 'x && y')
        if e2.value.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('y', 'x && y')
        res = []

        try:
            for l, r in concat_vectors(e1.value.items, e2.value.items):
                res.append(atomic_and(l.value, r.value))
        except UnsupportedVectorType as e:
            raise errors.InvalidArgTypeInArgs('x' if e.operand_index == 0 else 'y', 'x && y')

        res = [VectorItem(None, el) for el in res]

        ret = VectorObj(res)
        return ret


register_built_in_function(AndAndFun)


@RObj.register_r_obj
class AndFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = '&'
        args = [Arg('x', None), Arg('y', None)]
        return AndFun(name, args)

    def compute(self, params: List[Param], env: Environment):
        args = self.arrange_args(params)
        e1: VectorObj = args['x']
        e2: VectorObj = args['y']
        if e1.value.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('x', 'x & y')
        if e2.value.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('y', 'x & y')
        res = VectorItem(None, atomic_and(e1.value.items[0].value, e2.value.items[0].value))
        ret = VectorObj([res])
        return ret


register_built_in_function(AndFun)


@RObj.register_r_obj
class OrOrFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = '||'
        args = [Arg('x', None), Arg('y', None)]
        return OrOrFun(name, args)

    def compute(self, params: List[Param], env: Environment):
        args = self.arrange_args(params)
        e1: Param = args['x']
        e2: Param = args['y']
        if e1.value.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('x', 'x || y')
        if e2.value.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('y', 'x || y')
        res = []
        for l, r in concat_vectors(e1.value.items, e2.value.items):
            res.append(atomic_or(l.value, r.value))

        res = [VectorItem(None, el) for el in res]

        ret = VectorObj(res)
        return ret


register_built_in_function(OrOrFun)


@RObj.register_r_obj
class OrFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = '|'
        args = [Arg('x', None), Arg('y', None)]
        return OrFun(name, args)

    def compute(self, params: List[Param], env: Environment):
        args = self.arrange_args(params)
        e1: Param = args['x']
        e2: Param = args['y']
        if e1.value.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('x', 'x | y')
        if e2.value.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('y', 'x | y')
        res = VectorItem(None, atomic_or(e1.value.items[0].value, e2.value.items[0].value))
        ret = VectorObj([res])
        return ret


register_built_in_function(OrFun)


@RObj.register_r_obj
class NotFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = '!'
        args = [Arg('x', None)]
        return NotFun(name, args)

    def compute(self, params: List[Param], env: Environment):
        args = self.arrange_args(params)
        e1: Param = args['x']
        if e1.value.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgType()
        res = []
        for item in e1.value.items:
            res.append(atomic_not(item.value))

        res = [VectorItem(None, el) for el in res]

        ret = VectorObj(res)
        return ret


register_built_in_function(NotFun)


@RObj.register_r_obj
class AddFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = '+'
        args = [Arg('e1', None), Arg('e2', None)]
        return AddFun(name, args)

    def compute(self, params: List[Param], env: Environment):
        args = self.arrange_args(params)
        e1: Param = args['e1']
        e2: Param = args['e2']

        if isinstance(e2, EmptyParamObj):
            return e1.value

        if e1.value.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('x', 'x + y')
        if e2.value.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('y', 'x + y')
        res = []

        as_integer = False

        if e1.value.get_type().name == 'integer' and e2.value.get_type().name == 'integer':
            as_integer = True
        elif e1.value.get_type().name == 'integer' and e2.value.get_type().name == 'logical':
            as_integer = True
        elif e1.value.get_type().name == 'logical' and e2.value.get_type().name == 'integer':
            as_integer = True

        for l, r in concat_vectors(e1.value.items, e2.value.items):
            res.append(cast_atomic(atomic_add(l.value, r.value), 'integer' if as_integer else 'double'))

        res = [VectorItem(None, el) for el in res]

        ret = VectorObj(res)
        return ret


register_built_in_function(AddFun)


@RObj.register_r_obj
class SubtractFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = '-'
        args = [Arg('e1', None), Arg('e2', None)]
        return SubtractFun(name, args)

    def compute(self, params: List[Param], env: Environment):
        args = self.arrange_args(params)
        e1: Param = args['e1']
        e2: Param = args['e2']

        if isinstance(e2, EmptyParamObj):
            if e1.value.get_type().name not in ['double', 'logical', 'integer']:
                raise errors.InvalidArgTypeInArgs('x', '- x')

            res = []
            for item in e1.value.items:
                res.append(atomic_subtract(Atomic(False, types.LogicalType()), item.value))

            res = [VectorItem(None, el)
                   for el in res]

            ret = VectorObj(res)
            return ret

        if e1.value.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('x', 'x - y')
        if e2.value.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('y', 'x - y')
        res = []

        as_integer = False

        if e1.value.get_type().name == 'integer' and e2.value.get_type().name == 'integer':
            as_integer = True
        elif e1.value.get_type().name == 'integer' and e2.value.get_type().name == 'logical':
            as_integer = True
        elif e1.value.get_type().name == 'logical' and e2.value.get_type().name == 'integer':
            as_integer = True

        for l, r in concat_vectors(e1.value.items, e2.value.items):
            res.append(cast_atomic(atomic_subtract(l.value, r.value), 'integer' if as_integer else 'double'))

        res = [VectorItem(None, el) for el in res]

        ret = VectorObj(res)
        return ret


register_built_in_function(SubtractFun)


@RObj.register_r_obj
class MultiplyFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = '*'
        args = [Arg('e1', None), Arg('e2', None)]
        return MultiplyFun(name, args)

    def compute(self, params: List[Param], env: Environment):
        args = self.arrange_args(params)
        e1: Param = args['e1']
        e2: Param = args['e2']

        if e1.value.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('x', 'x * y')
        if e2.value.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('y', 'x * y')
        res = []

        as_integer = False

        if e1.value.get_type().name == 'integer' and e2.value.get_type().name == 'integer':
            as_integer = True
        elif e1.value.get_type().name == 'integer' and e2.value.get_type().name == 'logical':
            as_integer = True
        elif e1.value.get_type().name == 'logical' and e2.value.get_type().name == 'integer':
            as_integer = True

        for l, r in concat_vectors(e1.value.items, e2.value.items):
            res.append(cast_atomic(atomic_multiply(l.value, r.value), 'integer' if as_integer else 'double'))

        res = [VectorItem(None, el) for el in res]

        ret = VectorObj(res)
        return ret


register_built_in_function(MultiplyFun)


@RObj.register_r_obj
class DivideFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = '/'
        args = [Arg('e1', None), Arg('e2', None)]
        return DivideFun(name, args)

    def compute(self, params: List[Param], env: Environment):
        args = self.arrange_args(params)
        e1: Param = args['e1']
        e2: Param = args['e2']

        if e1.value.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('x', 'x / y')
        if e2.value.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('y', 'x / y')
        res = []

        as_integer = False

        if e1.value.get_type().name == 'integer' and e2.value.get_type().name == 'integer':
            as_integer = True
        elif e1.value.get_type().name == 'integer' and e2.value.get_type().name == 'logical':
            as_integer = True
        elif e1.value.get_type().name == 'logical' and e2.value.get_type().name == 'integer':
            as_integer = True

        for l, r in concat_vectors(e1.value.items, e2.value.items):
            res.append(cast_atomic(atomic_divide(l.value, r.value), 'integer' if as_integer else 'double'))

        res = [VectorItem(None, el) for el in res]

        ret = VectorObj(res)
        return ret


register_built_in_function(DivideFun)


@RObj.register_r_obj
class PowerFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = '**'
        args = [Arg('e1', None), Arg('e2', None)]
        return PowerFun(name, args)

    def compute(self, params: List[Param], env: Environment):
        args = self.arrange_args(params)
        e1: Param = args['e1']
        e2: Param = args['e2']

        if e1.value.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('x', 'x ** y')
        if e2.value.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('y', 'x ** y')
        res = []

        as_integer = False

        if e1.value.get_type().name == 'integer' and e2.value.get_type().name == 'integer':
            as_integer = True
        elif e1.value.get_type().name == 'integer' and e2.value.get_type().name == 'logical':
            as_integer = True
        elif e1.value.get_type().name == 'logical' and e2.value.get_type().name == 'integer':
            as_integer = True

        for l, r in concat_vectors(e1.value.items, e2.value.items):
            res.append(cast_atomic(atomic_power(l.value, r.value), 'integer' if as_integer else 'double'))

        res = [VectorItem(None, el) for el in res]

        ret = VectorObj(res)
        return ret


register_built_in_function(PowerFun)


@RObj.register_r_obj
class DivModFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = '%%'
        args = [Arg('e1', None), Arg('e2', None)]

        return DivModFun(name, args)

    def compute(self, params: List[Param], env: Environment):
        args = self.arrange_args(params)
        e1: Param = args['e1']
        e2: Param = args['e2']

        if e1.value.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('x', 'x ** y')
        if e2.value.get_type().name not in ['double', 'logical', 'integer']:
            raise errors.InvalidArgTypeInArgs('y', 'x ** y')
        res = []

        as_integer = False

        if e1.value.get_type().name == 'integer' and e2.value.get_type().name == 'integer':
            as_integer = True
        elif e1.value.get_type().name == 'integer' and e2.value.get_type().name == 'logical':
            as_integer = True
        elif e1.value.get_type().name == 'logical' and e2.value.get_type().name == 'integer':
            as_integer = True

        for l, r in concat_vectors(e1.value.items, e2.value.items):
            res.append(cast_atomic(atomic_mod(l.value, r.value), 'integer' if as_integer else 'double'))

        res = [VectorItem(None, el) for el in res]

        ret = VectorObj(res)
        return ret


register_built_in_function(PowerFun)


@RObj.register_r_obj
class CatFun(BuiltInFun):
    @staticmethod
    def create(*args):
        name = 'cat'
        args = [Arg('...', None)]
        return PowerFun(name, args)

    def compute(self, params: List[Param], env: Environment):
        args = self.arrange_args(params)
        e: DotsObj = args['...']

        for index, param in enumerate(e.items):
            if param.value.get_type().name not in ['character', 'double', 'integer', 'logical']:
                raise errors.ArgumentCannotBeHandledByFun(index+1, param.value.get_type().name, 'cat')
            for atom in param.value.items:
                rep = atom.show_self()
                print(rep)

        return NULLObj()


register_built_in_function(CatFun)


# class PlainAssignFun(FunctionObj):
#
#     def compute(self, params: List[RObj], env: Environment):
#         args = self.arrange_args(params)

