from lexer import *
from copy import copy

tokens = parse('test')
for token in tokens:
    print(token)
crtIdx = 0
crtToken = tokens[crtIdx]
symbols = {}

def consume(name):
    global crtToken
    global crtIdx
    if crtToken == name:
        try:
            crtIdx += 1
            crtToken = tokens[crtIdx]
        except IndexError:
            return True
        return True
    return False

def factor():
    tk = copy(crtToken)
    if consume('NUMBER'):
        return int(tk.value)
    if consume('VAR'):
        try:
            return symbols[tk.value]
        except Exception:
            print(TokenError(crtToken, 'Uninitialized variable'))
    return False

def term():
    fact = factor()    
    if fact:
        fact = _term(fact)
        return fact
    return False

def _term(fact):
    while crtToken.name in ('MUL', 'DIV'):
        if consume('MUL'):
            right = factor()
            if not right:
                raise TokenError(crtToken, 'missing factor after mul')
            fact *= right
        else: 
            consume('DIV')
            right = factor()
            if not right:
                raise TokenError(crtToken, 'missing factor after div')
            fact /= right
    return fact

def expression():
    t = term()
    if t:
        t = _expression(t)
        return t
    return False

def _expression(t):
    while crtToken.name in ('ADD', 'SUB'):
        if consume('ADD'):
            right = term()
            if not right:
                raise TokenError(crtToken, 'missing term after add')
            t += right
        else: 
            consume('SUB')
            right = term()
            if not right:
                raise TokenError(crtToken, 'missing term after sub')
            t -= right
    return t

def assignment():
    var_token = copy(crtToken)
    if consume('VAR'):
        if not consume('ASSIGN'):
            raise TokenError(crtToken, 'missing assign after var')
        result = expression()
        if not result:
            raise TokenError(crtToken, 'missing expr after assign')
        symbols[var_token.value] = result
        return True
    return False

def echo():
    global symbols
    if consume('ECHO'):
        tk = copy(crtToken)
        if not consume('VAR'):
            raise TokenError(crtToken, 'missing var after echo')
        try:
            print(symbols[tk.value])
        except Exception:
            print(TokenError(crtToken, 'Uninitialized variable'))
        return True
    return False

def read():
    if consume('READ'):
        if not consume('VAR'):
            raise TokenError(crtToken, 'missing var after read')
        return True
    return False

def statement():
    if read() or echo() or assignment():
        return True
    return False

def statements():
    if statement():
        _statements()
        return True
    return False

def _statements():
    if consume('SEMICOLON'):
        if not statement():
            raise TokenError(crtToken, 'missing statement after semicolon')
        _statements()

def script():
    if statements():
        if not consume('DOT'):
            raise TokenError(crtToken, 'missing dot after statements')
    print(symbols)

script()