from R.Environment import Environment, ReturnCommand
from R.RObj import RObj, Param, Arg, RError
from typing import List, Tuple, Dict
import R.Types as types
import R.RuntimeErrors as errors
from abc import abstractmethod
from R.AtomicObjs import DotsObj, Atomic, SymbolObj, EmptyParamObj, VectorItem, VectorObj


def func_args_arrange(fun_params: List[Param], fun_args: List[Arg]) -> Dict[str, RObj]:
    args_res = {arg.name: arg.value for arg in fun_args}

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

    has_dots_obj = len(list(filter(lambda arg: arg.name == '...', fun_args))) != 0

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
                    res[arg_name] = param[1]

    return res


@RObj.register_r_obj
class FunctionObj(RObj):
    def __init__(self, input_args, body: RObj):
        super(FunctionObj, self).__init__(types.ClosureType())
        self.input_args: List[Arg] = input_args
        self.body = body

    def show_self(self):
        pass

    # объект call создает список аргументов и передает их сюда
    @staticmethod
    def create(input_args: List[Arg]):
        return FunctionObj(input_args)

    def evaluate(self, env: Environment):
        return self

    def arrange_args(self, params: List[Param]):
        ret = func_args_arrange(params, self.input_args)
        return ret

    @staticmethod
    def create_new_environment(initialized_args: Dict[str, RObj], env: Environment):
        new_env: Environment = Environment(env)
        for name, val in initialized_args.items():
            val_val = val.evaluate(new_env)
            new_env.add(name, val_val)
        return new_env

    @abstractmethod
    def compute(self, params: List[Param], env: Environment):
        inited_args = self.arrange_args(params)
        new_env: Environment = self.create_new_environment(inited_args)
        try:
            ret = self.body.evaluate(new_env)
            return ret
        except ReturnCommand as e:
            ret = e.get_value()
            return ret

@RObj.register_r_obj
class CallObj(RObj):
    def __init__(self, base_obj, items: List[RObj]):
        super(CallObj, self).__init__(types.LanguageType())
        self.base_obj = base_obj
        self.items = items


    def show_self(self):
        pass

    @staticmethod
    def create(base_obj, items: List[RObj]):
        return CallObj(base_obj, items)

    def evaluate(self, env: Environment):
        return self

    def exception_occurred(self, e: RError):
        pass

    def compute(self, env: Environment):
        if self.base_obj.get_type().name == 'symbol':
            fun: FunctionObj = env.find_function(self.base_obj.name)
        else:
            fun: FunctionObj = self.base_obj.evaluate(env)
            if not isinstance(fun, FunctionObj):
                raise errors.ApplyToNonFunction()

        args = []

        assg_obj = RObj.get_r_obj('AssignObj')

        for item in self.items:
            # item_val = item.evaluate(env)
            if isinstance(item, DotsObj):
                args.extend(item.items)
            elif isinstance(item, Atomic):
                n = VectorObj.create([VectorItem(None, item)])
                args.append(Param(None, n))
            elif isinstance(item, assg_obj):
                if item.mode == 'plain':
                    if item.item.get_type().name == 'symbol':
                        name = item.item.name
                    elif isinstance(item.item, Atomic):
                        if item.item.get_type().name == 'character':
                            name = item.item.value
                        else:
                            raise errors.InvalidLeftHandAssignment()
                    else:
                        raise errors.InvalidLeftHandAssignment()
                    arg = Param(name, item.value.evaluate(env))
                    args.append(arg)
                else:
                    arg = Param(None, item.evaluate(env))
                    args.append(arg)
            else:
                arg = Param(None, item.evaluate(env))
                args.append(arg)

        try:
            ret = fun.compute(args, env)
        except errors.R_RuntimeError as e:
            r = RError(self, e.message)
            if not self.exception_occurred(r):
                raise r
        return ret



