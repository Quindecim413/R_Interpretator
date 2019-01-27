from parse_tree_visitor import ASTNode

from R.Environment import Environment
import R.RObj
import R.BuiltIn as builtin
from R.Function import FunctionObj, CallObj, Atomic, Arg
import R.AtomicObjs as atomics
import R.Types as types
import R.LanguageObjs as language
import R.Function as func
import R.RuntimeErrors as errors

Verbose = True


class OperandNotSupportedYet(Exception):
    def __init__(self, desc):
        super(Exception, self).__init__(desc)


class Start(ASTNode):
    def __init__(self, children, start, end):
        self.children = children
        super().__init__('start', start, end)

    def __repr__(self, level=0):
        ret = '\n'.join([ch.__repr__(level) for ch in self.children])
        return ret

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return Start(children, start, end)

    def evaluate(self):
        res = []
        for child in self.children:
            r = child.evaluate()
            res.append(r)
        return res

class list_of_inputs(ASTNode):
    @classmethod
    def create(cls, value, children, start, end):
        return children

    def evaluate(self, env):
        pass

class suite(ASTNode):
    def __init__(self, children, start, end):
        self.children = children
        super().__init__('suite', start, end)

    def __repr__(self, level=0):
        # chn = [str(ch) for ch in self.children]
        # chn = ['\n'.join([(' ' + l) for l in ch.split('\n')]) for ch in chn]
        # ret = '{' + '\n'.join(chn) + '\n}'
        # return ret
        ret = ' '*level+'block\n' + ('\n'.join([ch.__repr__(level+1) for ch in self.children]) if len(self.children) > 0
                                                else ' '*(level+1) + 'empty')
        return ret

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return suite(children, start, end)

    def evaluate(self):
        res = []
        for child in self.children:
            r = child.evaluate()
            res.append(r)
        return language.SuiteObj.create(res)

class break_stmt(ASTNode):
    def __repr__(self, level=0):
        return ' '*level + 'break'

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return break_stmt('break', start, end)

    def evaluate(self):
        return language.BreakObj.create()

class next_stmt(ASTNode):
    def __repr__(self, level=0):
        return ' '*level + 'next'

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return next_stmt('next', start, end)

    def evaluate(self):
        return language.NextObj.create()

class compound_stmt(ASTNode):
    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return children[0]

    def evaluate(self):
        pass

class repeat_stmt(ASTNode):
    def __init__(self, body, start, end):
        self.body = body
        super().__init__('repeat', start, end)

    def __repr__(self, level=0):
        ret = ' '*level+'repeat\n' + self.body.__repr__(level+1)
        return ret

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return repeat_stmt(children[0], start, end)

    def evaluate(self):
        res_body = self.body.evaluate()
        return language.RepeatLoopObj.create(res_body)



class for_stmt(ASTNode):
    def __init__(self, variable, argument, body, start, end):
        super().__init__('for_loop', start, end)
        self.variable = variable
        self.argument = argument
        self.body = body

    def __repr__(self, level=0):
        ret = ' '*level + 'for\n'+ ' '*(level+1) + 'variable\n' + self.variable.__repr__(level+2) + \
              '\n' + ' '*(level+1) + 'argument\n' + self.argument.__repr__(level+2) + \
              '\n' + ' ' * (level + 1)+'body\n' + self.body.__repr__(level+2)
        return ret

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return for_stmt(children[0], children[1], children[2], start, end)

    def evaluate(self):
        val_var = self.variable.evaluate()
        val_arg = self.argument.evaluate()
        val_body = self.body.evaluate()
        return language.ForLoopObj.create(val_var, val_arg, val_body)

class while_stmt(ASTNode):
    def __init__(self, _argument, body, start, end):
        super().__init__('while_loop', start, end)
        self.argument = _argument
        self.body = body

    def __repr__(self, level=0):
        ret = ' '*level+'while\n'+' '*(level+1) + 'argument\n' + self.argument.__repr__(level+2) + \
              '\n' + ' ' * (level+1) + 'body\n'+self.body.__repr__(level+2)
        return ret

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return while_stmt(children[0], children[1], start, end)

    def evaluate(self):
        val_arg = self.argument.evaluate()
        val_body = self.body.evaluate()
        return language.WhileObj.create(val_arg, val_body)

class if_stmt(ASTNode):
    def __init__(self, condition, body, alterbody, start, end):
        self.condition = condition
        self.alterbody = alterbody
        self.body = body
        super().__init__('if_stmt', start, end)

    def __repr__(self, level=0):
        ret = ' ' * level + 'if\n' + ' ' * (level + 1) + 'condition\n' + self.condition.__repr__(level + 2) +\
              '\n' + ' ' * (level + 1) + 'body\n' + self.body.__repr__(level + 2)+\
              ('\n' + ' ' * (level + 1) + 'alterbody\n' + self.alterbody.__repr__(level+2) if self.alterbody else '')
        return ret

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return if_stmt(children[0], children[1], children[2] if len(children) > 2 else None, start, end)

    def evaluate(self):
        val_arg = self.condition.evaluate()
        val_body = self.body.evaluate()
        val_alterbody = self.alterbody.evaluate() if self.alterbody is not None else None
        return language.IfElseObj.create(val_arg, val_body, val_alterbody)



# class EmptyASTNode(ASTNode):
#     def __init__(self):
#         super().__init__('empty', 0, 0)
#
#     def __repr__(self, level=0):
#         return ' ' * level+'block\n' + ' '*(level + 1) + '--//--'
#
#     __str__ = __repr__
#
#     @classmethod
#     def create(cls, value, children, start, end):
#         if not Verbose:
#             print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
#         return None
#
#     def evaluate(self):
#         raise OperandNotSupportedYet('EmptyAstNode')

# class condition_stmt(ASTNode):
#     def __init__(self, if_else_clause, start, end):
#         self.if_else_clause = if_else_clause
#         super().__init__('condition_stmt', start, end)
#
#     def __repr__(self, level=0):
#         ret = self.if_else_clause.__repr__(level)
#         return ret
#
#     __str__ = __repr__
#
#     @classmethod
#     def create(cls, value, children, start, end):
#         # if children[len(children) - 1].name != 'suite':
#         #     children.append(EmptyASTNode())
#         #
#         # ind = len(children)
#         # ch = children
#         # next_if_else_clause = if_else_stmt(ch[ind - 2].condition, ch[ind - 2].body,
#         #                                    ch[ind - 1],
#         #                                    ch[ind - 2].start, ch[ind - 2].end)
#         # for i in reversed(range(ind - 2)):
#         #     next_if_else_clause = if_else_stmt(ch[i].condition, ch[i].body,
#         #                                        next_if_else_clause,
#         #                                        ch[i].start, ch[i].end)
#         # if not Verbose:
#         #     print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
#         # return condition_stmt(next_if_else_clause, start, end)
#         return children
#
#     def evaluate(self, env):
#         pass

class or_expr(ASTNode):
    def __init__(self, left, right, or_op, start, end):
        super().__init__('or_expr', start, end)

        self.or_op = or_op
        if len(left) == 1:
            self.left = left[0]
        else:
            self.left = or_expr(left[:-2], left[len(left) - 1], left[len(left) - 2], start, end)
        self.right = right

    def __repr__(self, level=0):
        l = self.left.__repr__(level + 2)
        r = self.right.__repr__(level + 2)
        ret = ' ' * level + str(self.or_op) + '\n' + ' ' * (level + 1) + 'left\n' + l + \
              '\n' + ' ' * (level + 1) + 'right\n' + r
        return ret

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        if len(children) == 1:
            return children[0]
        return or_expr(children[:-2], children[len(children) - 1], children[len(children) - 2], start, end)

    def evaluate(self):
        val_left = self.left.evaluate()
        val_right = self.right.evaluate()

        if self.or_op.value == '||':
            return language.OrOrObj.create(val_left, val_right)
        else:
            return language.OrObj.create(val_left, val_right)


class and_expr(ASTNode):
    def __init__(self, left, right, and_op, start, end):
        super().__init__('and_expr', start, end)

        self.and_op = and_op
        if len(left) == 1:
            self.left = left[0]
        else:
            self.left = and_expr(left[:-2], left[len(left) - 1], left[len(left) - 2], start, end)
        self.right = right

    def __repr__(self, level=0):
        l = self.left.__repr__(level + 2)
        r = self.right.__repr__(level + 2)
        ret = ' ' * level + str(self.and_op) + '\n' + ' ' * (level + 1) + 'left\n' + l + \
              '\n' + ' ' * (level + 1) + 'right\n' + r
        return ret

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        if len(children) == 1:
            return children[0]
        return and_expr(children[:-2], children[len(children) - 1], children[len(children) - 2], start, end)

    def evaluate(self):
        val_left = self.left.evaluate()
        val_right = self.right.evaluate()

        if self.and_op.value == '&&':
            return language.AndAndObj.create(val_left, val_right)
        else:
            return language.AndObj.create(val_left, val_right)


class not_expr(ASTNode):
    def __init__(self, negating_expr, start, end):
        self.negating_expr = negating_expr
        super().__init__('not_expr', start, end)

    def __repr__(self, level=0):
        ret = ' ' * level + 'not\n' + self.negating_expr.__repr__(level+1)
        return ret

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        if len(children) == 1:
            return children[0]
        return not_expr(children[1], start, end)

    def evaluate(self):
        val = self.negating_expr.evaluate()
        return language.NotObj.create(val)

class compare_expr(ASTNode):
    def __init__(self, left, right, comp_op, start, end):
        self.compare_op = comp_op
        self.left = left
        self.right = right
        super().__init__('compare_expr', start, end)

    def __repr__(self, level=0):
        l = self.left.__repr__(level+2)
        r = self.right.__repr__(level+2)
        ret = ' ' * level + str(self.compare_op) + '\n' + ' ' * (level + 1) + 'left\n' + l + \
              '\n' + ' ' * (level + 1) + 'right\n' + r
        return ret

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        if len(children) == 1:
            return children[0]
        return compare_expr(children[0], children[2], children[1], start, end)

    def evaluate(self):

        val_left = self.left.evaluate()
        val_right = self.right.evaluate()

        if self.compare_op.value == '==':
            return language.EqualObj.create(val_left, val_right)
        elif self.compare_op.value == '!=':
            return language.NotEqualObj.create(val_left, val_right)
        elif self.compare_op.value == '<':
            return language.LessObj.create(val_left, val_right)
        elif self.compare_op.value == '<=':
            return language.LessOrEqualObj.create(val_left, val_right)
        elif self.compare_op.value == '>':
            return language.GreaterObj.create(val_left, val_right)
        elif self.compare_op.value == '>=':
            return language.GreaterOrEqualObj.create(val_left, val_right)
        else:
            raise Exception('invalid compare_op value - {}'.format(self.compare_op.value))


class arith_expr(ASTNode):
    def __init__(self, left, right, arith_op, start, end):
        self.arith_op = arith_op
        if len(left) == 1:
            self.left = left[0]
        else:
            self.left = arith_expr(left[:-2], left[len(left)-1], left[len(left)-2], start, end)
        self.right = right
        super().__init__('arith_expr', start, end)

    def __repr__(self, level=0):
        l = self.left.__repr__(level + 2)
        r = self.right.__repr__(level + 2)
        ret = ' ' * level + str(self.arith_op) + '\n' + ' ' * (level + 1) + 'left\n' + l + \
              '\n' + ' ' * (level + 1) + 'right\n' + r
        return ret

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' + str(children))
        if len(children) == 1:
            return children[0]
        return arith_expr(children[:-2], children[len(children) - 1], children[len(children) - 2], start, end)

    def evaluate(self):
        val_left = self.left.evaluate()
        val_right = self.right.evaluate()

        if self.arith_op.value == '+':
            return language.AddObj.create(val_left, val_right)
        else:
            return language.SubtractObj.create(val_left, val_right)


class term(ASTNode):
    def __init__(self, left, right, term_op, start, end):
        self.term_op = term_op
        if len(left) == 1:
            self.left = left[0]
        else:
            self.left = term(left[:-2], left[len(left)-1], left[len(left)-2], start, end)
        self.right = right
        super().__init__('term', start, end)

    def __repr__(self, level=0):
        l = self.left.__repr__(level + 2)
        r = self.right.__repr__(level + 2)
        ret = ' ' * level + str(self.term_op) + '\n' + ' ' * (level + 1) + 'left\n' + l + \
              '\n' + ' ' * (level + 1) + 'right\n' + r
        return ret

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        if len(children) == 1:
            return children[0]
        return term(children[:-2], children[len(children) - 1], children[len(children) - 2], start, end)

    def evaluate(self):
        val_left = self.left.evaluate()
        val_right = self.right.evaluate()

        if self.term_op.value == '*':
            return language.MultiplyObj.create(val_left, val_right)
        else:
            return language.DivideObj.create(val_left, val_right)


class special_term(ASTNode):
    def __init__(self, left, right, user_op, start, end):
        self.user_op = user_op
        if len(left) == 1:
            self.left = left[0]
        else:
            self.left = special_term(left[:-2], left[len(left)-1], left[len(left)-2], start, end)
        self.right = right
        super().__init__('special_term', start, end)

    def __repr__(self, level=0):
        l = self.left.__repr__(level + 2)
        r = self.right.__repr__(level + 2)
        ret = ' ' * level + str(self.user_op) + '\n' + ' ' * (level + 1) + 'left\n' + l + \
              '\n' + ' ' * (level + 1) + 'right\n' + r
        return ret

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        if len(children) == 1:
            return children[0]
        return special_term(children[:-2], children[len(children) - 1], children[len(children) - 2], start, end)

    def evaluate(self):
        val_left = self.left.evaluate()
        val_right = self.right.evaluate()

        return language.SpecialObj.create(val_left, val_right, self.user_op.value)


class sequence_term(ASTNode):
    def __init__(self, left, right, start, end):
        self.left = left
        self.right = right
        super().__init__('sequence_term', start, end)

    def __repr__(self, level=0):
        l = self.left.__repr__(level + 2)
        r = self.right.__repr__(level + 2)
        ret = ' ' * level + ':' + '\n' + ' ' * (level + 1) + 'left\n' + l + \
              '\n' + ' ' * (level + 1) + 'right\n' + r
        return ret

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        if len(children) == 1:
            return children[0]
        return sequence_term(children[0], children[2], start, end)

    def evaluate(self):
        val_left = self.left.evaluate()
        val_right = self.right.evaluate()

        return language.SequenceObj.create(val_left, val_right)


class factor(ASTNode):
    def __init__(self, plus_min_op, child, start, end):
        self.plus_min_op = plus_min_op
        self.child = child
        super().__init__('factor', start, end)

    def __repr__(self, level=0):
        v = self.child.__repr__(level + 1)
        ret = ' ' * level + str(self.plus_min_op) + '\n'  + v
        return ret

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        if len(children) == 1:
            return children[0]
        return factor(children[0], children[1], start, end)

    def evaluate(self):
        val_child = self.child.evaluate()

        if self.plus_min_op.value == '+':
            return language.AddUnaryObj.create(val_child)
        else:
            return language.SubtractUnaryObj.create(val_child)


class power(ASTNode):
    def __init__(self, left, right, user_op, start, end):
        self.user_op = user_op
        if len(left) == 1:
            self.left = left[0]
        else:
            self.left = power(left[:-2], left[len(left)-1], left[len(left)-2], start, end)
        self.right = right
        super().__init__('special_term', start, end)

    def __repr__(self, level=0):
        l = self.left.__repr__(level + 2)
        r = self.right.__repr__(level + 2)
        ret = ' ' * level + '^' + '\n' + ' ' * (level + 1) + 'left\n' + l + \
              '\n' + ' ' * (level + 1) + 'right\n' + r
        return ret

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        if len(children) == 1:
            return children[0]
        return power(children[:-2], children[len(children) - 1], children[len(children) - 2], start, end)

    def evaluate(self):
        val_left = self.left.evaluate()
        val_right = self.right.evaluate()

        return language.PowerObj.create(val_left, val_right)

class element(ASTNode):
    def __init__(self, item, _trailer, start, end):
        if len(_trailer) == 0:
            self.item = item
        else:
            trail = _trailer[0]
            trail.item = item
            self.item = element(trail, _trailer[1:], start, end).item
            k=0



        super().__init__('element', start, end)

    def __repr__(self, level=0):
        return self.item.__repr__(level)

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        item = element(children[0], children[1:] if len(children) >1 else [], start, end)

        return item.item

    def evaluate(self):
        pass

class simple_assign(ASTNode):
    def __init__(self, left, right, start, end):
        self.left = left
        self.right = right
        super().__init__('simple_assign', start, end)

    def __repr__(self, level=0):
        l = self.left.__repr__(level + 2)
        r = self.right.__repr__(level + 2)
        ret = ' ' * level + '=' + '\n' + ' ' * (level + 1) + 'left\n' + l + \
              '\n' + ' ' * (level + 1) + 'right\n' + r
        return ret

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return simple_assign(children[0], children[1], start, end)

    def evaluate(self):
        val_left = self.left.evaluate()
        val_right = self.right.evaluate()

        return language.AssignObj.create(val_left, val_right)

class super_left_assign(ASTNode):
    def __init__(self, left, right, start, end):
        self.left = left
        self.right = right
        super().__init__('super_left_assign', start, end)

    def __repr__(self, level=0):
        l = self.left.__repr__(level + 2)
        r = self.right.__repr__(level + 2)
        ret = ' ' * level + '<<-' + '\n' + ' ' * (level + 1) + 'left\n' + l + \
              '\n' + ' ' * (level + 1) + 'right\n' + r
        return ret

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        pass

    def evaluate(self):
        val_left = self.left.evaluate()
        val_right = self.right.evaluate()

        return language.SuperAssignObj.create(val_left, val_right)


class left_assign(ASTNode):
    def __init__(self, left, right, start, end):
        self.left = left
        self.right = right
        super().__init__('left_assign', start, end)

    def __repr__(self, level=0):
        l = self.left.__repr__(level + 2)
        r = self.right.__repr__(level + 2)
        ret = ' ' * level + '<-' + '\n' + ' ' * (level + 1) + 'left\n' + l + \
              '\n' + ' ' * (level + 1) + 'right\n' + r
        return ret

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        if isinstance(children[1], SimpleLeftAssignOp):
            return left_assign(children[0], children[2], start, end)
        return super_left_assign(children[0], children[2], start, end)

    def evaluate(self):
        val_left = self.left.evaluate()
        val_right = self.right.evaluate()

        return language.SimpleAssignObj.create(val_left, val_right)


class right_assign(ASTNode):
    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return left_assign(children[2], children[0], start, end)

    def evaluate(self):
        pass

class call(ASTNode):
    def __init__(self, arguments, start, end):
        self.arguments = arguments
        self.item = None
        super().__init__('call', start, end)

    def __repr__(self, level=0):
        chn = [ch.__repr__(level+2) for ch in self.arguments]
        chn = '\n'.join(chn)
        ret = ' '*level + 'call'+ \
              '\n' + ' ' * (level + 1) + 'item\n' + (
                  self.item.__repr__(level + 2) if self.item else ' ' * (level + 2) + 'None')+\
              '\n' + ' ' * (level + 1) + 'arguments\n' + (chn if len(self.arguments) > 0 else ' ' * (level + 2) + 'empty')
        return ret

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return call(children, start, end)

    def evaluate(self):
        val_item = self.item.evaluate()

        vals_args = []
        for arg in self.arguments:
            r = arg.evaluate()
            vals_args.append(r)

        return func.CallObj.create(val_item, vals_args)



class indexing(ASTNode):
    def __init__(self, arguments, start, end):
        self.arguments = arguments
        self.item = None
        super().__init__('indexing', start, end)

    def __repr__(self, level=0):
        chn = [ch.__repr__(level + 2) for ch in self.arguments]
        chn = '\n'.join(chn)
        ret = ' ' * level + '[]'+ \
              '\n' + ' ' * (level + 1) + 'item\n' + (
                  self.item.__repr__(level + 2) if self.item else ' ' * (level + 2) + 'None')+\
              '\n' + ' ' * (level + 1) + 'arguments\n' + (chn if len(self.arguments) > 0 else ' ' * (level + 2) + 'empty')
        return ret

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return indexing(children, start, end)

    def evaluate(self):
        val_item = self.item.evaluate()

        vals_args = []
        for arg in self.arguments:
            r = arg.evaluate()
            vals_args.append(r)

        return language.IndexingObj.create(val_item, vals_args)


class list_indexing(ASTNode):
    def __init__(self, argument, start, end):
        self.argument = argument
        self.item = None
        super().__init__('list_indexing', start, end)

    def __repr__(self, level=0):
        # ret = ' '*level + 'call\n' + self.argument.__repr__(level+1)
        ret = ' '*level + '[[]]\n'  '\n'+' '*(level+1) + 'item\n' +(self.item.__repr__(level + 2) if self.item else ' '*(level+2) + 'None')+\
              ' '*(level+1) + 'argument\n' + (self.argument.__repr__(level+2) if self.argument else ' '*(level+2) + 'empty')

        return ret

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return list_indexing(children[0] if len(children) > 0 else None, start, end)

    def evaluate(self):
        val_item = self.item.evaluate()

        val_arg = self.argument.evaluate()

        return language.SuperIndexingObj.create(val_item, val_arg)


class subname(ASTNode):
    def __init__(self, variable, start, end):
        self.variable = variable
        self.item = None
        super().__init__('subname', start, end)

    def __repr__(self, level=0):
        ret = ' '*level + '$'+'\n' + self.variable.__repr__(level+1) +\
              '\n' + ' '*(level+1) + 'item\n' + (self.item.__repr__(level + 2) if self.item else ' '*(level+2) + 'None')
        return ret

    __str__ = __repr__

    @classmethod
    def create(cls,  value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return subname(children[1], start, end)

    def evaluate(self):
        val_item = self.item.evaluate()

        val_var = self.variable.evaluate()

        return language.DLRObj.create(val_item, val_var)


class code_block(ASTNode):
    def __init__(self, children, start, end):
        self.children = children
        super().__init__('suite', start, end)

    def __repr__(self, level=0):
        ret = ' '*level+'block\n' + \
        ('\n'.join([ch.__repr__(level+1) for ch in self.children]) if len(self.children) > 0 else ' '*(level+1)+'empty')
        return ret

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return code_block(children, start, end)

    def evaluate(self):
        res = []
        for child in self.children:
            r = child.evaluate()
            res.append(r)
        return language.SuiteObj.create(res)


class funcdef(ASTNode):
    def __init__(self, arguments, body, start, end):
        self.arguments = arguments
        self.body = body
        super().__init__('func_def', start, end)

    def __repr__(self, level=0):
        chn = [ch.__repr__(level+2) for ch in self.arguments if ch]
        ret = ' '*level + 'func_def\n' + \
              ' '*(level+1) + 'arguments\n' + '\n'.join(chn) + \
              '\n' + ' '*(level + 1) + 'body\n' + self.body.__repr__(level+2)
        return ret

    __str__ = __repr__

    @classmethod
    def create(cls,  value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return funcdef(children[:-1], children[len(children)-1], start, end)

    def evaluate(self):
        args = []
        for arg in self.arguments:
            r = arg.evaluate()
            args.append(r)

        val_body = self.body.evaluate()

        return func.FunctionObj.create(args, val_body)


class optional_param(ASTNode):
    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return simple_assign.create(value, children, start, end)

    def evaluate(self):
        pass


#tokens
class Logical(ASTNode):
    def __init__(self, value, start, end):
        self.value = value
        super().__init__('Logical', start, end)

    def __repr__(self, level=0):
        return ' '*level + 'Logical\n' + ' '*(level + 1) + str(self.value)

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return Logical(value, start, end)

    def evaluate(self):
        return language.Atomic.create(True if self.value == 'TRUE' else False, types.LogicalType())

class Numeric(ASTNode):
    def __init__(self, value, start, end):
        self.value = value
        super().__init__('Numeric', start, end)

    def __repr__(self, level=0):
        return ' ' * level + 'Numeric\n' + ' ' * (level + 1) + str(self.value)

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return Numeric(value, start, end)

    def evaluate(self):
        return language.Atomic.create(float(self.value), types.DoubleType())

class Integer(ASTNode):
    def __init__(self, value, start, end):
        self.value = value
        super().__init__('Integer', start, end)

    def __repr__(self, level=0):
        return ' ' * level + 'Integer\n' + ' ' * (level + 1) + str(self.value)

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return Integer(value, start, end)

    def evaluate(self):
        return language.Atomic.create(int(self.value[:-1]), types.IntegerType())

class Complex(ASTNode):
    def __init__(self, value, start, end):
        self.value = value
        super().__init__('Complex', start, end)

    def __repr__(self, level=0):
        return ' ' * level + 'Complex\n' + ' ' * (level + 1) + str(self.value) + 'i'

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return Complex(value, start, end)

    def evaluate(self):
        raise OperandNotSupportedYet()

class Variable(ASTNode):
    def __init__(self, var_name, start, end):
        self.var_name = var_name
        super().__init__('Variable', start, end)

    def __repr__(self, level=0):
        return ' ' * level + 'Variable\n' + ' ' * (level + 1) + str(self.var_name)

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return Variable(value, start, end)

    def evaluate(self):
        return atomics.SymbolObj.create(self.var_name)


class Character(ASTNode):
    def __init__(self, value, start, end):
        self.value = value
        super().__init__('Character', start, end)

    def __repr__(self, level=0):
        return ' ' * level + 'Character\n' + ' ' * (level + 1) + str(self.value)

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return Character(value, start, end)

    def evaluate(self):
        return language.Atomic.create(self.value, types.CharacterType())


class SimpleLeftAssignOp(ASTNode):
    def __init__(self, start, end):
        super().__init__('SimpleLeftAssign', start, end)

    def __repr__(self, level=0):
        return '<-'

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return SimpleLeftAssignOp(start, end)

    def evaluate(self):
        pass


class SuperLeftAssignOp(ASTNode):
    def __init__(self, start, end):
        super().__init__('SimpleLeftAssign', start, end)

    def __repr__(self, level=0):
        return '<<-'

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return SuperLeftAssignOp(start, end)

    def evaluate(self):
        pass


class Dlr(ASTNode):
    def __init__(self, value, start, end):
        self.value = value
        super().__init__('Dlr', start, end)

    def __repr__(self, level=0):
        return ' '*level+'$'

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return Dlr(value, start, end)

    def evaluate(self):
        pass

class Dots(ASTNode):
    def __init__(self, value, start, end):
        self.value = value
        super().__init__('Dots', start, end)

    def __repr__(self, level=0):
        return ' '*level+'...'

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return Dots(value, start, end)

    def evaluate(self):
        return atomics.SymbolObj.create('...')


class NULL(ASTNode):
    def __init__(self, value, start, end):
        self.value = value
        super().__init__('NULL', start, end)

    def __repr__(self, level=0):
        return ' '*level+'NULL'

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return NULL(value, start, end)

    def evaluate(self):
        return atomics.NULLObj()

class Na(ASTNode):
    def __init__(self, value, start, end):
        self.value = value
        super().__init__('Na', start, end)

    def __repr__(self, level=0):
        return ' ' * level + 'Na'

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return Na(value, start, end)

    def evaluate(self):
        return language.Atomic.create(None, types.LogicalType(), is_na=True)

class Nan(ASTNode):
    def __init__(self, value, start, end):
        self.value = value
        super().__init__('Nan', start, end)

    def __repr__(self, level=0):
        return ' ' * level + 'Nan'

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return Nan(value, start, end)

    def evaluate(self):
        return language.Atomic.create(None, types.DoubleType(), is_nan=True)

class Inf(ASTNode):
    def __init__(self, value, start, end):
        self.value = value
        super().__init__('Inf', start, end)

    def __repr__(self, level=0):
        return ' ' * level + 'Inf'

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return Inf(value, start, end)

    def evaluate(self):
        return language.Atomic.create(None, types.DoubleType(), is_inf=True)


class OrOp(ASTNode):
    def __init__(self, value, start, end):
        self.value = value
        super().__init__('OrOp', start, end)

    def __repr__(self, level=0):
        return ' ' * level + str(self.value)

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return OrOp(value, start, end)

    def evaluate(self):
        pass

class AndOp(ASTNode):
    def __init__(self, value, start, end):
        self.value = value
        super().__init__('AndOp', start, end)

    def __repr__(self, level=0):
        return ' ' * level + str(self.value)

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return AndOp(value, start, end)

    def evaluate(self):
        pass


class NotOp(ASTNode):
    def __init__(self, value, start, end):
        self.value = value
        super().__init__('NotOp', start, end)

    def __repr__(self, level=0):
        return ' ' * level + '!'

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return NotOp(value, start, end)

    def evaluate(self):
        pass

class PlusMinOp(ASTNode):
    def __init__(self, value, start, end):
        self.value = value
        super().__init__('PlusMin', start, end)

    def __repr__(self, level=0):
        return ' ' * level + str(self.value)

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return PlusMinOp(value, start, end)

    def evaluate(self):
        pass

class MultDivOp(ASTNode):
    def __init__(self, value, start, end):
        self.value = value
        super().__init__('MulDivOp', start, end)

    def __repr__(self, level=0):
        return ' ' * level + str(self.value)

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return MultDivOp(value, start, end)

    def evaluate(self):
        pass

class UserOp(ASTNode):
    def __init__(self, value, start, end):
        self.value = value
        super().__init__('UserOp', start, end)

    def __repr__(self, level=0):
        return ' ' * level + str(self.value)

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return UserOp(value, start, end)

    def evaluate(self):
        pass

class SeqOp(ASTNode):
    def __init__(self, value, start, end):
        self.value = value
        super().__init__('SeqOp', start, end)

    def __repr__(self, level=0):
        return ' ' * level + ':'

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return SeqOp(value, start, end)

    def evaluate(self):
        pass

class FactOp(ASTNode):
    def __init__(self, value, start, end):
        self.value = value
        super().__init__('FactOP', start, end)

    def __repr__(self, level=0):
        return ' ' * level + '^'

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return FactOp(value, start, end)

    def evaluate(self):
        pass

class CompOp(ASTNode):
    def __init__(self, value, start, end):
        self.value = value
        super().__init__('CompOp', start, end)

    def __repr__(self, level=0):
        return ' ' * level + str(self.value)

    __str__ = __repr__

    @classmethod
    def create(cls, value, children, start, end):
        if not Verbose:
            print('creating ast node with ' + str(cls.__name__) + 'with children: ' +str(children))
        return CompOp(value, start, end)

    def evaluate(self):
        pass

