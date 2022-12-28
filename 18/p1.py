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

face_left =   [Point(0,0,0),Point(0,0,1),Point(1,0,0),Point(1,0,1)]
face_back =   [Point(0,0,0),Point(0,0,1),Point(0,1,0),Point(0,1,1)]
face_bottom = [Point(0,0,0),Point(0,1,0),Point(1,0,0),Point(1,1,0)]
face_front =  [Point(1,0,0),Point(1,0,1),Point(1,1,0),Point(1,1,1)]
face_top =    [Point(0,0,1),Point(0,1,1),Point(1,0,1),Point(1,1,1)]
face_right =  [Point(0,1,0),Point(0,1,1),Point(1,1,0),Point(1,1,1)]


all_faces = set()

faces_offsets = [face_left, face_back, face_bottom, face_front, face_top, face_right]

def get_face_offset(p, face_offsets):
    return [(p[0]+o[0], p[1]+o[1], p[2]+o[2]) for o in face_offsets]
def get_faces(p):
    faces_offsets = [face_left, face_back, face_bottom, face_front, face_top, face_right]
    return [Face([Point(p.x+f.x,p.y+f.y,p.z+f.z) for f in face]) for face in faces_offsets]

def solve(filename):
    with open(filename, "r") as file:
        points = read_puzzle_input(file)
    faces_touching_counter=0
    for p in points:
        faces = get_faces(p)
        for f in faces:
            if f in all_faces:
                faces_touching_counter += 1
                #print(f"face match: {f}")
            else:
                all_faces.add(f)
    num_cubes = len(points)
    print(f"num cubes = {num_cubes}, total faces: {num_cubes*6}")
    print(f"covered faces = {faces_touching_counter}, faces_uncovered: {(num_cubes*6) - (faces_touching_counter*2)}")
if __name__ == '__main__':

    filename = "18/p1_input.txt"
    solve(filename)
