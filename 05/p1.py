from dataclasses import dataclass
import re

class SupplyBins:
    def __init__(self, num_bins):
        self.num_bins = int(num_bins)
        self.bins = list()
        self.instructions = list()
        for i in range(0, self.num_bins):
            self.bins.append(list())

    def add_to_stack(self, line):
        for n,b in get_blocks(line):
            self.bins[n].append(b)
    
    def add_instruction(self, ins):
        # each ins is of the form move 2 from 3 to 4
        # which is move 2 blocks from stack 3 to stack 4
        PAT = 'move (\d+) from (\d+) to (\d+)'
        m = re.match(PAT, ins)
        if m:
            num = int(m.group(1))
            frm = int(m.group(2))
            to = int(m.group(3))
            self.instructions.append((num, frm, to))
    
    def execute_instructions(self):
        for (num, fr, to) in self.instructions:
            for n in range(num):
                self.move_item(fr,to)

    def get_top_items(self):
        top = []
        for b in self.bins:
            top.append(b[-1])
        return top
    
    def move_item(self, n,m):
        # moves an item from bin n over to bin m
        x = self.bins[n-1].pop()
        self.bins[m-1].append(x)
    
    def __str__(self):
        s = ""
        i = 0
        for b in self.bins:
            s += 'bin: ' + str(i) + ': ' + str(b) + '\n'
            i += 1
        for b in self.instructions:
            s += 'move: ' + str(b[0]) + ' from: ' + str(b[1]) + ' to: ' + str(b[2]) + '\n'

        return s

filename = "05/test_p1_input.txt"
filename = "05/p1_input.txt"

def get_blocks(line, width=4):
    linelen = len(line)
    p = 0
    PAT = '\[(.)\]'
    ith = 0
    while p < linelen:
        sect = line[p:p+width-1]
        m = re.match(PAT, sect)
        if m:
            yield (ith, m.group(1))
        p += width
        ith += 1

def read_blocks_and_instructions_input(inp):
    # input has two sections
    # first section is the configuration of boxes
    # second section is instuctions to move boxes
    # sections are separated by a blank line
    block_lines = []
    instr_lines = []
    in_blocks = True
    for line in inp:
        # e = parse_line(line)
        e = line
        if e == '\n':
            in_blocks = False
            continue
        if in_blocks:
            block_lines.append(e)
        else:
            instr_lines.append(e)
    return (block_lines, instr_lines)

BIN_WIDTH = 4

def read_puzzle_input(inp):
    bl, il = read_blocks_and_instructions_input(inp)
    num_bins = len(bl[-1]) / BIN_WIDTH
    sb = SupplyBins(num_bins)

    for b in reversed(bl[0:len(bl)-1]):
        sb.add_to_stack(b)

    for ins in il:
        sb.add_instruction(ins)

    return sb


with open(filename, "r") as file:
    bl = read_puzzle_input(file)
    top = bl.get_top_items()
    print("top: " + str(top))
    print(bl)
    print('---------------')
    bl.execute_instructions()
    top = bl.get_top_items()
    print("top: " + str(top))
    print(bl)
    print("".join(top))

