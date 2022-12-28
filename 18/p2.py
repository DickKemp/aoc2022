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
class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y and self.z == __o.z

    def __hash__(self) -> int:
        return hash(tuple([self.x,self.y,self.z]))
    
    def __str__(self) -> str:
        return f"{self.x}, {self.y}, {self.z}"
        
def compare_points(p1, p2):
    if p1.x < p2.x:
        return -1
    elif p1.x > p2.x:
        return 1
    else:
        if p1.y < p2.y:
            return -1
        elif p1.y > p2.y:
            return 1
        else:
            if p1.z < p2.z:
                return -1
            elif p1.z > p2.z:
                return 1
    return 0

class Face:
    def __init__(self, points):
        self.face_points = sorted(points, key=functools.cmp_to_key(compare_points))

    def __eq__(self, __o: object) -> bool:
        return self.face_points[0] == __o.face_points[0] and self.face_points[1] == __o.face_points[1] and \
            self.face_points[2] == __o.face_points[2] and self.face_points[3] == __o.face_points[3]

    def __hash__(self) -> int:
        return hash(tuple(self.face_points))

    def __str__(self) -> str:
        return f"({self.face_points[0]}) ({self.face_points[1]}) ({self.face_points[2]}) ({self.face_points[3]})"

        return f"({self.x}, {self.y}, {self.z})"

def read_puzzle_input(inp):
    points = []
    for ln in inp:
        ln = ln.strip()
        point = tuple([int(x.strip()) for x in ln.split(',')])
        points.append(Point(point[0], point[1], point[2]))
    return points

def get_faces(p):
    face_left =   [Point(0,0,0),Point(0,0,1),Point(1,0,0),Point(1,0,1)]
    face_back =   [Point(0,0,0),Point(0,0,1),Point(0,1,0),Point(0,1,1)]
    face_bottom = [Point(0,0,0),Point(0,1,0),Point(1,0,0),Point(1,1,0)]
    face_front =  [Point(1,0,0),Point(1,0,1),Point(1,1,0),Point(1,1,1)]
    face_top =    [Point(0,0,1),Point(0,1,1),Point(1,0,1),Point(1,1,1)]
    face_right =  [Point(0,1,0),Point(0,1,1),Point(1,1,0),Point(1,1,1)]
    faces_offsets = [face_left, face_back, face_bottom, face_front, face_top, face_right]
    return [Face([Point(p.x+f.x,p.y+f.y,p.z+f.z) for f in face]) for face in faces_offsets]


def get_possible_invisible_origins(origins):
    for p in origins:
        faces = get_faces(p)
        for f in faces:
            for i in range(1,4):
                o = f.face_points[i]
                if o not in origins:
                    yield o

def check_if_all_faces_are_real_faces(origin, all_faces):
    faces = get_faces(origin)
    for f in faces:
        if f not in all_faces:
            return False
    return True
class MinMax:
    def __init__(self):
        self.x_min = inf
        self.x_max = -inf
        self.y_min = inf
        self.y_max = -inf
        self.z_min = inf
        self.z_max = -inf

    # def add(self, p):
    #     self.add(p.x, p.y, p.z)
    def xd(self):
        return self.x_max - self.x_min
    def yd(self):
        return self.y_max - self.y_min
    def zd(self):
        return self.z_max - self.z_min
    def add(self, x, y, z):
        self.x_min = min(x, self.x_min)
        self.x_max = max(x, self.x_max)
        self.y_min = min(y, self.y_min)
        self.y_max = max(y, self.y_max)
        self.z_min = min(z, self.z_min)
        self.z_max = max(z, self.z_max)
        
class Queue:
    def __init__(self):
        self.q = []
    def add(self, x):
        self.q.append(x)
    def remove(self):
        if self.q:
            return self.q.pop(0)
        else:
            return None
    def empty(self):
        return len(self.q) == 0
    def __str__(self):
        return f"{list(reversed(self.q))}"

DIRECTIONS = ['n','s','e','w','u','d']        

class Box:
    def __init__(self, min_pt, max_pt, all_origins, all_faces):
        self.min_pt = min_pt
        self.max_pt = max_pt
        self.filled_w_steam = set()
        self.node_queue = Queue()
        self.all_origins = all_origins
        self.all_faces = all_faces

    def flood(self, node):
        """
        Flood-fill (node):
            1. Set Q to the empty queue or stack.
            2. Add node to the end of Q.
            3. While Q is not empty:
            4.   Set n equal to the first element of Q.
            5.   Remove first element from Q.
            6.   If n is Inside:
                    Set the n
                    Add the node to the west of n to the end of Q.
                    Add the node to the east of n to the end of Q.
                    Add the node to the north of n to the end of Q.
                    Add the node to the south of n to the end of Q.
            7. Continue looping until Q is exhausted.
            8. Return.
        """
        surface_face_count = 0
        # surface_faces = set()
        
        self.node_queue.add(node)
        while not self.node_queue.empty():
            n = self.node_queue.remove()
            # first make sure that this dube (as defined by the node n) is not one of the originally planted cubes
            if n in self.all_origins:
                continue
            if n in self.filled_w_steam:
                continue
            self.filled_w_steam.add(n)
            cnt = self.count_num_faces_touching_original_surface(n)
            surface_face_count += cnt
            for dir in DIRECTIONS:
                if self.can_move(n, dir):
                    self.node_queue.add(self.move_in_direction(n, dir))

        return surface_face_count

    def count_num_faces_touching_original_surface(self, node):
        cnt = 0
        for f in get_faces(node):
            if f in self.all_faces:
                cnt += 1
        return cnt

    def can_move(self, pt, direction):
        if direction == 'n' and pt.x >= self.max_pt.x:
            return False
        elif direction == 's' and pt.x <= self.min_pt.x:
            return False
        elif direction == 'e' and pt.z <= self.min_pt.z:
            return False
        elif direction == 'w' and pt.z >= self.max_pt.z:
            return False
        elif direction == 'u' and pt.y >= self.max_pt.y:
            return False
        elif direction == 'd' and pt.y <= self.min_pt.y:
            return False
        else:
            return True
    
    def move_in_direction(self, pt, direction):
        if direction == 'n':
            return Point(pt.x+1, pt.y, pt.z)
        elif direction == 's':
            return Point(pt.x-1, pt.y, pt.z)
        elif direction == 'e':
            return Point(pt.x, pt.y, pt.z-1)
        elif direction == 'w':
            return Point(pt.x, pt.y, pt.z+1)
        elif direction == 'u':
            return Point(pt.x, pt.y+1, pt.z)            
        elif direction == 'd':
            return Point(pt.x, pt.y-1, pt.z)
        raise Exception("bad direction")

def solve(filename):
    mm = MinMax()

    with open(filename, "r") as file:
        points = read_puzzle_input(file)
    faces_touching_counter=0
    all_faces = set()
    all_origins = set()
    faces_touching_faces = set()
    for p in points:
        mm.add(p.x, p.y, p.z)
        mm.add(p.x, p.y, p.z)
        all_origins.add(p)
        faces = get_faces(p)
        for f in faces:
            all_faces.add(f)

    min_pt = Point(mm.x_min-1, mm.y_min-1, mm.z_min-1)
    max_pt = Point(mm.x_max+1, mm.y_max+1, mm.z_max+1)
    box = Box(min_pt, max_pt, all_origins, all_faces)

    surface_count = box.flood(Point(mm.x_min, mm.y_min, mm.z_min))
    print(f"surface_count: {surface_count}")

if __name__ == '__main__':

    filename = "18/p1_input.txt"
    solve(filename)
