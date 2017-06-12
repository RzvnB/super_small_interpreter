

class Token(object):

    def __init__(self, name, value, line):
        self.name = name
        self.value = value
        self.line = line


    def __str__(self):
        return '--{} {} {}--'.format(self.name, self.value, self.line)

    def __key(self):
        return self.name

    def __eq__(self, other):
        return self.__key() == other


class TokenError(Exception):

    def __init__(self, token, message):
        self.token = token
        self.message = message

    def __str__(self):
        return 'Error: {}, \n Current Token: {}'.format(self.message, self.token)


def parse(filename):
    tokens = []
    with open(filename, 'r') as _file:
        state = 0
        buff = ''
        line = 1
        char = _file.read(1)
        while True:
            if char == '':
                break
            if state == 0:
                if char == ' ' or char == '\t':
                    char = _file.read(1)
                elif char == '\n':
                    line += 1
                    char = _file.read(1)
                elif char >= '0' and char <= '9':
                    buff += char
                    state = 1
                    char = _file.read(1)
                elif (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z'):
                    buff += char
                    state = 2
                    char = _file.read(1)
                elif char == '.':
                    tokens.append(Token('DOT', char, line))
                    char = _file.read(1)
                elif char == ';':
                    tokens.append(Token('SEMICOLON', char, line))
                    char = _file.read(1)
                elif char == '+':
                    tokens.append(Token('ADD', char, line))
                    char = _file.read(1)
                elif char == '-':
                    tokens.append(Token('SUB', char, line))
                    char = _file.read(1)
                elif char == '/':
                    tokens.append(Token('DIV', char, line))
                    char = _file.read(1)
                elif char == '*':
                    tokens.append(Token('MUL', char, line))
                    char = _file.read(1)
                elif char == '=':
                    tokens.append(Token('ASSIGN', char, line))
                    char = _file.read(1)
                else:
                    raise Exception()
            elif state == 1:
                if char >= '0' and char <= '9':
                    buff += char
                    char = _file.read(1)
                else:
                    tokens.append(Token('NUMBER', buff, line))
                    buff = ''
                    state = 0
            elif state == 2:
                if char >= 'a' and char <= 'z' or char >= 'A' and char <= 'Z':
                    buff += char
                    char = _file.read(1)
                else:
                    if buff == 'read':
                        tokens.append(Token('READ', buff, line))
                    elif buff == 'echo':
                        tokens.append(Token('ECHO', buff, line))
                    else:
                        tokens.append(Token('VAR', buff, line))
                    buff = ''
                    state = 0
    return tokens
