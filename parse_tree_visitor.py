from parsimonious.expressions import Not, ZeroOrMore, OneOrMore, OneOf, Optional, Sequence
class Walker:
    node_rules = dict()

    def __init__(self, rules, Verbose=True):
        self.node_visitors = rules
        self.Verbose = Verbose

    def walk(self, tree):
        if not self.Verbose:
            print('started')
        r = self.perform_walk(tree)
        if not self.Verbose:
            print('Done')
        return r

    def perform_walk(self, node, level=0):
        node_rule = self.node_visitors[node.expr_name] if node.expr_name in self.node_visitors else None
        if not node_rule:
            if not self.Verbose:
                s = ''+str('\t')*level
                print(s+'Not found node_rule for node {}'.format(str(node).split('\n')[0]))
                print(str(type(node.expr)))
            result_children = []
            for child in node.children:
                if not self.Verbose:
                    s = '' + str('\t') * level
                    print(s + 'Walking into into child{}'.format(str(child).split('\n')[0]))

                r = self.perform_walk(child, level+1)

                if not self.Verbose:
                    s = ''+str('\t')*level
                    print(s+'Returned from child:. Results: {}'.format(str(child).split('\n')[0], str(r).split('\n')[0]))

                if not r:
                    continue
                res = [n for n in r if n is not None]
                result_children.append(res)
            return result_children


        if not self.Verbose:
            s = '' + str('\t') * level
            print(s + 'Found node_rule {} for node {}'.format(str(node_rule).split('\n')[0], str(node).split('\n')[0]))

        result_children = []
        for child in node.children:

            if not self.Verbose:
                s = ''+str('\t')*level
                print(s+'Walking into child {}'.format(str(child).split('\n')[0]))

            r = self.perform_walk(child, level+1)

            if not self.Verbose:
                s = ''+str('\t')*level
                print(s+'Returned from child {}. Results: {}'.format(str(child).split('\n')[0], str(r).split('\n')[0]))

            if not r:
                continue
            res = [n for n in r if n is not None]
            result_children.append(res)

        if not self.Verbose:
            s = '' + str('\t') * level
            print(s + 'Evaluating node {} with children: {}'.format(str(node).split('\n')[0], str(result_children).split('\n')[0]))
        res = self.eval_node(node, result_children)

        if not self.Verbose:
            s = '' + str('\t') * level
            print(s + 'Evaluated node value: {}'.format(str(res).split('\n')[0]))

        if res:
            return res if isinstance(res, list) else list([res])
        return None

    def eval_node(self, node, children):
        node_rule = self.node_visitors[node.expr_name]

        val = node_rule.create(node.text, children, node.start, node.end)
        if val:
            return val
            # if isinstance(val, ASTNode):
            #     return val
            # raise Exception("visiting function should return ASTNode instance or None")
        return None


def visit(expr_name, text, children, start, end):
    pass


class ASTNode:
    @classmethod
    def create(cls, value, children, start, end):
        pass

    def evaluate(self):
        pass

    def __repr__(self, level=0):
        return super().__repr__()

    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end


