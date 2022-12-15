from dataclasses import dataclass
import re
import numpy as np
from collections import deque



class Node:
    def __init__(self, v):
        if type(v) is list:
            self.children = [Node(c) for c in v]
            self.value = None
        else:
            self.children = None
            self.value = int(v)

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
        indent = " "*(level*4)
        s = ""
        if self.value:
            s = str(self.value)
        else:
            s = s + indent + "["
            for c in self.children:
                cs = c.get_string(level+1)
                s = s + cs
            s = s + indent + "]"
        return indent + s + "\n"

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

def create_node(toks):
    return Node(_make_lists(toks)[0])

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

def read_puzzle_input(inp):
    pairs = []
    pair = []
    for ln in inp:
        ln = ln.strip()
        if ln == "":
            pairs.append((pair[0], pair[1]))
            pair = []
        else:
            p = ln
            pair.append(p)
    pairs.append((pair[0], pair[1]))
    return pairs
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

def solve(filename):
    with open(filename, "r") as file:
        packet_pairs = read_puzzle_input(file)
        compare_index = 0
        index_sum = 0
        for pair in packet_pairs:
            for p in pair:
                out = _make_lists(Tokens(p))
                # print(f" in: {p}")
                # print(f"out: {list_to_str(out)}")
            # print(f"compare {pair[0]} and {pair[1]}")
            result = compare_nodes(create_node(Tokens(pair[0])), create_node(Tokens(pair[1])))
            compare_index += 1
            if result == CORRECT:
                index_sum += compare_index
                print(f"FOUND CORRECT {pair[0]}")
                print(f"              {pair[1]}")
            print("------------------")
            
    print(index_sum)

if __name__ == '__main__':

    filename = "13/p1_input.txt"
    solve(filename)
