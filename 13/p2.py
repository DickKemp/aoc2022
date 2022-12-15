from dataclasses import dataclass
import re
import numpy as np
from collections import deque



class Node:
    def __init__(self, v, special=False):
        if type(v) is list:
            self.children = [Node(c) for c in v]
            self.value = None
        else:
            self.children = None
            self.value = int(v)
        self.special = special

    def is_leaf(self):
        return self.children is None

    def get_value(self):
        return self.value
    
    def get_child(self, n):
        return self.children[n]

    def get_children(self):
        return self.children

    def add_child(self, child):
        self.children.append(child)

    def get_string(self, level):
        level = 0
        indent = " "*(level*4)
        s = ""
        if self.value is not None:
            s = str(self.value)
        else:
            s = s + indent + "["
            first = True
            for c in self.children:
                if not first:
                    s = s + ", "
                first = False
                cs = c.get_string(level+1)
                s = s + cs
            s = s + indent + "]"
        return indent + s 

    def __str__(self):
        return self.get_string(0)
# tokenizer, returns "OPEN", "CLOSE" or int
def get_tokens(p):
    digits = []
    for i in range(len(p)):
        if p[i] == '[':
            if digits:
                yield "".join(digits)
                digits = []
            yield 'OPEN'
        elif p[i] == ']':
            if digits:
                yield "".join(digits)
                digits = []
            yield 'CLOSE'
        elif p[i] == ',':
            if digits:
                yield "".join(digits)
                digits = []
        else:
            digits.append(p[i])

def tokenize(s):
    return get_tokens(s)

class Tokens:
    def __init__(self, tokenstream):
        self.tokens = list(tokenize(tokenstream))
        self.toklen = len(self.tokens)
        self.ptr = 0

    def get_token(self):
        if self.ptr < self.toklen:
            currtok = self.tokens[self.ptr]
            self.ptr += 1
            return currtok

def create_node(toks, special=False):
    return Node(_make_lists(toks)[0], special)

def _make_lists(toks):
    lists = []
    t = toks.get_token()
    while t:
        if t == 'OPEN':
            sub_list = _make_lists(toks)
            lists.append(sub_list)
        elif t == 'CLOSE':
            return lists
        else:
            lists.append(int(t))
        t = toks.get_token()
    return lists

# return value is either CORRECT, WRONG, KEEP_GOING
CORRECT = 'CORRECT'
WRONG = "WRONG"
KEEP_GOING = "CONTINUE"

def compare_nodes(left,right):
    # both ints
    if left.is_leaf() and right.is_leaf():
        if left.get_value() < right.get_value():
            return CORRECT
        elif left.get_value() > right.get_value():
            return WRONG
        else:
            return KEEP_GOING
    # left int, right list
    elif left.is_leaf() and not right.is_leaf():
        c = compare_nodes(Node([left.get_value()]), right)
        return c
    # left list, right int
    elif not left.is_leaf() and right.is_leaf():
        c = compare_nodes(left, Node([right.get_value()]))
        return c
    elif not left.is_leaf() and not right.is_leaf():
        len_left = len(left.get_children())
        len_right = len(right.get_children())
        
        for i in range(len_left):
            if i >= len_right:
                return WRONG
            c = compare_nodes(left.get_child(i),right.get_child(i))
            if c == CORRECT or c == WRONG:
                return c
        if len_left < len_right:
            return CORRECT
        else:
            return KEEP_GOING

def list_to_str(list):
    s  = str(list)
    return s.replace(' ', '')

def read_puzzle_input(inp):
    packets = []
    for ln in inp:
        ln = ln.strip()
        if ln != "":
            p = create_node(Tokens(ln))
            packets.append(p)
    return packets

def compare2(item1, item2):
    if compare_nodes(item1, item2) == WRONG:
        return -1
    else:
        return 1

from functools import cmp_to_key

def solve(filename):
    dividers = ['[[2]]', '[[6]]']

    with open(filename, "r") as file:
        packets = read_puzzle_input(file)

    for d in dividers:
        packets.append(create_node(Tokens(d), True))
    
    ordered = sorted(packets, key=cmp_to_key(compare2), reverse=True)

    indx = 0
    divs = []
    for p in ordered:
        indx += 1
        if p.special:
            divs.append(indx)
        print(p)
    print(f"secret key: {divs[0]*divs[1]}")

if __name__ == '__main__':

    filename = "13/p1_input.txt"
    solve(filename)
