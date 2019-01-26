# from parsimonious.grammar import Grammar
#
#
# gr = open('test_grammar.peg').read()
# grammar = Grammar(gr)
#
#
# inp = open('test.r').read()
# parse_tree = grammar.parse(inp)
#
# k=0

class NoClassRegistered(Exception):
    def __init__(self, class_name):
        super(NoClassRegistered, self).__init__("No class {} registered".format(class_name))

class Base(object):
    subs = []

    @classmethod
    def addsub(cls, before=None):
        def inner(subclass):
            if before and before in cls.subs:
                cls.subs.insert(cls.subs.index(before), subclass)
            else:
                cls.subs.append(subclass)
            return subclass
        return inner

    # @classmethod
    # def get_class_by_name(cls, name):
    #
    #     for
    #
    #     raise NoClassRegistered(name)
    #
    # def create(self):
    #     sub3 = subs



@Base.addsub()
class Sub1(Base):
    @staticmethod
    def create():
        print('sub1')

class Sub2(Base):
    pass

@Base.addsub(before=Sub1)
class Sub3(Base):
    pass


Base.subs[1].create()

t = Base.subs[0].__name__
a = type(Sub3)
# a.__init__()
k= 0

o1 = type('X', (object,), dict(a='Foo', b=12))

print(type(o1))
print(vars(o1))


class test:
    a = 'Foo'
    b = 12


o2 = type('Y', (test,), dict(a='Foo', b=12))
print(type(o2))
print(vars(o2))
# from abc import abstractmethod
#
#
# class Base(object):  # New-style class (i.e. explicitly derived from object).
#
#     @classmethod
#     def register_subclass(cls, subclass):
#         """ Class decorator for registering subclasses. """
#
#         # Replace any occurrences of the class name in the class' subs list.
#         # with the class itself.
#         # Assumes the classes in the list are all subclasses of this one.
#         # Works because class decorators are called *after* the decorated class'
#         # initial creation.
#         while subclass.__name__ in cls.subs:
#             cls.subs[cls.subs.index(subclass.__name__)] = subclass
#
#         return subclass  # Return modified class.
#
#     @abstractmethod
#     def do_print(self, message):
#         pass
#
#     subs = ['Sub3', 'Sub1']  # Ordered list of subclass names.
#
#
# @Base.register_subclass
# class Sub1(Base):
#     def do_print(self, message):
#         print("Sub1" + message)
#
#
# @Base.register_subclass
# class Sub2(Base): pass
#
# @Base.register_subclass
# class Sub3(Base): pass
#
# print('Base.subs: {}'.format(Base.subs))
#
# sub1 = Sub1().do_print("abc")

