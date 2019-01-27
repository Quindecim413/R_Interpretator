from typing import List, Tuple
import R.Atomics as utils
from R.Environment import Environment
from R.NonRObjs import VectorItem, ListItem
from R.RObj import RObj
import R.Types as types
import R.RuntimeErrors as errors
from R.RObj import Param


@RObj.register_r_obj
class EmptyParamObj(RObj):
    def show_self(self, *args, **kwargs):
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

    def show_self(self, *args, **kwargs):
        return 'NULL'

    show_self_for_print = show_self

    def create(self, *args, **kwargs):
        pass

    def evaluate(self, env: Environment):
        return self


@RObj.register_r_obj
class DotsObj(RObj):
    def __init__(self, items: List[Tuple]):
        super(DotsObj, self).__init__(types.NoType())
        self.items: List[Tuple] = items

    def show_self(self, *args, **kwargs):
        return '...'

    show_self_for_print = show_self

    @staticmethod
    def create(items: List[Param]):
        return DotsObj(items)

    def evaluate(self, env: Environment):
        return self


@RObj.register_r_obj
class VectorObj(RObj):
    def evaluate(self, env: Environment):
        return self

    def get_default_class(self):
        if self.get_type().name == 'character':
            ret = 'character'
        elif self.get_type().name == 'double':
            ret = 'numeric'
        elif self.get_type().name == 'integer':
            ret = 'integer'
        elif self.get_type().name == 'logical':
            ret = 'logical'
        else:
            raise Exception('vector was initialized with improper type - {}'.format(self.get_type().name))
        return RObj.get_r_obj('Atomic')(ret, types.CharacterType())

    def show_self(self, *args, **kwargs):
        if len(self.items) == 0:
            if self.get_type().name == 'character':
                return 'character(0)'
            elif self.get_type().name == 'double':
                return 'numeric(0)'
            elif self.get_type().name == 'integer':
                return 'integer(0)'
            elif self.get_type().name == 'logical':
                return 'logical(0)'
            else:
                raise Exception('vector was initialized with improper type - {}'.format(self.get_type().name))

        headers = []
        itms = []
        headers_empty = True
        for item in self.items:
            h = str(item[0])
            headers_empty = headers_empty and not h

            i = item[1].show_self()

            len_h = len(h)
            len_i = len(i)

            i = ' ' * (len_h - len_i) + i
            h = ' ' * (len_i - len_h) + h

            headers.append(h)
            itms.append(i)
        if headers_empty:
            res = '\t'.join(itms)
        else:
            res = '\n'.join(['\t'.join(headers), '\t'.join(itms)])
        return res

    show_self_for_print = show_self

    def __init__(self, items: List[VectorItem], type: types.BaseType):
        super(VectorObj, self).__init__(type)
        self.items: List[Tuple] = items

    @staticmethod
    def create(items: List[VectorItem]):
        if len(items) == 0:
            return RObj.get_r_obj('NULLObj')()
        return VectorObj(items, type(items[0][1].type)())

    def get_items(self):
        res = []
        for item in self.items:
            res.append(VectorObj([item]))
        return res

    def get_sub(self, key, options: List[utils.NamedOption]):
        pass


@RObj.register_r_obj
class ListObj(RObj):
    def evaluate(self, env: Environment):
        return self

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('list', types.CharacterType())

    def show_self(self, *args, **kwargs):
        if len(self.items) == 0:
            return 'list()'
        ret = self._show_from_depth()
        return ret

    def _show_from_depth(self, base_header=''):
        out = []
        for index, item in enumerate(self.items):
            header = base_header + ('$' + item[0] if item[0] else '[[{}]]'.format(index + 1))
            if item.value.get_type().name == 'list':
                res = item[1]._show_from_depth(header)
                out.append(header+'\n'+res)
            else:
                res = item[1].show_self()
                out.append(header+'\n'+res)

        ret = '\n'.join(out)
        return ret

    show_self_for_print = show_self

    def __init__(self, items):
        super(ListObj, self).__init__(types.ListType())
        self.items: List[Tuple] = items

    @staticmethod
    def create(items: List[Tuple]):
        return ListObj(items)

    def get_items(self):
        return self.items


@RObj.register_r_obj
class SymbolObj(RObj):
    def get_default_class(self):
        pass

    def __init__(self, name):
        super(SymbolObj, self).__init__(types.SymbolType())
        self.name = name

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('symbol', types.CharacterType())

    @staticmethod
    def create(name):
        return SymbolObj(name)

    def evaluate(self, env: Environment):
        ret = env.find_object(self.name)
        return ret

    def show_self(self, *args, **kwargs):
        return str(self.name)

    show_self_for_print = show_self
