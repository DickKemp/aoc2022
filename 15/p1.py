from dataclasses import dataclass
import re
import numpy as np
from collections import deque
from math import inf

@dataclass
class Point:
    r: int
    c: int
    def __hash__(self) -> int:
        return hash((self.r,self.c))
    def __eq__(self, __o: object) -> bool:
        return self.r == __o.r and self.c == __o.c
        

class Sensor:

    def __init__(self, sx, sy, bx, by, orig=None):
        self.closest_beacon = Point(by, bx)
        self.sensor = Point(sy, sx)
        self.orig = orig
        self.distance = Sensor.manhattan_distance(self.closest_beacon, self.sensor)
        self.min_col = min([self.closest_beacon.c, self.sensor.c])
        self.max_col = max([self.closest_beacon.c, self.sensor.c])
        self.min_row = min([self.closest_beacon.r, self.sensor.r])
        self.max_row = max([self.closest_beacon.r, self.sensor.r])


    @staticmethod
    def manhattan_distance(a,b):
        return abs(a.r - b.r) + abs(a.c - b.c)

    def covers_point(self, pt):
        """returns True if the pt is within the sensors covered region, meaning that there would
        not be a beacon at that point since that point is closer to the sensor than it's closest beacon
        Args:
            pt (_type_): _description_
        """
        pt_distance = Sensor.manhattan_distance(self.sensor, pt)
        return pt_distance <= self.distance

    def __str__(self):
        return f"orig: {self.orig}\nsensor row: {self.sensor.r}, col: {self.sensor.c}; beacon row: {self.closest_beacon.r}, col: {self.closest_beacon.c}\n"

def read_puzzle_input(inp):
    paths = []
    PAT = 'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)'
    for ln in inp:
        ln = ln.strip()
        m = re.match(PAT, ln)
        if m:
            paths.append(Sensor(int(m.group(1)),int(m.group(2)),int(m.group(3)),int(m.group(4)),orig=ln))
        else:
            print(f"error: {m.group(0)}")
    return paths

def solve(filename):
    with open(filename, "r") as file:
        sensors = read_puzzle_input(file)

    min_col = inf
    max_col = -inf
    min_row = inf
    max_row = -inf
    beacon_points = set()
    for s in sensors:
        min_col = min([min_col, s.min_col])
        max_col = max([max_col, s.max_col])
        min_row = min([min_row, s.min_row])
        max_row = max([max_row, s.max_row])
        beacon_points.add(s.closest_beacon)


    points_covered = []
    row = 2000000
    w = max_col - min_col
    h = max_row - min_row
    border = w + h

    print(f"from: {min_col-border} to: {max_col+border}, range: {abs((min_col-border) - (max_col+border))}")
    print(f"number of sensors: {len(sensors)}")
    for c in range(min_col-border, max_col+border):
        if Point(row,c) in beacon_points:
            continue
        for s in sensors:
            if s.covers_point(Point(row,c)):
                points_covered.append(Point(row,c))
                break

    print(len(points_covered))

if __name__ == '__main__':

    filename = "15/p1_input.txt"
    solve(filename)
