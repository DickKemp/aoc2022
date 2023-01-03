from dataclasses import dataclass
import re
import numpy as np
from collections import deque
from math import inf
import networkx as nx
import pprint as pp
import numpy as np
import copy
import functools

class CircularList:
    def __init__(self, initial):
        self.items = initial

    def find_position_of_elem(self, elem):
        elems = [e.elem for e in self.items]
        return elems.index(elem)

    def find_position_of_ith_item(self, ith):
        items = [e.indx for e in self.items]
        return items.index(ith)

    def get_elem_at_position(self, pos):
        return self.items[pos%len(self.items)].elem
        
    def move_elem(self, indx_of_item_to_move, amt_to_move):
        item = self.items.pop(indx_of_item_to_move)
        moved_to_index = (indx_of_item_to_move + amt_to_move) % len(self.items)
        self.items.insert(moved_to_index, item)

    def __str__(self):
        return f"{self.items}"

class Item:
    def __init__(self, elem, indx):
        self.elem = elem * 811589153
        self.indx = indx

    def __str__(self):
        return f"{self.elem}/{self.indx}"
    
def read_puzzle_input(inp):
    items = []
    indx = 0
    for ln in inp:
        items.append( Item(int(ln.strip()), indx) )
        indx += 1
    return items

def solve(filename):
    with open(filename, "r") as file:
        items = read_puzzle_input(file)

    cl = CircularList(items)
    
    for nth in range(0,10):
        for ith in range(0, len(cl.items)):
            indx = cl.find_position_of_ith_item(ith)
            num_to_move = cl.get_elem_at_position(indx)
            cl.move_elem(indx, num_to_move)

    zero = cl.find_position_of_elem(0)
    one_t = zero + 1000
    two_t = zero + 2000
    three_t = zero + 3000
    e1 = cl.get_elem_at_position(one_t)
    e2 = cl.get_elem_at_position(two_t)
    e3 = cl.get_elem_at_position(three_t)

    print(f"e1: {e1}, e2: {e2}, e3: {e3}, sum: {e1+e2+e3}")

if __name__ == '__main__':

    filename = "20/input.txt"
    solve(filename)
