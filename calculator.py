from string import ascii_letters
from collections import deque


class Calculator:

    commands = {'/exit': 'Bye!', '/help': 'The program calculates stuff'}
    variables = {}
    operators = {'+': lambda x, y: y + x, '-': lambda x, y: y - x, '*': lambda x, y: y * x,  '/': lambda x, y: y / x, '^': lambda x, y: y ** x}
    opr_priority = {'+': 0, '-': 0, '*': 2, '/': 2, '^': 3, '(': -1, ')': -1}
    stack = deque()

    @staticmethod
    def check_identifier(inp):
        return True if all(char in ascii_letters for char in inp.strip()) else False

    def is_value(self, inp):
        return True if inp in self.variables or inp.lstrip('-+').isdigit() else False

    def get_postfix(self, inp):
        self.stack.clear()
        postfix = deque()
        infix = ''.join(x if x.isdigit() else ' ' + x + ' ' for x in inp)
        for x in infix.split():
            if x.isdigit():
                postfix.append(x)
            elif x == '(':
                self.stack.appendleft(x)
            elif x == ')':
                for _ in range(self.stack.index('(')):
                    postfix.append(self.stack.popleft())
                self.stack.popleft()
            elif x in self.opr_priority:
                if not self.stack:
                    self.stack.append(x)
                else:
                    for _ in range(len(self.stack)):
                        if self.opr_priority[self.stack[0]] >= self.opr_priority[x]:
                            postfix.append(self.stack.popleft())
                    self.stack.appendleft(x)
        postfix += self.stack
        return postfix
    
    def get_value(self, inp_pf):
        self.stack.clear()
        for x in inp_pf:
            if x.isdigit():
                self.stack.append(int(x))
            elif x in self.operators:
                self.stack.append(self.operators[x](self.stack.pop(), self.stack.pop()))
        return int(self.stack.pop())

    def normalize_input(self, inp):
        self.stack.clear()
        for x in inp:
            if self.stack and x.isdigit() and (self.is_value(self.stack[-1]) or len(self.stack) == 1
               or (len(self.stack) > 1 and self.stack[-1] in self.opr_priority and self.stack[-2] in self.opr_priority and self.opr_priority[self.stack[-1]] == 0)):
                self.stack.append(self.stack.pop() + x)
            else:
                if self.stack and (x == '-' or x == '+') and (self.stack[-1] == '-' or self.stack[-1] == '+'):
                    x = '+' if x == '-' and self.stack[-1] == '-' else x
                    self.stack.pop()
                self.stack.append(x)
        return self.stack.copy()

    def check_nor_inp(self, inp):
        self.stack.clear()
        previous = ''
        for x in inp:
            if x == '(':
                self.stack.append(x)
            elif x == ')' and self.stack:
                self.stack.pop()
            elif x == ')' and not self.stack or previous and previous in self.operators and x in self.operators:
                return False
            previous = x
        return False if self.stack or not self.is_value(inp[0]) else True

    def declare_variable(self, inp):
        inp = inp.replace(' ', '')
        identifier, *value = inp.split('=')
        if not self.check_identifier(identifier):
            print('Invalid identifier')
        elif self.is_value(' '.join(value)) or self.check_identifier(' '.join(value)):
            if self.is_value(' '.join(value)):
                self.variables[identifier] = ' '.join(value)
            else:
                print('Unknown variable')
        else:
            print('Invalid assignment')

    def check_input(self, inp):
        inp_var = ''.join(self.variables[x] if x in self.variables else x for x in inp)
        if inp.startswith('/'):
            print(self.commands[inp] if inp in self.commands else 'Unknown command')
            if inp == '/exit':
                return inp
        elif '=' in inp:
            self.declare_variable(inp)
        elif len(inp.split()) == 1 and all(x not in self.opr_priority for x in inp):
            if self.check_identifier(inp):
                print(self.variables[inp] if inp in self.variables else 'Unknown variable')
            else:
                print("Invalid identifier")
        elif self.check_nor_inp(self.normalize_input(inp_var)):
            return self.normalize_input(inp_var)
        else:
            print('Invalid expression')

    def main(self):
        while True:
            user_inp = input()
            user_inp = self.check_input(user_inp) if user_inp else None
            if user_inp and ''.join(user_inp) == '/exit':
                break
            elif user_inp and self.is_value(''.join(user_inp)):
                print(''.join(user_inp).lstrip('+'))
            elif user_inp:
                print(self.get_value(self.get_postfix(user_inp)))


Calculator().main()
