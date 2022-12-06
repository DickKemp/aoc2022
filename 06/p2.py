from dataclasses import dataclass
import re

class Window:

    def __init__(self):
        self.messages = list()

    def add_message(self, msg):
        self.messages.append(msg)

    def get_start_positions(self):
        res = list()
        for m in self.messages:
            res.append(self.calc_start_position(m))
        return res
    
    def calc_start_position(self, msg):
        WINDOW_SIZE = 14
        msg_len = len(msg)
        for i in range(0, msg_len - WINDOW_SIZE):
            window = msg[i:i+WINDOW_SIZE]
            if len(set(window)) == WINDOW_SIZE:
                return i + WINDOW_SIZE
        return -1

filename = "06/test_p1_input.txt"
filename = "06/p1_input.txt"

def read_puzzle_input(inp):
    w = Window()
    for line in inp:
        w.add_message(line)
    return w

with open(filename, "r") as file:
    bl = read_puzzle_input(file)
    r = bl.get_start_positions()
    print(r)
