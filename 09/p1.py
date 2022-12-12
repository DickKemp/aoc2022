from dataclasses import dataclass
import re
import numpy as np

class Piece:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move_up(self):
        return Piece(self.x, self.y-1)
        
    def move_down(self):
        return Piece(self.x, self.y+1)
        
    def move_left(self):
        return Piece(self.x-1, self.y)
        
    def move_right(self):
        return Piece(self.x+1, self.y)

    @staticmethod
    def is_touching(p1, p2):
        if abs(p1.x - p2.x) == 0:
            if abs(p1.y - p2.y) <= 1:
                return True
            else:
                return False

        if abs(p1.y - p2.y) == 0:
            if abs(p1.x - p2.x) <= 1:
                return True
            else:
                return False

        if abs(p1.x - p2.x) + abs(p1.y - p2.y) <= 2:
            return True

        return False

    def __str__(self):
        return "<" + str(self.x) + ", " + str(self.y) + ">"

class Board:

    def __init__(self, head, tail):
        self.head = head
        self.tail = tail
        self.tail_visited = set()
        self.tail_visited.add((self.tail.x, self.tail.y))

    def move_head_up(self):
        new_head = self.head.move_up()
        if not Piece.is_touching(self.tail, new_head):
            self.tail = self.head
        self.head = new_head
        self.tail_visited.add((self.tail.x, self.tail.y))

    def move_head_down(self):
        new_head = self.head.move_down()
        if not Piece.is_touching(self.tail, new_head):
            self.tail = self.head
        self.head = new_head
        self.tail_visited.add((self.tail.x, self.tail.y))


    def move_head_left(self):
        new_head = self.head.move_left()
        if not Piece.is_touching(self.tail, new_head):
            self.tail = self.head
        self.head = new_head
        self.tail_visited.add((self.tail.x, self.tail.y))

    def move_head_right(self):
        new_head = self.head.move_right()
        if not Piece.is_touching(self.tail, new_head):
            self.tail = self.head
        self.head = new_head
        self.tail_visited.add((self.tail.x, self.tail.y))

    def apply_moves(self, moves):
        for m in moves:
            if m[0] == 'U':
                num = int(m[1])
                for n in range(num):
                    self.move_head_up()
            elif m[0] == 'D':
                num = int(m[1])
                for n in range(num):
                    self.move_head_down()
            elif m[0] == 'R':
                num = int(m[1])
                for n in range(num):
                    self.move_head_right()
            elif m[0] == 'L':
                num = int(m[1])
                for n in range(num):
                    self.move_head_left()

    def __str__(self):
        # s = "visited: "
        # for p in self.tail_visited:
        #     s = s + str(p) + ", "
        # return "head:\n" + str(self.head) + "\ntail:\n" + str(self.tail) + "\n" + s
        return "num visited: " + str(len(self.tail_visited))

def read_puzzle_input(inp):
    rows = list()
    for ln in inp:
        ln = ln.strip()
        rows.append(ln.split())
    return rows

def solve(filename):
    with open(filename, "r") as file:
        moves = read_puzzle_input(file)
        board = Board(Piece(0,0), Piece(0,0))
        board.apply_moves(moves)
        print(str(board))

if __name__ == '__main__':

    filename = "09/p1_input.txt"
    solve(filename)
