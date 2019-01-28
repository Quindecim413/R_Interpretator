from R.RObj import RObj
from R.Environment import Environment, CommandException
from R.RuntimeErrors import R_RuntimeError
from R.RObj import RError, execute_item
from R.Function import Param, arrange_params_with_function_args
from typing import List


class Executor(object):
    def __init__(self, items: List[RObj], standard_output):
        self.items = items
        self.standard_output = standard_output

    @staticmethod
    def create(items: List[RObj], standard_output_fun):
        return Executor(items, standard_output_fun)

    def evaluate(self, env: Environment):
        standart_for_env = env.standart_output
        env.standart_output = self.standard_output
        try:
            for item in self.items:
                val = item.show_self()
                self.standard_output('> '+val)
                res: RObj = execute_item(item, env)
                func = env.find_function('print', classes_names=res.get_classes_as_python_list())
                try:
                    new_env = arrange_params_with_function_args([Param('x', res)], func, env)
                    func.compute(new_env)
                except Exception as e:
                    self.standard_output(str(e))
                # self.standard_output(res.show_self())
        except CommandException as e:
            self.standard_output(e.message)
        except R_RuntimeError as e:
            self.standard_output(e.message)
        except RError as e:
            func = env.find_function('print')
            try:
                new_env = arrange_params_with_function_args([Param('x', e)], func, env)
                func.compute(new_env)
            except Exception as e:
                self.standard_output(str(e))
        except Exception as e:
            print(e)
            raise
        finally:
            env.standart_output = standart_for_env
            return None
