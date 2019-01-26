from functools import wraps
import R.RuntimeErrors as errors
from R.Environment import Environment
import R.Types as types
from R.NonRObjs import VectorItem
from R.RObj import RObj

base_obj = None




@RObj.register_r_obj
class Atomic(RObj):
    def show_self(self, *args, **kwargs):
        if self.is_na:
            i = 'NA'
        elif self.is_nan:
            i = 'NaN'
        elif self.is_inf:
            if self.is_neg:
                i = '-Inf'
            else:
                i = 'Inf'
        elif self.get_type().name == 'logical':
            i = 'TRUE' if self.value else 'FALSE'
        else:
            i = ('-' if self.is_neg else '') + str(self.value)
        return i

    show_self_for_print = show_self

    def evaluate(self, env: Environment):
        # ret = RObj.get_r_obj('VectorObj')([VectorItem(None, self)])
        # return ret
        return self

    def __init__(self, value, type: types.BaseType, is_na=False, is_nan=False, is_inf=False, is_neg=False):
        if is_na and is_nan:
            raise Exception("Atomic can be NA and NaN at the same time")
        if (is_na or is_nan) and (is_inf):
            raise Exception('invalid Atomic initialization - is_na={}, is_nan={}, is_inf={}, is_neg={}'
                            .format(is_na, is_nan, is_inf, is_neg))
        super(Atomic, self).__init__(type)
        self.value = value
        self.type: types.BaseType = type
        self.is_na = is_na
        self.is_nan = is_nan
        self.is_inf = is_inf
        self.is_neg = is_neg


    @staticmethod
    def create(value, type: types.BaseType, is_na=False, is_nan=False, is_inf=False, is_neg=False):

        if type.name not in ['double', 'integer', 'logical', 'character', 'NULL', 'NA']:
            raise Exception('Invalid atomic initialization type - {}'.format(type.name))

        atom = Atomic(value, type, is_na=is_na, is_nan=is_nan, is_inf=is_inf, is_neg=is_neg)
        return atom

# def format_call_error(obj, method):
#     @wraps(method)
#     def wrapper(*args, **kwargs):
#         try:
#             return method(*args, **kwargs)
#         except errors.R_RuntimeError as e:
#             new_e = RError('Error in ' + obj.show_self() + ' :\n' + e.message)
#             raise new_e
#     return wrapper


def as_boolean(o):
    if isinstance(o, Atomic):
        if o.is_nan or o.is_na:
            return False
        elif o.is_inf:
            return True
        else:
            return bool(o.value)


# def atomic_as_boolean(o: Atomic):
#     if o.is_nan or o.is_na:
#         return False
#     elif o.is_inf:
#         return True
#     else:
#         return bool(o.value)
#
#
# def vector_first_as_boolean(o):
#     return atomic_as_boolean(o.items[0].value)


class NamedOption(object):
    def __init__(self, name, opt_value):
        self._name = name
        self._opt_value = opt_value

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._opt_value

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
