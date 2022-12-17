from dataclasses import dataclass
import re
import numpy as np
from collections import deque
from math import inf
import shapely.geometry as geo
import shapely.set_operations as geo_set
from shapely import Point as GeoPoint
import shapely.predicates as pred

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
        
        dist = self.distance
        x0,y0 = self.sensor.c, self.sensor.r
        l0 = (x0-dist, y0)
        u0 = (x0, y0-dist)
        r0 = (x0+dist, y0)
        d0 = (x0, y0+dist)
        self.polygon = geo.Polygon((l0, u0, r0, d0, l0))


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

    beacon_points = set()
    all_polygons = None
    all_poly = []
    for s in sensors:
        beacon_points.add(s.closest_beacon)
        all_poly.append(s.polygon)

    all_polygons = geo_set.union_all(all_poly)

    R1 = geo.box(0,0,4000000,4000000)
    
    d3 = geo_set.difference(R1, all_polygons)

    signal = d3.centroid.x * 4000000 + d3.centroid.y
    print(f"signal: {signal}")

if __name__ == '__main__':

    filename = "15/p1_input.txt"
    solve(filename)
