from dataclasses import dataclass
import re
import numpy as np
from collections import deque
from bfs import shortest_path

# returns tuple with value & position of the neighboring cell in the grid
def up(g, r, c):
    return (g[r-1,c] if r>0 else None, tuple([r-1,c])) 
def down(g, r, c):
    return (g[r+1,c] if r<g.shape[0]-1 else None, tuple([r+1,c])) 
def left(g, r, c):
    return (g[r,c-1] if c>0 else None, tuple([r,c-1])) 
def right(g, r, c):
    return (g[r,c+1] if c<g.shape[1]-1 else None, tuple([r,c+1])) 

def find_all(grid, cs):
    (height,width) = grid.shape
    res = []
    for h in range(height):
        for w in range(width):
            if grid[h,w] in cs:
                res.append(tuple([h,w]))
    return res

def build_graph(grid):
    graph = {}
    start = None
    end = None
    (height,width) = grid.shape

    for h in range(height):
        for w in range(width):
            if grid[h,w] == 'S':
                start = tuple([h,w])
                grid[h,w] = 'a'
                continue
            if grid[h,w] == 'E':
                end = tuple([h,w])
                grid[h,w] = 'z'
                continue

    for h in range(height):
        for w in range(width):
            node_id = tuple([h,w])
            node_val = grid[h,w]
            reachable = set()
            for (val,id) in [up(grid, h, w), down(grid, h, w), left(grid, h, w), right(grid, h, w)]:
                if val:
                    if can_reach(node_val, val):
                        reachable.add(id)
            graph[node_id] = reachable

    return graph, start, end

def can_reach(f,t):
    return (ord(t) - ord(f)) < 2
        
def read_puzzle_input(inp):
    grid = []
    for ln in inp:
        ln = ln.strip()
        grid.append(list(ln))
    return np.array(grid)

def solve(filename):
    with open(filename, "r") as file:
        grid = read_puzzle_input(file)
        graph, _, end = build_graph(grid)
        all_a = find_all(grid, ['a','S'])
        paths = [shortest_path(graph, a, end) for a in all_a]
        path_lens = [len(p) for p in paths]
        non_zero_paths = filter((lambda x: x!=0), path_lens)
        print(f"min path with length: {min(non_zero_paths)-1}")

if __name__ == '__main__':

    filename = "12/p1_input.txt"
    solve(filename)
