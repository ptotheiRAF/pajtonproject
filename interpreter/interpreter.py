from .lexer import INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF, POW, LOG, SQRT, SIN, TAN, COS, CTG, MORE, MOREEQL, LESS, LESSEQL, EQUALS
import math

###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_UnOp(self, node):
        if node.op.type == LOG:
            return math.log2(self.visit(node.num))
        elif node.op.type == POW:
            return math.pow(self.visit(node.num), 2)
        elif node.op.type == SQRT:
            return math.sqrt(self.visit(node.num))
        elif node.op.type == SIN:
            return math.sin(self.visit(node.num))
        elif node.op.type == COS:
            return math.cos(self.visit(node.num))
        elif node.op.type == TAN:
            return math.tan(self.visit(node.num))
        elif node.op.type == CTG:
            return 1 / math.tan(self.visit(node.num))

    def visit_CompOp(self, node):
        if node.op.type == MORE:
            if self.visit(node.lnum) > self.visit(node.rnum):
                return True
            else:
                return False
        elif node.op.type == MOREEQL:
            if self.visit(node.lnum) >= self.visit(node.rnum):
                return True
            else:
                return False
        elif node.op.type == LESS:
            if self.visit(node.lnum) < self.visit(node.rnum):
                return True
            else:
                return False
        elif node.op.type == LESSEQL:
            if self.visit(node.lnum) <= self.visit(node.rnum):
                return True
            else:
                return False
        elif node.op.type == EQUALS:
            if self.visit(node.lnum) == self.visit(node.rnum):
                return True
            else:
                return False

    def visit_Num(self, node):
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

