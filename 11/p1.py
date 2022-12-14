from dataclasses import dataclass
import re
import numpy as np
from collections import deque

class Game:
    def __init__(self):
        self.monkeys = []
        self.monkeys_index = {}

    def add_monkey(self, m):
        self.monkeys.append(m)
        self.monkeys_index[m.id] = m

    def do_n_rounds(game_self, n):
        for i in range(0,n):
            for m in game_self.monkeys:
                m.play(game_self)

    def give_worry_to_monkey(self, worry, monkey):
        m = self.monkeys_index[monkey]
        m.enq_item(worry)
    
    def __str__(self):
        s = ""
        for m in self.monkeys:
            items = [x for x in m.items]
            s = s + f"monkey: {m.id}: {items}, inspected: {m.num_times_inspected}\n"
        return s

class Monkey:
    
    def __init__(self, id):
        self.id = id
        self.items = []
        self.operation_str = ""
        self.operation = None
        self.divisible_by = 0
        self.if_true = -1
        self.if_false = -2
        self.num_times_inspected = 0

    def play(self, game):
        while self.items:
            item = self.items.popleft()
            self.execute(item, game)

    def execute(self, wory, game):
        self.num_times_inspected += 1
        new_worry = self.operation(wory)
        updated_worry = int(new_worry/3)
        if updated_worry % self.divisible_by == 0:
            game.give_worry_to_monkey(updated_worry, self.if_true)
        else:
            game.give_worry_to_monkey(updated_worry, self.if_false)

    def add_str_operation(self, str_op):
        """accepts a string operation and uses that info to prime a lambda
        function that implements the desired operation
        """
        pass
        op_parts = str_op.split()
        op_parts = [op.strip() for op in op_parts]
        if op_parts[1] == '+':
            op = lambda x,y: x + y
        else:
            op = lambda x,y: x * y

        first_old = False
        second_old = False

        if op_parts[0] == 'old':
            first_old = True
        else:
            operand = int(op_parts[0])

        if op_parts[2] == 'old':
            second_old = True
        else:
            operand = int(op_parts[2])

        if first_old and second_old:
            fn = lambda old: op(old,old)
        else:
            fn = lambda old: op(operand,old)
        self.operation = fn


    def add_str_items(self, lst_items):
        self.items = deque([int(it.strip()) for it in lst_items])
    
    def deq_item(self):
        return self.items.popleft()

    def enq_item(self,itm):
        self.items.append(int(itm))

    def __str__(self):
        op = self.operation if self.operation else self.operation_str
        div = f"{self.divisible_by}" if self.divisible_by is not None else "Nothing"
        tr = self.if_true
        fa = self.if_false
        s = f"Monkey: {self.id}, items: {self.items}, op: {op}, div: {div}, true: {tr}, false: {fa}"
        return s


def parse_monkey(inp):
    MONKEY_PAT = "Monkey (.+):"
    ITEMS_PAT = "Starting items: (.*)"
    OP_PAT = "Operation: new = (.*)"
    TEST_PAT = "Test: divisible by (\d+)"
    TRUE_PAT = "If true: throw to monkey (\d+)"
    FALSE_PAT = "If false: throw to monkey (\d+)"

    for ln in inp:
        ln = ln.strip()
        if ln == "":
            yield monkey
            continue
        m = re.match(MONKEY_PAT, ln)
        if m:
            monkey = Monkey(int(m.group(1)))
            continue
        m = re.match(ITEMS_PAT, ln)
        if m:
            monkey.add_str_items( m.group(1).split(',') )
            continue
        m = re.match(OP_PAT, ln)
        if m:
            monkey.add_str_operation( m.group(1) )
            continue
        m = re.match(TEST_PAT, ln)
        if m:
            monkey.divisible_by = int(m.group(1))
            continue
        m = re.match(TRUE_PAT, ln)
        if m:
            monkey.if_true = int(m.group(1))
            continue
        m = re.match(FALSE_PAT, ln)
        if m:
            monkey.if_false = int(m.group(1))
            continue
    yield monkey

def read_puzzle_input(inp):
    game = Game()
    for monkey in parse_monkey(inp):
        print("got monkey----------------------")
        print(monkey)
        game.add_monkey(monkey)
    return game

def solve(filename):
    with open(filename, "r") as file:
        game = read_puzzle_input(file)
        print(f"answer: {0}")
        game.do_n_rounds(20)
        print(game)
        inspected = sorted([m.num_times_inspected for m in game.monkeys], reverse=True)
        total = inspected[0] * inspected[1]
        print(f"monkey business: {total}")

if __name__ == '__main__':

    filename = "11/p1_input.txt"
    solve(filename)
