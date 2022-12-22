from dataclasses import dataclass
import re
import numpy as np
from collections import deque
from math import inf
import networkx as nx
import pprint as pp
import numpy as np
import copy

class Rock:
    def __init__(self, shape):
        self.shape = shape
        self.position = (None,None)

    def set_position(self, position):
        self.position = position

    def get_height(self):
        shape_hgt = max([p[0] for p in self.shape])
        return self.position[0] + shape_hgt + 1

    def get_right_edge_col(self):
        shape_wdth = max([p[1] for p in self.shape])
        return self.position[1] + shape_wdth
    
    def get_points(self):
        points = []
        for offset in self.shape:
            points.append((self.position[0] + offset[0], self.position[1] + offset[1]))
        return points

    def overlaps(self, r):
        # return true if there is any overlap between r and self
        return len(set(self.get_points()).intersection(set(r.get_points()))) != 0

    def move(self, direction):
        if direction == LEFT:
            self.position = (self.position[0], self.position[1]-1)
        elif direction == RIGHT:
            self.position = (self.position[0], self.position[1]+1)
        elif direction == DOWN:
            self.position = (self.position[0]-1, self.position[1])
        else:
            raise Exception('unknown instruction')
        return self

    def is_into_floor(self):
        return self.position[0] < 0

    def is_into_wall(self):
        if self.get_right_edge_col() >= 7:
            return True
        if self.position[1] < 0:
            return True
        return False

HORZ = Rock([(0,0),(0,1),(0,2),(0,3)])
PLUS = Rock([(0,1),(1,0),(1,1),(1,2),(2,1)])
ELL  = Rock([(0,0),(0,1),(0,2),(1,2),(2,2)])
VERT = Rock([(0,0),(1,0),(2,0),(3,0)])
BOX  = Rock([(0,0),(1,0),(1,1),(0,1)])
DOWN='v'
LEFT='<'
RIGHT='>'

rock_sequence = [HORZ, PLUS, ELL, VERT, BOX]


class Game:

    list_of_instructions = []

    def __init__(self, rocks=[], next_rock=0, next_instuction=0):
        self.rocks = rocks
        self.next_rock = next_rock
        self.next_instruction = next_instuction
        self.floor_row = 0
        self.left_col = 0
        self.right_col = 6

    def calculate_max_height(self):
        # if self.rocks: 
        #     return max([r.get_height() for r in self.rocks])
        # else:
        #     return self.floor_row
        max_hgt = 0
        for r in self.rocks:
            h = r.get_height()
            max_hgt = max(max_hgt, h)
        return max_hgt

    def get_next_rock(self):
        indx = self.next_rock
        self.next_rock = advance_index(self.next_rock, len(rock_sequence))
        return copy.copy(rock_sequence[indx])

    def get_next_instruction(self):
        indx = self.next_instruction
        self.next_instruction = advance_index(self.next_instruction, len(Game.list_of_instructions))
        return Game.list_of_instructions[indx]

    def get_number_of_stopped_rocks(self):
        return len(self.rocks)-1

    def add_rock(self, rock):
        h = self.calculate_max_height()
        rock.set_position((h+3, 2))
        self.rocks.append(rock)

    def can_last_rock_move(self, direction):
        last_rock = self.rocks[-1]
        potentially_moved_rock = copy.copy(last_rock).move(direction)
        if potentially_moved_rock.is_into_floor():
            return False
        if potentially_moved_rock.is_into_wall():
            return False
        all_but_last_rock = reversed(self.rocks[:-1])
        for r in all_but_last_rock:
            if potentially_moved_rock.overlaps(r):
                return False
        return True

    def move_last_rock(self, instruction):
        last_rock = self.rocks[-1]
        # copy.copy(last_rock).move(instruction)
        last_rock.move(instruction)
    
    def draw(self):
        max_hgt = self.calculate_max_height() + 10
        canvas = np.zeros(shape=(max_hgt, 7))
        for r in self.rocks:
            points = r.get_points()
            for r,c in points:
                canvas[r,c] = 1

        for r in range(max_hgt-1, -1, -1):
            row = []
            for c in range(0,7):
                if canvas[r,c] == 1:
                    row.append('#')
                elif canvas[r,c] == 0:
                    row.append('.')
            print("".join(row))
        print("-----------------------")

def advance_index(indx, seq_len):
    return indx+1 if indx<seq_len-1 else 0

def read_puzzle_input(inp):
    return list(inp.read().strip())

def solve(filename):
    with open(filename, "r") as file:
        Game.list_of_instructions = read_puzzle_input(file)
        game = Game()
        count  = 0
        # now start the game
        while game.get_number_of_stopped_rocks() < 2022:
            game.draw()
            count += 1
            if count % 1000 == 0:
                print('.')
            # print(f"height after {len(game.rocks)} rocks: {game.calculate_max_height()}")
            new_rock = game.get_next_rock()
            game.add_rock(new_rock)
            # game.draw()
            count2 = 0
            rock_is_stuck = False
            while not rock_is_stuck:
                count2 += 1
                if count2 % 1000 == 0:
                    print('#')
                instruction = game.get_next_instruction()
                if game.can_last_rock_move(instruction):
                    game.move_last_rock(instruction)
                if game.can_last_rock_move(DOWN):
                    game.move_last_rock(DOWN)
                else:
                    rock_is_stuck = True
            # game.draw()

        height = game.calculate_max_height()-1
        print(f"height: {height}")

if __name__ == '__main__':

    filename = "17/p1_input.txt"
    solve(filename)
