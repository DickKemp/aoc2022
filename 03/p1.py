from dataclasses import dataclass

@dataclass

class Rugsack:
    left: str
    right: str

def find_mistake_priority(l,r):
    return get_priority( find_mistake(l, r) )

def find_mistake(l, r):
    for c in list(l):
        if c in r:
            return c
    return '_'

def get_priority(x):
    priorities = '_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return priorities.index(x)

filename = "03/test_p1_input.txt"
filename = "03/p1_input.txt"

def consume_rugsacks_input(inp):
    rs = []
    for line in inp:
        line = line.strip()
        ln = len(line)
        r = Rugsack(line[0:int(ln/2)], line[int(ln/2):ln])
        rs.append(r)
    return rs

with open(filename, "r") as file:
    
    rs = consume_rugsacks_input(file)
    all_priorities = [find_mistake_priority(r.left, r.right) for r in rs]    
    print(sum(all_priorities))
    