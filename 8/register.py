#!/usr/bin/python

import fileinput
from collections import defaultdict


ops = {
    "inc": lambda r, x: r + x,
    "dec": lambda r, x: r - x
}


conditions = {
    "!=": lambda r, x: r != x,
    "==": lambda r, x: r == x,
    ">":  lambda r, x: r > x,
    ">=": lambda r, x: r >= x,
    "<=": lambda r, x: r <= x,
    "<":  lambda r, x: r < x,
}


class Instruction():
    def __init__(self, register_name, op, op_x, cond_reg_name, cond_op, cond_x):
        self.register_name = register_name
        self.op = ops[op]
        self.op_x = op_x
        self.cond_reg_name = cond_reg_name
        self.cond_op = conditions[cond_op]
        self.cond_x = cond_x
        
    def execute(self, registers):

        register_value = registers[self.register_name]
        cond_reg_value = registers[self.cond_reg_name]

        if self.cond_op(cond_reg_value, self.cond_x):
            registers[self.register_name] = self.op(register_value, self.op_x)


def parse_input(lines):
    return map(parse_line, lines)


def parse_line(line):
    tokens = line.split(" ")
    return Instruction(
        tokens[0],
        tokens[1],
        int(tokens[2]),
        tokens[4],
        tokens[5],
        int(tokens[6])
    )
        
    

if __name__ == "__main__":

    instructions = parse_input(fileinput.input())

    registers = defaultdict(int)
    largest_value = 0
    for instruction in instructions:
        instruction.execute(registers)
        largest_value = max(largest_value, max(registers.itervalues()))

    print max(registers.itervalues())
    print largest_value
