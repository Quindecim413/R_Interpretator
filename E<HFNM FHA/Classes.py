from typing import List

class BaseClass(object):
    def __init__(self, _name, _super: List[str]=list()):
        self._name = _name
        self._super = _super


class VectorClass(BaseClass):
    def __init__(self):
        super(VectorClass, self).__init__('vector', [])


class LogicalClass(BaseClass):
    def __init__(self):
        super(LogicalClass, self).__init__('logical', ['vector'])


class NumericClass(BaseClass):
    def __init__(self):
        super(NumericClass, self).__init__('numeric', ['vector'])


class IntegerClass(BaseClass):
    def __init__(self):
        super(IntegerClass, self).__init__('integer', ['vector'])


class CharacterClass(BaseClass):
    def __init__(self):
        super(CharacterClass, self).__init__('character', ['vector'])


class ListClass(BaseClass):
    def __init__(self):
        super(ListClass, self).__init__('list', ['vector'])


class MatrixClass(BaseClass):
    def __init__(self):
        super(MatrixClass, self).__init__('matrix', ['vector'])


class ArrayClass(BaseClass):
    def __init__(self):
        super(ArrayClass, self). __init__('array', ['vector'])


class FunctionClass(BaseClass):
    def __init__(self):
        super(FunctionClass, self).__init__('function', [])


class NameClass(BaseClass):
    def __init__(self):
        super(NameClass, self).__init__('name', [])


class SuiteClass(BaseClass):
    def __init__(self):
        super(SuiteClass, self).__init__('{', [])

class WhileClass(BaseClass):
    def __init__(self):
        super(WhileClass, self).__init__('while', [])

class ForClass(BaseClass):
    def __init__(self):
        super(ForClass, self).__init__('for', [])

# for repeat and operators executing
class CallClass(BaseClass):
    def __init__(self):
        super(CallClass, self).__init__('call', [])

