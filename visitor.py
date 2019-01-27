from node_rules import *
from parsimonious import NodeVisitor
from parsimonious.expressions import OneOf, OneOrMore, Sequence, ZeroOrMore, Optional

def extract_arr(tree):
    if not isinstance(tree, list):
        if tree:
            return [tree]
        else:
            return []
    ret = []
    for el in tree:
        r = extract_arr(el)
        if r:
            ret.extend(r)
    return ret

class Visitor(NodeVisitor):
    def generic_visit(self, node, visited_children):
        # print('visiting generically: \n\t\texpr_name \"' + str(node.expr_name) + '\"\n\t\ttext - \"' + str(node.full_text)+"\"")
        if isinstance(node.expr, OneOf):
            ret = extract_arr(visited_children)
            return ret
        if isinstance(node.expr, OneOrMore):
            ret = extract_arr(visited_children)
            return ret
        if isinstance(node.expr, ZeroOrMore):
            ret = extract_arr(visited_children)
            return ret
        if isinstance(node.expr, Optional):
            ret = extract_arr(visited_children)
            return ret
        if isinstance(node.expr, Sequence):
            ret = extract_arr(visited_children)
            return ret
        return

    def visit_start(self, node, children):
        ret =  Start.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_simple_input(self, node, children):
        return extract_arr(children)

    def visit_list_of_inputs(self, node, children):
        return extract_arr(children)

    def visit_simple_stmt(self, node, children):
        return extract_arr(children)

    def visit_flow_stmt(self, node, children):
        return extract_arr(children)

    def visit_break_stmt(self, node, children):
        ret =  break_stmt.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_next_stmt(self, node, children):
        ret =  next_stmt.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_compound_stmt(self, node, children):
        return extract_arr(children)

    def visit_repeat_stmt(self, node, children):
        ret =  repeat_stmt.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_for_stmt(self, node, children):
        ret =  for_stmt.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_while_stmt(self, node, children):
        ret =  while_stmt.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_if_case(self, node, children):
        ret =  if_stmt.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_expr(self, node, children):
        ret =  or_expr.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_or_expr(self, node, children):
        ret =  or_expr.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_and_expr(self, node, children):
        ret =  and_expr.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_not_expr(self, node, children):
        ret =  not_expr.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_compare_expr(self, node, children):
        ret =  compare_expr.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_arith_expr(self, node, children):
        ret = arith_expr.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_term(self, node, children):
        ret =  term.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_special_term(self, node, children):
        ret =  special_term.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_sequence_term(self, node, children):
        ret =  sequence_term.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_factor(self, node, children):
        ret =  factor.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_power(self, node, children):
        ret =  power.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_element(self, node, children):
        ret = element.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_assign_expr(self, node, children):
        return extract_arr(children)

    def visit_simple_assign(self, node, children):
        ret =  simple_assign.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_left_assign(self, node, children):
        ret =  left_assign.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_right_assign(self, node, children):
        ret =  right_assign.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_assign_item(self, node, children):
        return extract_arr(children)

    def visit_atom(self, node, children):
        return extract_arr(children)

    def visit_trailer(self, node, children):
        return extract_arr(children)

    def visit_call(self, node, children):
        ret = call.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_indexing(self, node, children):
        ret = indexing.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_list_indexing(self, node, children):
        ret =  list_indexing.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_subname(self, node, children):
        ret =  subname.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_argument(self, node, children):
        return extract_arr(children)

    def visit_expr_item(self, node, children):
        return extract_arr(children)

    def visit_code_block(self, node, children):
        ret =  code_block.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_funcdef(self, node, children):
        ret =  funcdef.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_func_params(self, node, children):
        return extract_arr(children)

    def visit_optional_param(self, node, children):
        ret =  optional_param.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_optionals(self, node, children):
        return extract_arr(children)

    def visit_suite(self, node, children):
        ret =  suite.create(None, extract_arr(children), node.start, node.end)
        return ret

    def visit_Logical(self, node, children):
        ret =  Logical.create(node.text, extract_arr(children), node.start, node.end)
        return ret

    def visit_Numeric(self, node, children):
        ret =  Numeric.create(node.text, extract_arr(children), node.start, node.end)
        return ret

    def visit_Integer(self, node, children):
        ret =  Integer.create(node.text, extract_arr(children), node.start, node.end)
        return ret

    def visit_Complex(self, node, children):
        ret =  Complex.create(node.text, extract_arr(children), node.start, node.end)
        return ret

    def visit_Variable(self, node, children):
        ret =  Variable.create(node.text, extract_arr(children), node.start, node.end)
        return ret

    def visit_Character(self, node, children):
        ret =  Character.create(node.text, extract_arr(children), node.start, node.end)
        return ret

    def visit_SimpleLeftAssignOp(self, node, children):
        return SimpleLeftAssignOp.create(node.text, [], node.start, node.end)

    def visit_SuperLeftAssignOp(self, node, children):
        return SuperLeftAssignOp.create(node.text, [], node.start, node.end)

    def visit_SimpleRightAssignOp(self, node, children):
        return SimpleLeftAssignOp.create(node.text, [], node.start, node.end)

    def visit_SuperRightAssignOp(self, node, children):
        return SuperLeftAssignOp.create(node.text, [], node.start, node.end)

    def visit_Dlr(self, node, children):
        ret =  Dlr.create(node.text, extract_arr(children), node.start, node.end)
        return ret

    def visit_Dots(self, node, children):
        ret =  Dots.create(node.text, extract_arr(children), node.start, node.end)
        return ret

    def visit_Null(self, node, children):
        ret =  NULL.create(node.text, extract_arr(children), node.start, node.end)
        return ret

    def visit_Na(self, node, children):
        ret =  Na.create(node.text, extract_arr(children), node.start, node.end)
        return ret

    def visit_Nan(self, node, children):
        ret =  Nan.create(node.text, extract_arr(children), node.start, node.end)
        return ret

    def visit_Inf(self, node, children):
        ret =  Inf.create(node.text, extract_arr(children), node.start, node.end)
        return ret

    def visit_OrOp(self, node, children):
        ret =  OrOp.create(node.text, extract_arr(children), node.start, node.end)
        return ret

    def visit_AndOp(self, node, children):
        ret =  AndOp.create(node.text, extract_arr(children), node.start, node.end)
        return ret

    def visit_NotOp(self, node, children):
        ret =  NotOp.create(node.text, extract_arr(children), node.start, node.end)
        return ret

    def visit_PlusMinOp(self, node, children):
        ret =  PlusMinOp.create(node.text, extract_arr(children), node.start, node.end)
        return ret

    def visit_MultDivOp(self, node, children):
        ret =  MultDivOp.create(node.text, extract_arr(children), node.start, node.end)
        return ret

    def visit_UserOp(self, node, children):
        ret =  UserOp.create(node.text, extract_arr(children), node.start, node.end)
        return ret

    def visit_SeqOp(self, node, children):
        ret = SeqOp.create(node.text, extract_arr(children), node.start, node.end)
        return ret

    def visit_FactOp(self, node, children):
        ret =  FactOp.create(node.text, extract_arr(children), node.start, node.end)
        return ret

    def visit_CompOp(self, node, children):
        ret =  CompOp.create(node.text, extract_arr(children), node.start, node.end)
        return ret
