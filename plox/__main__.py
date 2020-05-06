# coding: utf-8

import sys
import signal

from plox.token import TokenType

from plox.parser import Parser
from plox.scanner import Scanner
from plox.interpreter import Interpreter

signal.signal(signal.SIGINT, lambda *f: exit(0))

class PLox:
    def __init__(self):
        self.interpreter = Interpreter(self)
        self.error_occured = False
        self.runtime_error_occured = False

    def run(self, source):
        token_list  = Scanner(self, source).scan_tokens()
        parsed_expr = Parser(self, token_list).parse()

        if parsed_expr:
            self.interpreter.interpret(parsed_expr)

    def run_prompt(self):
        while True:
            self.run(input('plox > '))
            self.error_occured = False
            self.runtime_error_occured = False

    def run_file(self, file_name):
        with open(file_name, 'r') as f:
            self.run(f.read())

        if self.error_occured:
            sys.exit(65)

        if self.runtime_error_occured:
            sys.exit(70)

    def scan_error(self, line, message):
        self.report(line, '', message)

    def parse_error(self, token, message):
        where = 'at end' if token.type == TokenType.EOF else f"at '{token.lexeme}'"
        self.report(token.line, where, message)

    def runtime_error(self, error):
        self.report(error.token.line, '', error.message)
        self.runtime_error_occured = True

    def report(self, line, where, message):
        print(f'l{line} error: {where} {message}', file=sys.stderr)
        self.error_occured = True

if __name__ == '__main__':
    if len(sys.argv) == 1:
        PLox().run_prompt()
    else:
        PLox().run_file(sys.argv[1])