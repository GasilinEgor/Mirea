from TokensAndStates import Tokens
from LexicalAnalyzer import Token


class Parse:
    def __init__(self, file_name):
        self.file = open(file_name, 'r')
        self.token = Token(Tokens.KW, 'token')

    def get_token(self):
        token = self.file.readline().split('->')
        self.token = Token(token[1][:-1], token[0])

    def program(self):  # программа
        self.get_token()
        if self.token.value != 'program' or self.token.token != Tokens.KW.name:
            print(1, self.token.value)
        self.get_token()
        if self.token.value != 'var' or self.token.token != Tokens.KW.name:
            print(1, self.token.value)
        self.get_token()
        if self.token.token != Tokens.TP.name:
            print(2, self.token.value)
        self.description()
        if self.token.token != Tokens.KW.name or self.token.value != 'begin':
            print(1, self.token.value)
        self.get_token()
        if self.token.value == '[' and self.token.token == Tokens.DV.name:
            self.get_token()
            if self.token.value == 'next' and self.token.token == Tokens.DV.name:
                self.composite()
            else:
                print(9, self.token.value)
        else:
            self.operator()
        self.get_token()
        if self.token.value != 'end' or self.token.token != Tokens.KW.name:
            print(15, self.token.value)
        else:
            print("Ошибок нет")

    def composite(self):  # составной оператор
        while self.token.value != ']':
            if (self.token.value == 'next' or self.token.value == ':') and self.token.token == Tokens.DV.name:
                self.get_token()
                self.operator()
            else:
                print(11, self.token.value)
                break
        self.get_token()

    def description(self):  # описание
        self.get_token()
        if self.token.token != Tokens.ID.name:
            print(3, self.token.value)
        self.get_token()
        while self.token.token == Tokens.DV.name and self.token.value == ',':
            self.get_token()
            if self.token.token != Tokens.ID.name:
                print(5, self.token.value)
            self.get_token()

    def operator(self):  # оператор
        if self.token.token == Tokens.ID.name:
            self.assignment()
        elif self.token.token == Tokens.KW.name and self.token.value == 'if':
            self.condition()
        elif self.token.token == Tokens.KW.name and self.token.value == 'for':
            self.for_cycle()
        elif self.token.token == Tokens.KW.name and self.token.value == 'while':
            self.while_cycle()
        elif self.token.token == Tokens.KW.name and self.token.value == 'write':
            self.write()
        elif self.token.token == Tokens.KW.name and self.token.value == 'read':
            self.read()

    def read(self):  # ввод
        self.get_token()
        if self.token.value == '(' and self.token.token == Tokens.DV.name:
            self.get_token()
            if self.token.token != Tokens.ID.name:
                print(13, self.token.value)
            self.get_token()
            while self.token.value == ',' and self.token.token == Tokens.DV.name:
                self.get_token()
                if self.token.token != Tokens.ID.name:
                    print(13, self.token.value)
                self.get_token()
            if self.token.value != ')':
                print(14, self.token.value)
            self.get_token()
        else:
            print(15, self.token.value)

    def write(self):  # вывод
        self.get_token()
        if self.token.value == '(' and self.token.token == Tokens.DV.name:
            self.get_token()
            if self.token.token != Tokens.ID.name:
                print(13, self.token.value)
            self.get_token()
            while self.token.value == ',' and self.token.token == Tokens.DV.name:
                self.expression()
            if self.token.value != ')':
                print(14, self.token.value)
            self.get_token()
        else:
            print(15, self.token.value)

    def while_cycle(self):  # цикл while
        self.expression()
        if self.token.value == 'do' and self.token.token == Tokens.KW.name:
            self.get_token()
            if self.token.value == '[' and self.token.token == Tokens.DV.name:
                self.get_token()
                if self.token.value == 'next' and self.token.token == Tokens.DV.name:
                    self.composite()
                else:
                    print(9, self.token.value)
            else:
                self.operator()
        else:
            print(12, self.token.value)

    def for_cycle(self):  # цикл for
        self.get_token()
        if self.token.token == Tokens.ID.name:
            self.assignment()
        else:
            print(10, self.token.value)
        self.expression()
        if self.token.value == 'do' and self.token.token == Tokens.KW.name:
            self.get_token()
            if self.token.value == '[' and self.token.token == Tokens.DV.name:
                self.get_token()
                if self.token.value == 'next' and self.token.token == Tokens.DV.name:
                    self.composite()
                else:
                    print(9, self.token.value)
            else:
                self.operator()
        else:
            print(12, self.token.value)

    def assignment(self):  # присвоение
        self.get_token()
        if self.token.token == Tokens.EQ.name and self.token.value == 'as':
            self.expression()

    def condition(self):  # if
        self.expression()
        if self.token.value != 'then' or self.token.token != Tokens.KW.name:
            print(8, self.token.value)
        self.get_token()
        if self.token.value == '[' and self.token.token == Tokens.DV.name:
            self.get_token()
            if self.token.value == 'next' and self.token.token == Tokens.DV.name:
                self.composite()
            else:
                print(9, self.token.value)
        else:
            self.operator()

    def expression(self):  # выражение
        self.sum()
        while self.token.token == Tokens.SP.name:
            self.sum()

    def sum(self):  # сумма
        if self.product():
            self.get_token()
        if self.token.token == Tokens.OP.name and (
                self.token.value == '+' or self.token.value == '-' or self.token.value == 'or'):
            if self.product():
                self.get_token()
        else:
            return

    def product(self):  # произведение
        self.multiplier()
        self.get_token()
        if self.token.token == Tokens.OP.name and (
                self.token.value == '*' or self.token.value == '/' or self.token.value == 'and'):
            self.multiplier()
            return True
        else:
            return False

    def multiplier(self):  # множитель
        self.get_token()
        if self.token.value == '(':
            self.get_token()
            self.expression()
        elif self.token.value == 'not':
            self.get_token()
            self.multiplier()
        elif self.token.token == Tokens.ID.name or self.token.token == Tokens.NM.name:
            return
        else:
            print(7, self.token.value)
