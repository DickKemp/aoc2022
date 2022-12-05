from dataclasses import dataclass

@dataclass

class A:
    low: int
    hi: int

filename = "04/test_p1_input.txt"
filename = "04/p1_input.txt"

def contains(a,b):
    return a.low <= b.low and a.hi >= b.hi 

def parse_line(ln):
    # takes as input "2-3,4-5" and returns (A(2,3),A(4,5))
    ln = ln.strip()
    xy = ln.split(',')
    x = xy[0].split('-')
    y = xy[1].split('-')
    return tuple([A(int(x[0]),int(x[1])), A(int(y[0]),int(y[1]))])
    
def read_puzzle_input(inp):
    # input is a sequence of lines of the form: N-N,N-N
    # where N is an int
    es = []
    for line in inp:
        e = parse_line(line)        
        es.append(e)
    return es

with open(filename, "r") as file:
    rs = read_puzzle_input(file)
    print(rs)
    c = [(contains(x[0],x[1]) or (contains(x[1],x[0]))) for x in rs]
    
    print(sum(c))
    