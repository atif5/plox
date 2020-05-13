from enum import Enum

FunctionType = (
    'FunctionType',
    '''
        NONE
        FUNCTION
    '''
)

TokenType = Enum(
    'TokenType', 
    '''
        IDENTIFIER STRING NUMBER

        BANG BANG_EQUAL EQUAL EQUAL_EQUAL
        GREATER GREATER_EQUAL LESS LESS_EQUAL

        COMMA DOT MINUS PLUS SEMICOLON SLASH STAR
        LEFT_PAREN RIGHT_PAREN LEFT_BRACE RIGHT_BRACE

        EOF IF CLASS ELSE TRUE BREAK FUN FOR AND OR VAR
        CONTINUE SUPER PRINT FALSE RETURN NIL WHILE THIS
    '''
)