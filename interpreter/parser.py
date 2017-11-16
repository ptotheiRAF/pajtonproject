from .lexer import *


###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################

class AST(object):
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class UnOp(AST):
    def __init__(self, op, num):
        self.op = op
        self.num = num


class CompOp(AST):
    def __init__(self, lnum, op, rnum):
        self.lnum = lnum
        self.token = self.op = op
        self.rnum = rnum


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def op(self):
        node = self.factor()
        token = self.current_token

        if token.type == POW:
            self.eat(POW)
            node = UnOp(token, self.factor())
        elif token.type == LOG:
            self.eat(LOG)
            node = UnOp(token, self.factor())
        elif token.type == SQRT:
            self.eat(SQRT)
            node = UnOp(token, self.factor())
        elif token.type == SIN:
            self.eat(SIN)
            node = UnOp(token, self.factor())
        elif token.type == COS:
            self.eat(COS)
            node = UnOp(token, self.factor())
        elif token.type == TAN:
            self.eat(TAN)
            node = UnOp(token, self.factor())
        elif token.type == CTG:
            self.eat(CTG)
            node = UnOp(token, self.factor())
        return node

    def compareOp(self):
        node = self.expr()
        token = self.current_token
        if (token.type == MORE):
            self.eat(MORE)
            node = CompOp(node, token, self.expr())
        elif (token.type == MOREEQL):
            self.eat(MOREEQL)
            node = CompOp(node, token, self.expr())
        elif (token.type == LESS):
            self.eat(LESS)
            node = CompOp(node, token, self.expr())
        elif (token.type == LESSEQL):
            self.eat(LESSEQL)
            node = CompOp(node, token, self.expr())
        elif (token.type == EQUALS):
            self.eat(EQUALS)
            node = CompOp(node, token, self.expr())

        return node

    def factor(self):
        """factor : INTEGER | LPAREN expr RPAREN"""
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.compareOp()
            self.eat(RPAREN)
            return node

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.op()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        """
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN
        """
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def parse(self):
        node = self.compareOp()
        if self.current_token.type != EOF:
            self.error()
        return node