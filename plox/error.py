# coding: utf-8

class ParseError(Exception):
    pass

class RuntimeError(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message

class Return(RuntimeError):
    def __init__(self, value):
        self.value = value