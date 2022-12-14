from dataclasses import dataclass
import re

HOME='home'
UP='up'
DOWN='down'
LIST='list'

class CmdTrace:
    def __init__(self, cmd, arg=None):
        self.command = cmd
        self.argument = arg
        self.output = list()

    def append_result(self, out):
        self.output.append(out)

class CmdOutput:
    def __init__(self, name, is_dir):
        self.name = name
        self.is_dir = is_dir
        self.size = 0

    def set_size(self, sz):
        self.size = int(sz)

class Node:
    def __init__(self, name='/', is_dir=False, size=0, parent=None):
        self.name = name
        self.is_dir = is_dir
        self.size = size
        self.children = list()
        self.parent = parent
    def go_up(self):
        return self.parent
    def go_down(self, d):
        for c in self.children:
            if c.name == d:
                return c
        return self
    def calc_dir_sizes(self):
        if not self.is_dir:
            raise Exception("not a directory!")
        sum_sizes = 0
        for c in self.children:
            if c.is_dir:
                s = c.calc_dir_sizes()
                sum_sizes += s
            else:
                sum_sizes += c.size
        self.size = sum_sizes
        return sum_sizes
    
    def find_dirs(self):
        dirs = []
        for c in self.children:
            if c.is_dir:
                dirs.append(c)
                dirs = dirs + c.find_dirs()
        return dirs
        
def parse_output(ln):
    PAT_DIR = "dir (.+)"
    PAT_FILE = "(\d+) (.+)"
    m = re.match(PAT_DIR, ln)
    if m:
        o = CmdOutput(m.group(1), True)
    else:
        m = re.match(PAT_FILE, ln)
        if m:
            o = CmdOutput(m.group(2), False)
            o.set_size(m.group(1))
    return o

def parse_command(ln):
    PAT_CD_ROOT = "cd /"
    PAT_CD_UP = "cd \.\."
    PAT_CD_DOWN = "cd (.*)"
    PAT_LS = "ls"
    ln = ln[1:].strip() # advance past the prompt
    if re.match(PAT_CD_ROOT, ln):
        return CmdTrace(HOME)
    elif re.match(PAT_CD_UP, ln):
        return CmdTrace(UP)
    elif re.match(PAT_CD_DOWN, ln):
        m = re.match(PAT_CD_DOWN, ln)
        return CmdTrace(DOWN, m.group(1))
    elif re.match(PAT_LS, ln):
        return CmdTrace(LIST)
    return CmdTrace('ERROR')

def parse_commands(inp):
    cmds = []
    curr_cmd = None
    for ln in inp:
        if ln[0] == '$':
            if curr_cmd:
                cmds.append(curr_cmd)
            curr_cmd = parse_command(ln.strip())
        else:
            curr_cmd.append_result(parse_output(ln.strip())) 
    cmds.append(curr_cmd)
    return cmds

def derive_file_system_from_cmds(cmds):
    root = Node()
    curr_dir = None
    for cmd in cmds:
        if cmd.command == HOME:
            curr_dir = root
        elif cmd.command == UP:
            curr_dir = curr_dir.go_up()
        elif cmd.command == DOWN:
            curr_dir = curr_dir.go_down(cmd.argument)
        elif cmd.command == LIST:
            dir_list = cmd.output
            for d in dir_list:
                child = Node(d.name, d.is_dir, d.size, curr_dir)
                curr_dir.children.append(child)
    return root

def read_puzzle_input(inp):
    return parse_commands(inp)

DISK_SIZE = 70000000
NEED_THIS_MUCH_SPACE = 30000000

def solve(filename):
    with open(filename, "r") as file:
        commands = read_puzzle_input(file)
        file_sys = derive_file_system_from_cmds(commands)
        file_sys.calc_dir_sizes()
        print("total size: " + str(file_sys.size))
        disk_free = DISK_SIZE - file_sys.size
        print("disk free: " + str(disk_free))
        need_to_free = NEED_THIS_MUCH_SPACE - disk_free
        print("need to free up: " + str(need_to_free))
        dirs = file_sys.find_dirs()
        # filter for only dirs that are larger than what we need
        # and then sort it so we can find the smallest
        possible_dirs = sorted([d.size for d in dirs if d.size > need_to_free])
        print("delete this: " + str(possible_dirs[0]))

if __name__ == '__main__':

    filename = "07/p1_input.txt"
    solve(filename)

