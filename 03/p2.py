from dataclasses import dataclass

@dataclass

class Rugsack:
    left: str
    right: str

def find_common_in_group(grouplist):
    com12 = find_common_item(grouplist[0], grouplist[1])
    com123 = find_common_item(com12, grouplist[2])
    return com123

def find_common_item(l, r):
    com = set()
    
    for c in list(l):
        if c in r:
            com.add(c)
    return "".join(list(com))

def get_priority(x):
    priorities = '_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return priorities.index(x)

filename = "03/test_p1_input.txt"
filename = "03/p1_input.txt"

def get_groups(lst):
    ln = len(lst)
    num_groups = int(ln/3)
    for i in range(0,num_groups):
        yield lst[i*3:i*3+3]

def consume_rugsacks_input(inp):
    rs = []
    for line in inp:
        line = line.strip()
        ln = len(line)
        r = Rugsack(line[0:int(ln/2)], line[int(ln/2):ln])
        rs.append(r.left + r.right)
    return rs

with open(filename, "r") as file:
    common = []    
    rs = consume_rugsacks_input(file)
    for group in get_groups(rs):
        com = find_common_in_group(group)
        common.append(com)
    
    all_priorities = [get_priority(c) for c in common]
    print(sum(all_priorities))
        