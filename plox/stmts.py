# coding: utf-8

__all__ = (
    'Statement', 'VarStatement', 'IfStatement', 'WhileStatement',
    'BlockStatement', 'PrintStatement', 'ExpressionStatement'
)

class Statement:
    pass

class PrintStatement(Statement):
    def __init__(self, expr):
        self.expression = expr

    def accept(self, visitor):
        visitor.visit_print_statement(self)

class ExpressionStatement(Statement):
    def __init__(self, expr):
        self.expression = expr

    def accept(self, visitor):
        visitor.visit_expression_statement(self)

class VarStatement(Statement):
    def __init__(self, name, expr):
        self.name = name
        self.initializer = expr

    def accept(self, visitor):
        visitor.visit_var_statement(self)

class BlockStatement(Statement):
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        visitor.visit_block_statement(self)

class IfStatement(Statement):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        visitor.visit_if_statement(self)

class WhileStatement(Statement):
    def __init__(self, condition, statement):
        self.condition = condition
        self.statement = statement

    def accept(self, visitor):
        visitor.visit_while_statement(self)