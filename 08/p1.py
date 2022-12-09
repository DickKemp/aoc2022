from dataclasses import dataclass
import re
import numpy as np

class Forest:

    def __init__(self):
        self.messages = list()
    def add_trees(self, list_of_lists):
        self.trees = np.array(list_of_lists)
        self.row_len = self.trees.shape[0]
        self.col_len = self.trees.shape[1]
        self.visible_vert = np.ndarray(shape=self.trees.shape, dtype=int)
        self.visible_vert[:,:] = 0
        self.visible_horz = np.ndarray(shape=self.trees.shape, dtype=int)        
        self.visible_horz[:,:] = 0
        self._set_edge_visibility_to_true()

    def _set_edge_visibility_to_true(self):
        self.visible_vert[0,:] = 1
        self.visible_vert[self.row_len-1,:] = 1
        self.visible_vert[:,0] = 1
        self.visible_vert[:, self.col_len-1] = 1

        self.visible_horz[0,:] = 1
        self.visible_horz[self.row_len-1,:] = 1
        self.visible_horz[:,0] = 1
        self.visible_horz[:, self.col_len-1] = 1

    def get_height(self,x,y):
        return self.trees[x,y]

    def is_tree_visible_left(self, x,y, gt=True):
            if self.visible_horz[x,y] > 0:
                return True
            #elif self.visible_horz[x,y] < 0:
                return False
            else:
                tree_height_current = self.get_height(x, y) 
                tree_visible_left = self.is_tree_visible_left(x, y-1, False)
                if tree_visible_left:
                    tree_height_left = self.get_height(x, y-1) 
                    if (gt and tree_height_left < tree_height_current) or tree_height_left <= tree_height_current:
                        return True
                self.set_tree_visible_horizontally(x, y, -1)
                return False

    def is_tree_visible_right(self, x,y, gt=True):
            if self.visible_horz[x,y] > 0:
                return True
            # elif self.visible_horz[x,y] < 0:
            #    return False
            else:
                tree_height_current = self.get_height(x, y) 
                tree_visible_right = self.is_tree_visible_right(x, y+1, False)
                if tree_visible_right:
                    tree_height_right = self.get_height(x, y+1) 
                    if (gt and tree_height_right < tree_height_current) or tree_height_right <= tree_height_current:
                        self.set_tree_visible_horizontally(x, y, 1)
                        return True
                return False

    def is_tree_visible_above(self, x,y, gt=True):
            if self.visible_vert[x,y] > 0:
                return True
            #elif self.visible_vert[x,y] < 0:
            #    return False
            else:
                tree_height_current = self.get_height(x, y) 
                tree_visible_above = self.is_tree_visible_above(x-1, y, False)
                if tree_visible_above:
                    tree_height_above = self.get_height(x-1, y) 
                    if (gt and tree_height_above < tree_height_current) or tree_height_above <= tree_height_current:
                        self.set_tree_visible_vertically(x, y, 1)
                        return True
                return False

    def is_tree_visible_below(self, x,y, gt=True):
            if self.visible_vert[x,y] > 0:
                return True
            #elif self.visible_vert[x,y] < 0:
            #    return False
            else:
                tree_height_current = self.get_height(x, y) 
                tree_visible_below = self.is_tree_visible_below(x+1, y, False)
                if tree_visible_below:
                    tree_height_below = self.get_height(x+1, y) 
                    if (gt and tree_height_below < tree_height_current) or tree_height_below <= tree_height_current:
                        self.set_tree_visible_vertically(x, y, 1)
                        return True
                return False

    def set_tree_visible_horizontally(self, x, y, val):
        self.visible_horz[x,y] = val
    def set_tree_visible_vertically(self, x, y, val):
        self.visible_vert[x,y] = val


    def calc(self):
        for i in range(self.row_len):
            for j in range(self.col_len):
                if not (self.is_tree_visible_above(i,j) or self.is_tree_visible_below(i,j)):
                    self.set_tree_visible_vertically(i, j, -1)
                if not (self.is_tree_visible_left(i,j) or self.is_tree_visible_right(i,j)):
                    self.set_tree_visible_horizontally(i, j, -1)

    def __str__(self):
        return "trees:\n" + str(self.trees) + "\nvert_visible\n" + str(self.visible_vert) + "\nhorz_visible\n" + str(self.visible_horz)

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

if __name__ == '__main__':

    filename = "08/test_p1_input.txt"
    solve(filename)
