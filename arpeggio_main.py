# from arpeggio.cleanpeg import ParserPEG
# from arpeggio import visit_parse_tree, PTNodeVisitor
#
# grammar = open('arpeggio_grammar2.peg').read()
# inp = open('test.r').read()
#
# parser = ParserPEG(grammar, 'start', debug=True, ws='\t ')
#
# parse_tree = parser.parse(inp)
#
# k = 0

from __future__ import absolute_import, unicode_literals, print_function
from arpeggio import visit_parse_tree, PTNodeVisitor

import os
from arpeggio.cleanpeg import ParserPEG
from arpeggio import visit_parse_tree
from node_rules import *


debug = True
ws = '\t '
grammar = open(os.path.join(os.path.dirname(__file__),
                                     'clean_grammar_test.peg'), 'r').read()
parser = ParserPEG(grammar, "start", debug=False, ws=ws, comment_rule_name='Comment')
input_expr = open('./test.r', 'r').read()
parse_tree = parser.parse(input_expr)
print(str(parse_tree))

# level = 20
# value = 5
# l = ' ' * level + 'Numeric\n' + ' ' * (level + 1) + str(value)
# print(l)
# exit()

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

# class Visitor(PTNodeVisitor):
#     def visit_Numeric(self, node, children):
#         print('here we visit Numeric - ' + str(node))
#         return float(node.value)
#
#     def visit__default__(self, node, children):
#         print('in_default')
#         print(str(node))
#         return children

# result = visit_parse_tree(parse_tree, Visitor(True))
#
# print('results')
# print(result)

class Visitor(PTNodeVisitor):
    def visit__default__(self, node, children):
        # print('in_default')
        # print(str(node))
        return extract_arr(children)

    # def generic_visit(self, node, visited_children):
    #     # print('visiting generically: \n\t\texpr_name \"' + str(node.expr_name) + '\"\n\t\ttext - \"' + str(node.full_text)+"\"")
    #     if isinstance(node.expr, OneOf):
    #         ret = extract_arr(visited_children)
    #         return ret
    #     if isinstance(node.expr, OneOrMore):
    #         ret = extract_arr(visited_children)
    #         return ret
    #     if isinstance(node.expr, ZeroOrMore):
    #         ret = extract_arr(visited_children)
    #         return ret
    #     if isinstance(node.expr, Optional):
    #         ret = extract_arr(visited_children)
    #         return ret[0] if ret else None
    #     if isinstance(node.expr, Sequence):
    #         ret = extract_arr(visited_children)
    #         return ret
    #     return

    def visit_start(self, node, children):
        ret = Start.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_simple_input(self, node, children):
        ret =  simple_input.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_list_of_inputs(self, node, children):
        ret =  list_of_inputs.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_simple_stmt(self, node, children):
        ret =  simple_stmt.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_flow_stmt(self, node, children):
        ret =  flow_stmt.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_break_stmt(self, node, children):
        ret =  break_stmt.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_next_stmt(self, node, children):
        ret =  next_stmt.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_compound_stmt(self, node, children):
        ret =  compound_stmt.create(None, extract_arr(children),node.position, node.position_end)
        return ret

    def visit_repeat_stmt(self, node, children):
        ret =  repeat_stmt.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_for_stmt(self, node, children):
        ret =  for_stmt.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_while_stmt(self, node, children):
        ret =  while_stmt.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_if_case(self, node, children):
        ret =  if_stmt.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_expr(self, node, children):
        ret =  or_expr.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_or_expr(self, node, children):
        ret =  or_expr.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_and_expr(self, node, children):
        ret =  and_expr.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_not_expr(self, node, children):
        ret =  not_expr.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_compare_expr(self, node, children):
        ret =  compare_expr.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_arith_expr(self, node, children):
        ret = arith_expr.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_term(self, node, children):
        ret =  term.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_special_term(self, node, children):
        ret =  special_term.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_sequence_term(self, node, children):
        ret =  sequence_term.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_factor(self, node, children):
        ret =  factor.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_power(self, node, children):
        ret =  power.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_element(self, node, children):
        ret = element.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    # def visit_assign_expr(self, node, children):
    #     ret =  assign_expr.create(None, extract_arr(children), node.position, node.position_end)
    #     return ret

    def visit_simple_assign(self, node, children):
        ret =  simple_assign.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_left_assign(self, node, children):
        ret =  left_assign.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_right_assign(self, node, children):
        ret =  right_assign.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_assign_item(self, node, children):
        ret = assign_item.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_atom(self, node, children):
        ret =  atom.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_trailer(self, node, children):
        ret =  trailer.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_call(self, node, children):
        ret = call.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_indexing(self, node, children):
        ret = indexing.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_list_index(self, node, children):
        ret =  list_indexing.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_subname(self, node, children):
        ret =  subname.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_argument(self, node, children):
        ret =  argument.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_expr_item(self, node, children):
        ret =  expr_item.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_code_block(self, node, children):
        ret =  code_block.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_funcdef(self, node, children):
        ret =  funcdef.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_call_params(self, node, children):
        ret =  call_params.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_func_params(self, node, children):
        ret =  func_params.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_optional(self, node, children):
        return children

    def visit_optional_param(self, node, children):
        ret =  optional_param.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_suite(self, node, children):
        ret =  suite.create(None, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_Logical(self, node, children):
        ret =  Logical.create(node.value, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_Numeric(self, node, children):
        ret =  Numeric.create(node.value, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_Integer(self, node, children):
        ret =  Integer.create(node.value, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_Complex(self, node, children):
        ret =  Complex.create(node.value, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_Variable(self, node, children):
        ret =  Variable.create(node.value, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_Character(self, node, children):
        ret =  Character.create(node.value, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_Dlr(self, node, children):
        ret =  Dlr.create(node.value, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_Dots(self, node, children):
        ret =  Dots.create(node.value, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_Null(self, node, children):
        ret =  NULL.create(node.value, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_Na(self, node, children):
        ret =  Na.create(node.value, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_Nan(self, node, children):
        ret =  Nan.create(node.value, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_Inf(self, node, children):
        ret =  Inf.create(node.value, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_OrOp(self, node, children):
        ret =  OrOp.create(node.value, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_AndOp(self, node, children):
        ret =  AndOp.create(node.value, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_NotOp(self, node, children):
        ret =  NotOp.create(node.value, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_PlusMinOp(self, node, children):
        ret =  PlusMinOp.create(node.value, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_MultDivOp(self, node, children):
        ret =  MultDivOp.create(node.value, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_UserOp(self, node, children):
        ret =  UserOp.create(node.value, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_SeqOp(self, node, children):
        ret = SeqOp.create(node.value, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_FactOp(self, node, children):
        ret =  FactOp.create(node.value, extract_arr(children), node.position, node.position_end)
        return ret

    def visit_CompOp(self, node, children):
        ret =  CompOp.create(node.value, extract_arr(children), node.position, node.position_end)
        return ret


result = visit_parse_tree(parse_tree, Visitor())

print('results')
print(str(result))
