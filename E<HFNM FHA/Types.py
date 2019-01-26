class BaseType(object):
    def __init__(self, _name):
        self._name = _name


class DoubleType(BaseType):
    def __init__(self):
        super(DoubleType, self).__init__('double')


class IntegerType(BaseType):
    def __init__(self):
        super(IntegerType, self).__init__('integer')


class LogicalType(BaseType):
    def __init__(self):
        super(LogicalType, self).__init__('logical')





# for closures and functions
class ClosureType(BaseType):
    def __init__(self):
        super(ClosureType, self).__init__('closure')


# такой тип выставляется у объекта переменная
class SymbolType(BaseType):
    def __init__(self):
        super(SymbolType, self).__init__('symbol')

