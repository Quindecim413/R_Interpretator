class BaseType(object):
    def __init__(self, _name):
        self._name = _name

    @property
    def name(self):
        return self._name

class NoType(BaseType):
    def __init__(self):
        super(NoType, self).__init__('no-type')


class DoubleType(BaseType):
    def __init__(self):
        super(DoubleType, self).__init__('double')


class IntegerType(BaseType):
    def __init__(self):
        super(IntegerType, self).__init__('integer')


class LogicalType(BaseType):
    def __init__(self):
        super(LogicalType, self).__init__('logical')


class CharacterType(BaseType):
    def __init__(self):
        super(CharacterType, self).__init__('character')

class ListType(BaseType):
    def __init__(self):
        super(ListType, self).__init__('list')


class NAType(BaseType):
    def __init__(self):
        super(NAType, self).__init__('NA')


class NULLType(BaseType):
    def __init__(self):
        super(NULLType, self).__init__('NULL')


class DotsType(BaseType):
    def __init__(self):
        super(DotsType, self).__init__('Dots')


# for closures and functions
class ClosureType(BaseType):
    def __init__(self):
        super(ClosureType, self).__init__('closure')


class BuiltInType(BaseType):
    def __init__(self):
        super(BuiltInType, self).__init__('builtin')


# такой тип выставляется у объекта переменная
class SymbolType(BaseType):
    def __init__(self):
        super(SymbolType, self).__init__('symbol')


class LanguageType(BaseType):
    def __init__(self):
        super(LanguageType, self).__init__('language')
