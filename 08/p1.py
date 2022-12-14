from dataclasses import dataclass
import re
import numpy as np

class Forest:

    def __init__(self):
        pass

    def add_trees(self, list_of_lists):
        self.trees = np.array(list_of_lists)
        self.row_len = self.trees.shape[0]
        self.col_len = self.trees.shape[1]
        self.visible = np.ndarray(shape=self.trees.shape, dtype=int)
        self.visible[:,:] = 0

    def get_height(self,x,y):
        return self.trees[x,y]
    
    def is_on_edge(self, x, y):
        return x == 0 or y == 0 or x == self.col_len-1 or y == self.row_len-1
        
    def is_visible_from_outside(self, x, y):
        h = self.row_len
        w = self.col_len

        """
        right:  range(x+1,w)
        left: range(x-1,-1)
        up: range(y-1,-1)
        down: range(y+1,h)
        """
        if self.is_on_edge(x, y):
            return True

        height_of_pt = self.get_height(x,y)

        blocked = False
        for i in range(x+1,w):
            if height_of_pt <= self.get_height(i,y):
                blocked = True
        if not blocked:
            return True

        blocked = False
        for i in range(x-1,-1,-1):
            if height_of_pt <= self.get_height(i,y):
                blocked = True
        if not blocked:
            return True

        blocked = False
        for i in range(y-1,-1,-1):
            if height_of_pt <= self.get_height(x,i):
                blocked = True
        if not blocked:
            return True

        blocked = False
        for i in range(y+1, h):
            if height_of_pt <= self.get_height(x,i):
                blocked = True
        if not blocked:
            return True

        return False

    def set_tree_visible(self, x, y, val=1):
        self.visible[x,y] = val

    def calc(self):
        for i in range(self.row_len):
            for j in range(self.col_len):
                if self.is_visible_from_outside(i, j):
                    self.set_tree_visible(i, j)

    def count_visible(self):
        count = 0
        for i in range(self.row_len):
            for j in range(self.col_len):
                if self.visible[i,j] == 1:
                    count += 1
        return count

    def __str__(self):
        return "trees:\n" + str(self.trees) + "\nvisible\n" + str(self.visible)

def read_puzzle_input(inp):
    forest = Forest()
    rows = list()
    for ln in inp:
        ln = ln.strip()
        rows.append(list(ln))
    
    forest.add_trees(rows)
    return forest

def solve(filename):
    with open(filename, "r") as file:
        forest = read_puzzle_input(file)
        forest.calc()
        print(forest)
        print("count visible: " + str(forest.count_visible()))

if __name__ == '__main__':

    filename = "08/p1_input.txt"
    solve(filename)
