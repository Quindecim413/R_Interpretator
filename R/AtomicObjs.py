from typing import List
import R.Utils as utils
from R.Environment import Environment
from R.RObj import RObj
import R.Types as types
import R.RuntimeErrors as errors
from R.RObj import Param


@RObj.register_r_obj
class Atomic(RObj):
    def show_self(self):
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

    def evaluate(self, env: Environment):
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


@RObj.register_r_obj
class EmptyParamObj(RObj):
    def show_self(self):
        pass

    def create(self, *args, **kwargs):
        pass

    def evaluate(self, env: Environment):
        pass

    def __init__(self, arg_name):
        def throw_invalid_param(*args, **kwargs):
            raise errors.ArgumentMissingWithNoDefualt(arg_name)
        self.evaluate = throw_invalid_param
        self.get_type = throw_invalid_param
        self.set_value = throw_invalid_param
        self.set_super_sub = throw_invalid_param
        self.get_sub = throw_invalid_param
        self.get_super_sub = throw_invalid_param
        self.set_sub = throw_invalid_param
        self.get_dlr = throw_invalid_param
        self.set_dlr = throw_invalid_param

        super(EmptyParamObj, self).__init__(types.NoType())


# class DotsItem(object):
#     def __init__(self, name, value: RObj):
#         self.name = name
#         self.value: RObj = value


@RObj.register_r_obj
class NULLObj(RObj):
    def __init__(self):
        super(NULLObj, self).__init__(types.NULLType())

    def show_self(self):
        return 'NULL'

    def create(self, *args, **kwargs):
        pass

    def evaluate(self, env: Environment):
        return self


@RObj.register_r_obj
class DotsObj(RObj):
    def __init__(self, items: List[Param]):
        super(DotsObj, self).__init__(types.NoType())
        self.items: List[Param] = items

    def show_self(self):
        pass

    @staticmethod
    def create(items: List[Param]):
        return DotsObj(items)

    def evaluate(self, env: Environment):
        return self





class VectorItem(object):
    def __init__(self, name, value: Atomic):
        self.name = name if name is not None else ''
        if not isinstance(value, Atomic):
            raise Exception('VectorItem accepts only Atomic value. Got {}'.format(value))
        self.value: Atomic = value

@RObj.register_r_obj
class VectorObj(RObj):
    def evaluate(self, env: Environment):
        return self

    def show_self(self):
        headers = []
        itms = []
        headers_empty = True
        for item in self.items:
            h = str(item.name)
            headers_empty = headers_empty and not h

            i = item.value.show_self()

            len_h = len(h)
            len_i = len(i)

            i = ' ' * (len_h - len_i) + i
            h = ' ' * (len_i - len_h) + h

            headers.append(h)
            itms.append(i)
        if headers_empty:
            res = '\t'.join(itms)
        else:
            res = '\n'.join(['    '.join(headers), '    '.join(itms)])
        return res

    def __init__(self, items: List[VectorItem]):
        super(VectorObj, self).__init__(type(items[0].value.type)())
        self.items: List[VectorItem] = items


    @staticmethod
    def create(items: List[VectorItem]):
        if len(items) == 0:
            return RObj.get_r_obj('NULLObj')()
        return VectorObj(items)
    # def evaluate(self, env: Environment):
    #     o = []
    #     for obj in self.objs:
    #         if isinstance(obj, Atomic):
    #             o.append(obj)
    #         if isinstance(obj, RObj.get_r_obj('DotsObj')):
    #             items: List[] = obj.get_items()

    def get_sub(self, key, options: List[utils.NamedOption]):
        pass


class ListItem(object):
    def __init__(self, name, value: RObj):
        self.name = name if name is not None else ''
        if not isinstance(value, RObj):
            raise Exception('ListItem accepts only RObj value. Got {}'.format(value))
        self.value: RObj = value


@RObj.register_r_obj
class ListObj(RObj):
    def evaluate(self, env: Environment):
        return self

    def show_self(self):
        pass

    def __init__(self, items):
        super(ListObj, self).__init__(types.ListType())
        self._items = items

    def create(self, items: List[ListItem]):
        return ListObj(items)


@RObj.register_r_obj
class SymbolObj(RObj):
    def __init__(self, name):
        super(SymbolObj, self).__init__(types.SymbolType())
        self.name = name

    @staticmethod
    def create(name):
        return SymbolObj(name)

    def evaluate(self, env: Environment):
        ret = env.find_object(self.name)
        return ret

    def show_self(self):
        pass