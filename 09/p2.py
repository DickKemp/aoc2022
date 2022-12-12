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

    def __eq__(self, b):
        return self.x == b.x and self.y == b.y

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

    def __init__(self, pieces):
        self.pieces = pieces
        self.num_pieces = len(pieces)
        self.tail_visited = list()
        self.tail_visited.append((self.pieces[-1].x, self.pieces[-1].y))

    def update_all_pieces(self, new_p):
        
        new_pieces = list()
        for i in range(0, self.num_pieces):
            new_pieces.append(self.pieces[i])
        new_pieces[0] = new_p

        # if new head moves too far away from the origignal tail
        # then update the new tail to the new position, based on
        # updated algorithm implemented by Board.move_tail()

        for i in range(0, self.num_pieces-1):
            if self.pieces[i] == new_pieces[i]:
                break
            
            if not Piece.is_touching(self.pieces[i+1], new_pieces[i]):
                x,y = Board.move_tail(new_pieces[i].x, new_pieces[i].y, self.pieces[i+1].x, self.pieces[i+1].y)
                new_pieces[i+1] = Piece(x,y)

        self.tail_visited.append((new_pieces[-1].x, new_pieces[-1].y))
        self.pieces = new_pieces

    def move_head_up(self):
        new_head = self.pieces[0].move_up()
        self.update_all_pieces(new_head)

    def move_head_down(self):
        new_head = self.pieces[0].move_down()
        self.update_all_pieces(new_head)

    def move_head_left(self):
        new_head = self.pieces[0].move_left()
        self.update_all_pieces(new_head)

    def move_head_right(self):
        new_head = self.pieces[0].move_right()
        self.update_all_pieces(new_head)        

    # Based on current position of head (xh, yh) and tail (xt, yt) determine
    # by the movement rules what the new position of the tail should be.
    # borrowed this method from the subredit
    @staticmethod
    def move_tail(xh, yh, xt, yt):
        dx = xh - xt
        dy = yh - yt
        if dx > 1:
            xt += 1
            if dy > 0:
                yt += 1
            elif dy < 0:
                yt -= 1
        elif dx < -1:
            xt -= 1
            if dy > 0:
                yt += 1
            elif dy < 0:
                yt -= 1
        elif dy > 1:
            yt += 1
            if dx > 0:
                xt += 1
            elif dx < 0:
                xt -= 1
        elif dy < -1:
            yt -= 1
            if dx > 0:
                xt += 1
            elif dx < 0:
                xt -= 1
        return (xt, yt)

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

    def get_visited_list(self):
        vl = []
        for v in self.tail_visited:
            vl.append("p:" + str(v))
        return(vl)

    def __str__(self):
        steps = len(self.tail_visited)
        unique_steps = len(set(self.tail_visited))
        s = ""
        return s + "\n\nnum visited: " + str(unique_steps)

def read_puzzle_input(inp):
    rows = list()
    for ln in inp:
        ln = ln.strip()
        rows.append(ln.split())
    return rows

def solve(filename):
    with open(filename, "r") as file:
        moves = read_puzzle_input(file)
        pieces10 = [Piece(0,0), Piece(0,0),Piece(0,0), Piece(0,0),Piece(0,0), Piece(0,0),Piece(0,0), Piece(0,0),Piece(0,0), Piece(0,0)]
        #pieces3 = [Piece(0,0), Piece(0,0),Piece(0,0)]
        board = Board(pieces10)
        # print(str(board))
        board.apply_moves(moves)
        # print(str(board.get_visited_list()))
        print(str(board))

if __name__ == '__main__':

    #filename = "09/test_small_p2_input.txt"
    filename = "09/p1_input.txt"
    solve(filename)
