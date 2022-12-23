from dataclasses import dataclass
import re
import numpy as np
from collections import deque
from math import inf
import networkx as nx
import pprint as pp
import numpy as np
import copy

class Operation:
    def __init__(self, map, op, arg1, arg2=None):
        self.map = map
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        if op == '=':
            self.type = 'value'
        elif op in ['+', '-', '/', '*']:
            self.type = 'calc'
        elif op == '==':
            self.type = 'equivalent'
        elif op == '?':
            self.type = 'placeholder'
        else:
            raise Exception(f'unknown operator: {op}')
        self.set_dependent_formulas()

    def calc(self):
        if self.op == '=':
            return int(self.arg1)
        elif self.op == '?':
            raise Exception("cannot calculate a placeholder")
        elif self.op == '==':
            return self.solve_for_placeholder()
        else: 
            opr1 = self.map[self.arg1]
            opr2 = self.map[self.arg2]
            return self.apply_op(self.op, opr1.calc(), opr2.calc())

    def solve_for_placeholder(self):
        opr1 = self.map[self.arg1]
        opr2 = self.map[self.arg2]

        opr_with_placeholder = None
        opr_with_value = None
        
        # find which of the two operands has the placeholder,
        # then the other operand must have a value
        if opr1.check_if_op_has_placeholder():
            opr_with_placeholder = opr1
            opr_with_value = opr2
        else:
            opr_with_placeholder = opr2
            opr_with_value = opr1
        
        # get the calculated value from operanPd without the placeholder, 
        # and then push that value into the other operand that has the placeholder.
        # What this will do is push down the value to force the placeholder to assume the
        # correct value

        calc_result = opr_with_value.calc()
        place_holder_value = opr_with_placeholder.push_down_result(calc_result)
        return place_holder_value

    def apply_op(self, op, arg1, arg2):
        if op == '+':
            return int(arg1) + int(arg2)
        elif op == '-':
            return int(arg1) - int(arg2)
        elif op == '*':
            return int(arg1) * int(arg2)
        elif op == '/':
            return int(arg1) / int(arg2)            
        raise Exception("should not get here")

    def push_down_result(self, val_from_above):
        if self.type == 'placeholder':
            return val_from_above
        elif self.type == 'calc':
            left_operand = self.map[self.arg1]
            right_operand = self.map[self.arg2]

            opr_with_placeholder = None
            opr_with_value = None
            
            # find which of the two operands has the placeholder,
            # then the other operand must have a value
            if left_operand.check_if_op_has_placeholder():
                formula_to_use = self._formula_to_calc_left_operand
                opr_with_placeholder = left_operand
                opr_with_value = right_operand
            else:
                formula_to_use = self._formula_to_calc_right_operand
                opr_with_placeholder = right_operand
                opr_with_value = left_operand
            
            # get the calculated value from operand that we know will return a value, 
            # and then apply the modified formula that takes asserted calculated amount, along with
            # the calculated amount from the other operand, in order to compute the value that this
            # operand should have.
            # then push that value into the other operand that has the placeholder.

            other_operand_calc_result = opr_with_value.calc()

            # apply dependent formula using the passed in value & the result from the other operand
            value_to_push_down = formula_to_use(val_from_above, other_operand_calc_result)

            # then take the calculated result and push it down
            return opr_with_placeholder.push_down_result(value_to_push_down)

    def check_if_op_has_placeholder(self):
        # if you try to calculate an operation that contains a placeholder then
        # it will thrown an exception
        try:
            self.calc()
            return False
        except:
            return True

    def set_dependent_formulas(self):
        if self.type == 'equivalent':
            self._formula_to_calc_left_operand = lambda this, other : other
            self._formula_to_calc_right_operand = lambda this, other : other

        if self.type == 'calc':
            # this = opr1 + opr2
            #   opr1 = this - opr2
            #   opr2 = this - opr1 
            if self.op == '+':
                self._formula_to_calc_left_operand = lambda this, other : self.apply_op("-", this, other)
                self._formula_to_calc_right_operand = lambda this, other : self.apply_op("-", this, other)
            
            # this = opr1 * opr2
            #   opr1 = this / opr2
            #   opr2 = this / opr1 
            if self.op == '*':
                self._formula_to_calc_left_operand = lambda this, other : self.apply_op("/", this, other)
                self._formula_to_calc_right_operand = lambda this, other : self.apply_op("/", this, other)

            # this = opr1 - opr2
            #   opr1 = this + opr2
            #   opr2 = opr1 - this
            if self.op == '-':
                self._formula_to_calc_left_operand = lambda this, other : self.apply_op("+", this, other)
                self._formula_to_calc_right_operand = lambda this, other : self.apply_op("-", other, this)

            # this = opr1 / opr2
            #   opr1 = this * opr2
            #   opr2 = opr1 / this
            if self.op == '/':
                self._formula_to_calc_left_operand = lambda this, other : self.apply_op("*", this, other)
                self._formula_to_calc_right_operand = lambda this, other : self.apply_op("/", other, this)


def read_puzzle_input(inp):
    """ input looks like this:
        pngc: vdvn + qtgs
        hmtl: 3
    """
    PAT = "(.+):(.+)([+-/*])(.+)"
    PAT2 = "(.+): (\d+)"
    operations_map = {}
    for ln in inp:
        ln = ln.strip()
        m = re.match(PAT, ln)
        if m:
            variable = m.group(1).strip()
            operand1 = m.group(2).strip()
            operation = m.group(3).strip()
            operand2 = m.group(4).strip()
            if variable == 'root':
                operation = '=='
            operations_map[variable] = Operation(operations_map, operation, operand1, operand2)
        else:
            m = re.match(PAT2, ln)
            if m:
                variable = m.group(1).strip()
                value = m.group(2).strip()
                operation = '='
                if variable == 'humn':
                    operation = '?'
                operations_map[variable] = Operation(operations_map, operation, value)
            else:
                print(f"cannot parse: {ln}")
    return operations_map

def solve(filename):
    with open(filename, "r") as file:
        ops = read_puzzle_input(file)

    root = ops["root"]
    answer = root.calc()
    print(f"humm: {answer}")

if __name__ == '__main__':

    filename = "21/p1_input.txt"
    solve(filename)
