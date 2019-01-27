from R.Environment import Environment, ReturnCommand
from R.NonRObjs import VectorItem
from R.RObj import RObj, Param, Arg, RError, execute_item
from typing import List, Dict, Tuple
import R.Types as types
import R.RuntimeErrors as errors
from abc import abstractmethod
from R.AtomicObjs import DotsObj, EmptyParamObj, VectorObj
from R.Atomics import Atomic


def func_args_arrange(fun_params: List[Tuple], fun_args: List[Tuple]) -> Dict[str, RObj]:
    args_res = {arg[0]: arg[1] for arg in fun_args}

    assign_type = RObj.get_r_obj('AssignObj')

    named_params = dict()

    unset_params = []

    params = list(enumerate(fun_params))

    for index, param in params:
        if isinstance(param, assign_type):
            if param.mode == 'plain':
                item = param.item
                if item.get_type().name == 'symbol':
                    named_params[item.name] = (index, param)
                elif isinstance(item, Atomic):
                    if item.type.name == 'character':
                        named_params[item.value] = (index, param)
                    else:
                        raise errors.InvalidLeftHandAssignment()
                else:
                    raise errors.InvalidLeftHandAssignment()
        else:
            unset_params.append((index, param))

    dots_items = []

    has_dots_obj = len(list(filter(lambda arg: arg[0] == '...', fun_args))) != 0

    for name, obj in named_params.items():
        if name not in args_res:
            if not has_dots_obj:
                raise errors.UnusedArguments(obj[1])
            else:
                dots_items.append(obj)
        else:
            args_res[name] = obj[1]

    unused_count = len(unset_params)

    i = 0

    res = args_res.copy()

    for arg_name, val in args_res.items():
        if val is None:
            if arg_name == '...':
                arr = [*unset_params[i:], *dots_items]
                itms = [i[1] for i in sorted(arr, key=lambda o: o[0])]
                res[arg_name] = DotsObj.create(itms)
                i = unused_count
            else:
                if i == unused_count:
                    res[arg_name] = EmptyParamObj(arg_name)
                else:
                    param = unset_params[i]
                    i = i + 1
                    res[arg_name] = param[1][1]

    return res


def arrange_params_with_function_args(params, func, env: Environment):
    res = func_args_arrange(params, func.input_args)
    new_env: Environment = Environment(env)

    for name, val in res.items():
        new_env.add(name, val)

    return new_env

@RObj.register_r_obj
class FunctionObj(RObj):
    def __init__(self, input_args, body: RObj):
        super(FunctionObj, self).__init__(types.ClosureType())
        self.input_args: List[Arg] = input_args
        self.body = body

    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('function', types.CharacterType())

    def show_self(self):
        args = []
        for arg in self.input_args:
            arg_val = arg[0] + ((' = {}'.format(arg[1].show_self())) if arg[1] is not None else '')
            args.append(arg_val)
        body_val = self.body.show_self()
        args_val = ', '.join(args)
        ret = 'function (' + args_val + ')' + \
              (body_val if isinstance(self.body, RObj.get_r_obj('SuiteObj'))
               else ' {}'.format(body_val))
        return ret

    def show_self_for_print(self, *args, **kwargs):
        args = []
        for arg in self.input_args:
            arg_val = arg.name + ((' = {}'.format(arg.value.show_self())) if arg.value is not None else '')
            args.append(arg_val)
        body_val = self.body.show_self()
        args_val = ', '.join(args)
        ret = 'function (' + args_val + ')' + \
              (body_val if isinstance(self.body, RObj.get_r_obj('SuiteObj'))
               else ' {}'.format(body_val)) + '\n<bytecode: {}>'.format(id(self))
        return ret

    # объект call создает список аргументов и передает их сюда
    @staticmethod
    def create(input_args: List, body: RObj):
        args = []
        for arg in input_args:
            if isinstance(arg, RObj.get_r_obj('SymbolObj')):
                a = Arg(arg.name, None)
            elif isinstance(arg, RObj.get_r_obj('AssignObj')):
                if not isinstance(arg.item, RObj.get_r_obj('SymbolObj')):
                    raise errors.R_RuntimeError('invalid assigment of function')
                else:
                    a = Arg(arg.item.name, arg.value)
            args.append(a)

        return FunctionObj(args, body)

    def evaluate(self, env: Environment):
        return self

    # def arrange_args(self, params: List[Param]):
    #     ret = func_args_arrange(params, self.input_args)
    #     return ret

    @staticmethod
    def create_new_environment(initialized_args: Dict[str, RObj], env: Environment):
        new_env: Environment = Environment(env)
        for name, val in initialized_args.items():
            val_val = val.evaluate(new_env)
            new_env.add(name, val_val)
        return new_env

    @abstractmethod
    def compute(self, env: Environment):
        # inited_args = self.arrange_args(params)
        # new_env: Environment = self.create_new_environment(inited_args)
        try:
            ret = execute_item(self.body, env)
            return ret
        except ReturnCommand as e:
            ret = e.get_value()
            return ret

    # @abstractmethod
    # def compute(self, params: List[Param], env: Environment):
    #     inited_args = self.arrange_args(params)
    #     new_env: Environment = self.create_new_environment(inited_args)
    #     try:
    #         ret = self.body.evaluate(new_env)
    #         return ret
    #     except ReturnCommand as e:
    #         ret = e.get_value()
    #         return ret


@RObj.register_r_obj
class CallObj(RObj):
    def get_default_class(self):
        return RObj.get_r_obj('Atomic')('call', types.CharacterType())

    def __init__(self, base_obj, items: List[RObj]):
        super(CallObj, self).__init__(types.LanguageType())
        self.base_obj: RObj = base_obj
        self.items: List[RObj] = items
        self.as_from_lang = False

    def show_self(self):
        base_val = self.base_obj.show_self()

        if self.as_from_lang:
            return base_val

        itms = []
        for item in self.items:
            val_item = item.show_self()
            itms.append(val_item)
        ret = base_val + '(' + ', '.join(itms) + ')'
        return ret

    show_self_for_print = show_self

    @staticmethod
    def create(base_obj, items: List[RObj]):
        ret = CallObj(base_obj, items)
        return ret

    @staticmethod
    def create_from_lang_obj(lang_obj: RObj):
        ret = CallObj(lang_obj, [])
        ret.as_from_lang = True
        return ret

    # def evaluate(self, env: Environment):
    #     return self

    def exception_occurred(self, e: RError):
        pass

    def evaluate(self, env: Environment):
        if self.as_from_lang:
            try:
                return self.base_obj.compute(env)
            except errors.R_RuntimeError as e:
                r = RError.create_simple(self, e.message)
                if not self.exception_occurred(r):
                    raise r

        if self.base_obj.get_type().name == 'symbol':
            fun: FunctionObj = env.find_function(self.base_obj.name)
            if not isinstance(fun, FunctionObj):
                raise RError.create_simple(self, errors.ApplyToNonFunction().message)
        else:
            fun: FunctionObj = self.base_obj.evaluate(env)
            if not isinstance(fun, FunctionObj):
                raise errors.ApplyToNonFunction()

        args = []

        assg_obj = RObj.get_r_obj('AssignObj')

        for item in self.items:
            if isinstance(item, DotsObj):
                args.extend(item.items)
            elif isinstance(item, Atomic):
                n = VectorObj.create([VectorItem(None, item)])
                args.append(Param(None, n))
            elif isinstance(item, assg_obj):
                if item.item.get_type().name == 'symbol':
                    name = item.item.name
                elif isinstance(item.item, Atomic):
                    if item.item.get_type().name == 'character':
                        name = item.item[0]
                    else:
                        raise RError.create_simple(self, errors.InvalidLeftHandAssignment().message)
                else:
                    raise RError.create_simple(self, errors.InvalidLeftHandAssignment().message)
                arg = Param(name, item.value.evaluate(env))
                args.append(arg)
            else:
                arg = Param(None, item.evaluate(env))
                args.append(arg)
            #     if item.mode == 'plain':
            #         if item.item.get_type().name == 'symbol':
            #             name = item.item.name
            #         elif isinstance(item.item, Atomic):
            #             if item.item.get_type().name == 'character':
            #                 name = item.item[0]
            #             else:
            #                 raise errors.InvalidLeftHandAssignment()
            #         else:
            #             raise errors.InvalidLeftHandAssignment()
            #         arg = Param(name, item.value.evaluate(env))
            #         args.append(arg)
            #     else:
            #         arg = Param(None, item.evaluate(env))
            #         args.append(arg)
            # else:
            #     arg = Param(None, item.evaluate(env))
            #     args.append(arg)

        try:
            res = func_args_arrange(args, fun.input_args)
            new_env: Environment = Environment(env)
            for name, val in res.items():
                new_env.add(name, val)
            ret = fun.compute(new_env)
            return ret
        except errors.R_RuntimeError as e:
            r = RError.create_simple(self, e.message)
            if not self.exception_occurred(r):
                raise r


# @RObj.register_r_obj
# class LanguageCallObj(RObj):
#     def get_default_class(self):
#         return RObj.get_r_obj('Atomic')('call', types.CharacterType())
#
#     def __init__(self, lang_obj):
#         super(LanguageCallObj, self).__init__(types.LanguageType())
#         self.lang_obj: RObj = lang_obj
#
#     def show_self(self):
#         obj_val = self.lang_obj.show_self()
#         return obj_val
#
#     show_self_for_print = show_self
#
#     @staticmethod
#     def create(lang_obj: RObj):
#         return LanguageCallObj(lang_obj)
#
#     def evaluate(self, env: Environment):
#         return self
#
#     def exception_occurred(self, e: RError):
#         pass
#
#     def compute(self, env: Environment):
#         return self.lang_obj.compute(env)
        # if self.base_obj.get_type().name == 'symbol':
        #     fun: FunctionObj = env.find_function(self.base_obj.name)
        # else:
        #     fun: FunctionObj = self.base_obj.evaluate(env)
        #     if not isinstance(fun, FunctionObj):
        #         raise errors.ApplyToNonFunction()
        #
        # args = []
        #
        # assg_obj = RObj.get_r_obj('AssignObj')
        #
        # for item in self.items:
        #     # item_val = item.evaluate(env)
        #     if isinstance(item, DotsObj):
        #         args.extend(item.items)
        #     elif isinstance(item, Atomic):
        #         n = VectorObj.create([VectorItem(None, item)])
        #         args.append(Param(None, n))
        #     elif isinstance(item, assg_obj):
        #         if item.mode == 'plain':
        #             if item.item.get_type().name == 'symbol':
        #                 name = item.item.name
        #             elif isinstance(item.item, Atomic):
        #                 if item.item.get_type().name == 'character':
        #                     name = item.item[0]
        #                 else:
        #                     raise errors.InvalidLeftHandAssignment()
        #             else:
        #                 raise errors.InvalidLeftHandAssignment()
        #             arg = Param(name, item.value.evaluate(env))
        #             args.append(arg)
        #         else:
        #             arg = Param(None, item.evaluate(env))
        #             args.append(arg)
        #     else:
        #         arg = Param(None, item.evaluate(env))
        #         args.append(arg)
        #
        # try:
        #     ret = fun.compute(args, env)
        # except errors.R_RuntimeError as e:
        #     r = RError.create_simple(self, e.message)
        #     if not self.exception_occurred(r):
        #         raise r
        # return ret


