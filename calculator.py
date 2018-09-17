#!/bin/python3
# calculator.py

from enum import Enum, auto
import pprint as pp
import operations

class Token(Enum):
    START = auto()
    END = auto()
    FUNC = auto()
    NUM = auto()


numbers = [str(n) for n in range(10)]
reserved_chars = ['(', ')', ' ']


def lex(string):
    string = list(string)
    tokens = []

    def pop_next():
        return string.pop(0)

    def peek_next():
        return string[0]

    def get_num():
        num = []
        while peek_next() in numbers:
            num.append(int(pop_next()))
        return sum([(10 ** i) * n for (i, n) in enumerate(reversed(num))])

    def get_name():
        name = ''
        while peek_next() not in reserved_chars:
            name = name + pop_next()
        return name

    while string:
        ch = peek_next()
        if ch == ' ':
            pop_next()
            continue
        elif ch == '(':
            t = (Token.START, pop_next())
        elif ch == ')':
            t = (Token.END, pop_next())
        elif ch in numbers:
            t = (Token.NUM, get_num())
        else:
            t = (Token.FUNC, get_name())
        tokens.append(t)
    return tokens


def get_arg_tup(tokens):
    def pop_next():
        return tokens.pop(0)

    def peek_next():
        return tokens[0]

    def get_next_expr():
        i = 1
        expr_tokens = [pop_next()]
        while i > 0:
            if peek_next()[0] is Token.START:
                i += 1
            elif peek_next()[0] is Token.END:
                i -= 1
            expr_tokens.append(pop_next())
        return expr_tokens

    tup = []
    while tokens:
        if peek_next()[0] is Token.NUM:
            tup.append(pop_next()[1])
        else:
            tup.append(parse(get_next_expr()))

    return tuple(tup)


def parse(tokens):
    return (tokens[1][1], ) + get_arg_tup(tokens[2:-1])


def comple(tree):
    if type(tree) is int:
        return tree
    else:
        return apply(tree[0], *map(lambda branch: comple(branch), tree[1:]))


def apply(funcsym, *args):
    func_name, writer = operations.sym_dict[funcsym]
    func = getattr(operations, func_name)
    print('Thanks for the "%s" function, %s!' % (funcsym, writer))
    return func(*args)


def compute(string):
    return comple(parse(lex(string)))


if __name__ == "__main__":
    test_str = '(+ (- 10 10) 10)'
    print('%s = %f' % (test_str, compute(test_str)))


