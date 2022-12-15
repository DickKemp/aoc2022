from dataclasses import dataclass
import re
import numpy as np
from collections import deque
from math import inf

@dataclass
class Point:
    r: int
    c: int
    

class Line:
    from_pt: Point
    to_pt: Point

class Cave:

    def __init__(self, paths):
        self.paths = paths
        self.sand_source = Point(0,500)
        self.current_grain_location = None
        self._find_extents()

        self.top = 0
        self.bottom = self.maxpoint.r+1
        self.bottom = self.bottom + 1 # add this for the floor
        self.left = self.minpoint.c
        self.right = self.maxpoint.c+1

        self.grid = np.zeros(shape=(self.bottom+100, self.right+1000))
        for path in self.paths:
            self._insert_rocks(path)

        self.floor = self.bottom 

    def _find_extents(self):
        self.minpoint = Point(inf,inf)
        self.maxpoint = Point(0, 0)

        for line in self.paths:
            for point in line:
                self.minpoint.c = min(point.c, self.minpoint.c)
                self.minpoint.r = min(point.r, self.minpoint.r)
                self.maxpoint.c = max(point.c, self.maxpoint.c)
                self.maxpoint.r = max(point.r, self.maxpoint.r)

    def reset(self):
        self._generate_new_grain()
        return True

    def can_move(self, pt):
        down = Point(pt.r+1, pt.c)    
        down_left = Point(pt.r+1, pt.c-1)
        down_right = Point(pt.r+1, pt.c+1)
        
        if not self.is_occupied(down):
            return down

        if not self.is_occupied(down_left):
            return down_left

        if not self.is_occupied(down_right):
            return down_right
        else:
            return None

    def run(self, n):

        for i in range(n):
            # will throw an exception if the move pushs the piece off the edge
            new_pos = self.can_move(self.current_grain_location)

            if new_pos is not None:
                self.move(self.current_grain_location, new_pos)
                self.current_grain_location = new_pos
            else:
                self._generate_new_grain()


    def move(self, curr_pt, pt):
        self.grid[curr_pt.r, curr_pt.c] = 0
        self.grid[pt.r, pt.c] = 2

    def remove(self, pt):
        self.grid[pt.r, pt.c] = 0

    def _is_abyss_pathway(self, pt):
        """ in part 2, there is no abyss
        """
        return False

    def is_floor(self, pt):
         return pt.r == self.floor

    def is_occupied(self, pt):
        occ = self.grid[pt.r, pt.c] != 0
        return pt.r == self.floor or occ

    def _generate_new_grain(self):
        self.current_grain_location = self.sand_source
        return self.current_grain_location

    @staticmethod
    def _get_pairs(lst):
        for i in range(len(lst)-1):
            yield (lst[i], lst[i+1])

    def count_sand(self):
        return (self.grid == 2).sum()

    def _insert_rocks(self, path):
        for (p1, p2) in Cave._get_pairs(path):
            if p1.c == p2.c:
                strt = min([p1.r,p2.r])
                end = max([p1.r,p2.r])
                for r in range(strt,end+1):
                    self._insert_rock(r, p1.c)
            elif p1.r == p2.r:
                strt = min([p1.c,p2.c])
                end = max([p1.c,p2.c])
                for c in range(strt,end+1):
                    self._insert_rock(p1.r, c)
        return True

    def _insert_rock(self, r, c):
        self.grid[r,c] = 1

    def draw(self):
        print("cave")
        # print(self.paths)
        # print(f"min: {self.minpoint}, max: {self.maxpoint}")
        # print(f"grid{self.top}:{self.bottom}, {self.left}:{self.right}")
        # print(self.grid[self.top:self.bottom, self.left:self.right])
        # print("")
        for r in range(self.top, self.bottom):
            row = []
            row.append(str(r).zfill(3))
            row.append(' ')
            for c in range(self.left-10, self.right+10):
                if self.grid[r,c] == 1:
                    row.append('#')
                elif self.grid[r,c] == 2:
                    row.append('o')
                else:
                    if r == 0 and c == 500:
                        row.append('V')
                    else:
                        row.append('.')                
                    
            print("".join(row))

    def __str__(self):
        return "hello"

def read_puzzle_input(inp):
    paths = []
    """the input line segment is expressed as a pair of points as col,row -> col,row, wwhich is
    column,row indicating the cooridnate.
    However, our grid coordinates is indexed by (row,col) 
    Need to be careful with this
    """
    for ln in inp:
        ln = ln.strip()
        path_str = [s.strip() for s in ln.split('->')]
        path_int = [Point(int(p[1]), int(p[0])) for p in [x.split(',') for x in path_str]]
        paths.append(path_int)
    return paths

def solve(filename):
    with open(filename, "r") as file:
        paths = read_puzzle_input(file)
    cave = Cave(paths)
    #cave.draw()
    #cave.run(10)
    #cave.draw()
    # cave.run(5000)
    cave.draw()
    cave.reset()
    cave.run(20000001)
    cave.draw()

    cnt = cave.count_sand() + 1

    print("count: " + str(cnt))

if __name__ == '__main__':

    filename = "14/p1_input.txt"
    solve(filename)
