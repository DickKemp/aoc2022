from dataclasses import dataclass
import re
import numpy as np
from collections import deque
from math import inf
import networkx as nx
import pprint as pp
import numpy as np
import copy

class Instruction:
    def __init__(self, map, op, arg1, arg2=None):
        self.map = map
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2

    def calc(self):
        if self.op == '=':
            return int(self.arg1)
        elif self.op == '+':
            opr1 = self.map[self.arg1]
            opr2 = self.map[self.arg2]
            return int(opr1.calc()) + int(opr2.calc())
        elif self.op == '-':
            opr1 = self.map[self.arg1]
            opr2 = self.map[self.arg2]
            return int(opr1.calc()) - int(opr2.calc())
        elif self.op == '*':
            opr1 = self.map[self.arg1]
            opr2 = self.map[self.arg2]
            return int(opr1.calc()) * int(opr2.calc())
        elif self.op == '/':
            opr1 = self.map[self.arg1]
            opr2 = self.map[self.arg2]
            return int(opr1.calc()) / int(opr2.calc())

def read_puzzle_input(inp):
    """ input looks like this:
        pngc: vdvn + qtgs
        hmtl: 3
    """
    PAT = "(.+):(.+)([+-/*])(.+)"
    PAT2 = "(.+): (\d+)"
    instructions_map = {}
    for ln in inp:
        ln = ln.strip()
        m = re.match(PAT, ln)
        if m:
            instructions_map[m.group(1).strip()] = Instruction(instructions_map, m.group(3).strip(), m.group(2).strip(), m.group(4).strip())
        else:
            m = re.match(PAT2, ln)
            if m:
                instructions_map[m.group(1).strip()] = Instruction(instructions_map, '=', m.group(2).strip())
            else:
                print(f"cannot parse: {ln}")
    return instructions_map
    
def solve(filename):

    with open(filename, "r") as file:
        instuctions = read_puzzle_input(file)

    pp.pprint(instuctions)
    root = instuctions['root']
    print(f"root: {root.calc()}")

if __name__ == '__main__':

    filename = "21/p1_input.txt"
    solve(filename)
