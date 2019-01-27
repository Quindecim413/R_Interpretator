from R.Environment import Environment
import R.RObj
import R.BuiltIn as builtin
from R.Function import FunctionObj, CallObj, Atomic, Arg
import R.AtomicObjs as objs
import R.Types as types
import R.LanguageObjs as language


this_env: Environment = Environment(builtin.built_in_env)
this_env.set_global(this_env)
print('123')

items1 = [
    language.AssignObj.create(objs.SymbolObj('h'), Atomic.create(1, types.IntegerType())),
    Atomic.create(2, types.IntegerType()),
    Atomic.create(5, types.IntegerType())
]


items2 = [
    Atomic.create(False, types.LogicalType()),
    language.AssignObj.create(objs.SymbolObj('f'), Atomic.create(1, types.IntegerType())),
    Atomic.create(5, types.IntegerType()),
    language.AssignObj.create(objs.SymbolObj('h'), Atomic.create(1, types.IntegerType()))
]


symbol_c = objs.SymbolObj('c')

c_call1 = CallObj(symbol_c, items1)
vect1 = c_call1.evaluate(this_env)

print(vect1.show_self())


c_call2 = CallObj(symbol_c, items2)
vect2 = c_call2.evaluate(this_env)

print(vect2.show_self())

and_obj = language.AndObj.create(vect1, vect2).evaluate(this_env)

symbol_k = objs.SymbolObj('k')

symbol_t = objs.SymbolObj('t')

assign_ob = language.AssignObj.create(symbol_k, items1[1])
# assign_ob2 = language.AssignObj(symbol_t, items2, )

res = assign_ob.evaluate(this_env)

res2 = language.AndAndObj.create(vect1, vect1).evaluate(this_env)

print(res.show_self())

print(res2.show_self())
#
r1 = language.PowerObj.create(res, res2).evaluate(this_env)

res3 = CallObj(objs.SymbolObj('^'), [res, res2]).evaluate(this_env)

print('r1')
print(r1.show_self())
print(res2.show_self())
print(res3.show_self())

print(res3.show_self())

symbol_c = objs.SymbolObj('c')

vec_2 = Atomic.create(5, types.IntegerType(), is_neg=True) ## 2L
vec_3 = Atomic.create(0, types.DoubleType(), is_neg=True)  ## 3

vec_4 = CallObj(symbol_c, [vec_2, vec_3, vec_2, vec_3]).evaluate(this_env)

r = CallObj(objs.SymbolObj('/'), [vec_2, vec_4], ).evaluate(this_env)


# 2 / 3

print(vec_2.show_self())
print(vec_4.show_self())
print('res')
print(r.show_self())

k = 0


