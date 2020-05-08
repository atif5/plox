# coding: utf-8

from numbers import Number
from plox.token import TokenType

class RuntimeError(Exception):
    def __init__(self, token, message):
        super().__init__(message)
        self.token = token

def is_truthy(object):
    return bool(object)

def stringify(object):
    if object is None:
        return 'nil'

    if type(object) is bool:
        return str(object).lower()

    return str(object)

def check_number_operands(operator, *operands):
    if all(map(lambda o: isinstance(o, Number), operands)):
        return

    raise RuntimeError(operator, 'operands must be numbers')

class Environment:
    def __init__(self, enclosing=None):
        self.__values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        self.__values[name.lexeme] = value

    def get(self, name):
        try:
            return self.__values[name.lexeme]
        except KeyError:

            if self.enclosing:
                return self.enclosing.get(name)

            raise RuntimeError(name, f'undefined variable "{name.lexeme}"')

    def assign(self, name, value):
        if name.lexeme in self.__values:
            self.__values[name.lexeme] = value; return

        if self.enclosing:
            self.enclosing.assign(name, value); return

        raise RuntimeError(name, f'undefined variable "{name.lexeme}"')

class Interpreter:
    def __init__(self, plox):
        self.plox = plox
        self.environment = Environment()

    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as error:
            self.plox.runtime_error(error)

    def evaluate(self, expr):
        return expr.accept(self)

    def execute(self, stmt):
        if stmt:
            stmt.accept(self)

    def execute_block(self, statements, environment):
        previous = self.environment

        try:
            self.environment = environment

            for statement in statements:
                self.execute(statement)

        finally:
            self.environment = previous
        
    def visit_literal(self, expr):
        return expr.value

    def visit_grouping(self, expr):
        return self.evaluate(expr.expression)

    def visit_unary(self, expr):
        right = self.evaluate(expr.expression)

        if expr.operator.type == TokenType.MINUS:
            check_number_operands(expr.operator, right)
            return -1 * right

        elif expr.operator.type == TokenType.BANG:
            return not is_truthy(right)

        return None

    def visit_variable(self, expr):
        return self.environment.get(expr.name)

    def visit_assignment(self, expr):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)

        return value

    def visit_logical(self, expr):
        left = self.evaluate(expr.left)

        if expr.operator.type == TokenType.OR:
            if is_truthy(left):
                return left
        else:
            if not is_truthy(left):
                return left

        return self.evaluate(expr.right)

    def visit_binary(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        t_type = expr.operator.type

        if t_type not in [TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL, TokenType.PLUS]:
            check_number_operands(expr.operator, left, right)

        if t_type is TokenType.EQUAL_EQUAL:
            return left == right

        elif t_type is TokenType.BANG_EQUAL:
            return not (left == right)

        elif t_type is TokenType.LESS:
            return left < right

        elif t_type is TokenType.GREATER:
            return left > right

        elif t_type is TokenType.LESS_EQUAL:
            return left <= right

        elif t_type is TokenType.GREATER_EQUAL:
            return left >= right

        elif t_type is TokenType.STAR:
            return left * right

        elif t_type is TokenType.SLASH:
            return left / right

        elif t_type is TokenType.MINUS:
            return left - right

        elif t_type is TokenType.PLUS:
            try:
                if isinstance(left, str) or isinstance(right, str):
                    return f'{left}{right}'

                return left + right
            except TypeError:
                raise RuntimeError(expr.operator, 'operands must be numbers or strings')

        return None

    def visit_expression_statement(self, stmt):
        self.evaluate(stmt.expression)

    def visit_print_statement(self, stmt):
        print(stringify(self.evaluate(stmt.expression)))

    def visit_var_statement(self, stmt):
        value = None

        if stmt.initializer:
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name, value)

    def visit_block_statement(self, stmt):
        self.execute_block(stmt.statements, Environment(self.environment))

    def visit_if_statement(self, stmt):
        if is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)

        elif stmt.else_branch:
            self.execute(stmt.else_branch)

    def visit_while_statement(self, stmt):
        while is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.statement)