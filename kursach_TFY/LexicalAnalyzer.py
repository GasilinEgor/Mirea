import re
from TokensAndStates import Tokens, States

NUMBER = r"[0-9]"
NUMBER2 = r"[0-9a-fA-FoO]"
BINNUMBER = r"[0-1]+(b|B)?$"
OCTNUMBER = r"[0-7]+(о|О)?$"
DECNUMBER = r"[0-9]+(d|D)?$"
HEXNUMBER = r"[0-9a-fA-F]+(h|H)?$"
FLOATNUMBER = r"[0-9]+.(E|e)?(\+|-)?[0-9]+$"
LETTER = r"[a-zA-Z]"
KWORDS = ['or', 'and', 'not', 'program', 'var', 'begin', 'end', 'if', 'then', 'else', 'for', 'to', 'do', 'while',
          'read', 'write']
NUM_ID = ['b', 'B', 'o', 'O', 'd', 'D', 'h', 'H', '.', 'e', 'E', '+', '-']
SEPARATORS = ';[]:,()'


class Token:
    def __init__(self, token, value):
        self.token = token
        self.value = value


def is_bin_number(number):
    if re.match(BINNUMBER, number) is not None:
        return True
    else:
        return False


def is_oct_number(number):
    if re.match(OCTNUMBER, number) is not None:
        return True
    else:
        return False


def is_dec_nuber(number):
    if re.match(DECNUMBER, number) is not None:
        return True
    else:
        return False


def is_hex_number(number):
    if re.match(HEXNUMBER, number) is not None:
        return True
    else:
        return False


def is_int_number(number):
    return is_bin_number(number) or is_oct_number(number) or is_dec_nuber(number) or is_hex_number(number)


def is_float_number(number):
    if re.match(FLOATNUMBER, number):
        return True
    else:
        return False


def is_type(value):
    return value == 'int' or value == 'float' or value == 'bool'


def is_bool_value(value):
    return value == 'true' or value == 'false'


def is_kword(value):
    if KWORDS.count(value) > 0:
        return True
    else:
        return False


def is_boll_operation(value):
    return value == 'or' or value == 'and'


def is_unary_operation(value):
    return value == 'not'


class Lexer:
    def __init__(self, program_name):
        self.file = open(program_name, "r")
        self.position = 0
        self.line = "start"
        self.tokens = []

    def getline(self):
        self.line = self.file.readline()
        self.position = 0

    def getchar(self):
        if self.position >= len(self.line):
            return '\n'
        else:
            self.position += 1
            return str(self.line[self.position - 1])

    def get_next_char(self):
        if self.position >= len(self.line):
            return '\n'
        else:
            return str(self.line[self.position])

    def print_tokens(self):
        for token in self.tokens:
            print(f"({token.token}, '{token.value}')")

    def print_tokens_in_text(self):
        name = f"Tokens_{self.file.name.split('.')[0]}.txt"
        with open(f"Tokens_{self.file.name.split('.')[0]}.txt", 'w+') as file:
            for token in self.tokens:
                file.write(f'{token.value}->{token.token.name}\n')
        file.close()
        return name

    def lexer(self):
        while self.line != "":
            self.getline()
            st = States.H
            c = self.getchar()
            while c != '\n':
                if st == States.H:
                    if c == '\n':
                        self.tokens.append(Token(Tokens.DV, c))
                    while c == ' ' or c == '\n' or c == '\t':
                        c = self.getchar()
                        if c == '\n':
                            self.tokens.append(Token(Tokens.DV, c))
                    if re.match(LETTER, c) is not None or c == '_':
                        st = States.ID
                    elif re.match(NUMBER, c) is not None:
                        st = States.NM
                    else:
                        st = States.DLM
                elif st == States.DLM:
                    next_c = self.get_next_char()
                    if c == '<' and next_c == '>' or (c == '<' or c == '>') and next_c == '=':
                        self.tokens.append(Token(Tokens.SP, c + next_c))
                        c = self.getchar()
                    elif c == '<' or c == '>' or c == '=':
                        self.tokens.append(Token(Tokens.SP, c))
                    elif c == '+' or c == '-' or c == '*' or c == '/':
                        self.tokens.append(Token(Tokens.OP, c))
                    elif SEPARATORS.find(c) != -1:
                        self.tokens.append(Token(Tokens.DV, c))
                    else:
                        self.tokens.append(Token(c, Tokens.ER))
                    c = self.getchar()
                    st = States.H
                elif st == States.NM:
                    num = c
                    c = self.getchar()
                    while (re.match(NUMBER, c) is not None or re.match(LETTER, c) is not None
                           or c == '+' or c == '-' or c == '.'):
                        num += c
                        c = self.getchar()
                    if is_int_number(num):
                        self.tokens.append(Token(Tokens.NM, num))
                    elif is_float_number(num):
                        self.tokens.append(Token(Tokens.NM, num))
                    else:
                        self.tokens.append(Token(Tokens.ER, num))
                    st = States.H
                elif st == States.ID:
                    name = c
                    c = self.getchar()
                    while re.match(LETTER, c) is not None or re.match(NUMBER, c) is not None or c == '_':
                        name += c
                        c = self.getchar()
                    if name == 'as':
                        self.tokens.append(Token(Tokens.EQ, name))
                    elif is_type(name):
                        self.tokens.append(Token(Tokens.TP, name))
                    elif is_bool_value(name) or is_unary_operation(name):
                        self.tokens.append(Token(Tokens.NM, name))
                    elif is_boll_operation(name):
                        self.tokens.append(Token(Tokens.OP, name))
                    elif is_kword(name):
                        self.tokens.append(Token(Tokens.KW, name))
                    else:
                        self.tokens.append(Token(Tokens.ID, name))
                    st = States.H
            self.tokens.append(Token(Tokens.DV, 'next'))
        self.file.close()
