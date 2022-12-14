from dataclasses import dataclass
import re
import numpy as np

class Program:
    
    def __init__(self):
        self.instructions = list()

    def load_instruction(self, instr, arg):
        self.instructions.append((instr, arg))

    @staticmethod
    def abc(p1, p2):
        return False

    def __str__(self):
        return str(self.instructions)

class Machine:
    def __init__(self):
        self.registers = list()
        self.registers.append(int(1))  # reg at time 0 is 1
        self.curr_time = 0             # start at time 1

    def load_to_register(self, v):
        self.registers.append(v)
        self.curr_time += 1

    def advance_register(self):
        reg_val = self.get_reg_val_at_time(self.curr_time)
        self.registers.append(reg_val)
        self.curr_time += 1

    def get_reg_val_at_time(self, t):
        return self.registers[t]

    def execute_noop(self):
        self.advance_register()

    def execute_addx(self, arg):
        reg_val = self.get_reg_val_at_time(self.curr_time)
        self.advance_register()
        self.load_to_register(reg_val + arg)

    def execute(self, program):

        for inst in program.instructions:
            if inst[0] == 'noop':
                self.execute_noop()
                
            elif inst[0] == 'addx':
                self.execute_addx(inst[1])
    def __str__(self):
        s = ""
        i = 0
        for r in self.registers:
            s = s + "\n" + str(i) + ": " +  str(r)
            i += 1
        return s

def read_puzzle_input(inp):
    p = Program()
    for ln in inp:
        ln = ln.strip()
        instr = tuple(ln.split())
        if len(instr) == 1:
            p.load_instruction('noop', None)
        else:
            p.load_instruction(instr[0], int(instr[1]))
    return p

def solve(filename):
    with open(filename, "r") as file:
        inp = read_puzzle_input(file)
        machine = Machine()
        machine.execute(inp)
        # board = Board(Piece(0,0), Piece(0,0))
        # board.apply_moves(moves)
        # print(str(board))
        print(machine)
        print("----------------")
        total = 0
        for c in [20, 60, 100, 140, 180, 220]:
            print(f'{c}: {machine.registers[c-1]}')
            s = c * machine.registers[c-1]
            total += s
        print(f"answer: {total}")

if __name__ == '__main__':

    filename = "10/p1_input.txt"
    solve(filename)
