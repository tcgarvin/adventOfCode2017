import fileinput
import sys
from collections import deque

ORIGINAL_LINE = "abcdefghijklmnop"

def spin(line, amount):
    line.rotate(amount)


def exchange(line, x, y):
    temp = line[x]
    line[x] = line[y]
    line[y] = temp


def index_of(line, a):
    for i, x in enumerate(line):
        if a == x:
            return i
            

def partner(line, a, b):
    x = index_of(line, a)
    y = index_of(line, b)
    exchange(line, x, y)


def apply_command(line, command):
    if command[0] is "s":
        spin(line, command[1])

    elif command[0] is "x":
        exchange(line, command[1], command[2])

    elif command[0] is "p":
        partner(line, command[1], command[2])

    else:
        raise Exception("Invalid command %s" % (command,))


def dance(line, commands):
    for command in commands:
        apply_command(line, command)

# defines how many spaces each spot moves
def derive_position_mapping(commands):
    line = deque(ORIGINAL_LINE)
    dance(line, filter(lambda c: c[0] is not "p", commands))

    position_mapping = []
    for position, program in enumerate(ORIGINAL_LINE):
        new_position = index_of(line, program)
        position_mapping.append(new_position - position)

    print position_mapping

    return position_mapping


def apply_position_mapping(line, position_mapping, target):
    for position, program in enumerate(line):
        difference = position_mapping[position]
        target[position + difference] = program

    return target
    

# defines who replaces each program - should be totally orthoginal to the
# position_mapping
def derive_partner_swapping(commands):
    line = deque(ORIGINAL_LINE)
    dance(line, filter(lambda c: c[0] is "p", commands))

    partner_swapping = {}
    for i, program in enumerate(ORIGINAL_LINE):
        partner_swapping[program] = line[i]

    print partner_swapping

    return partner_swapping


def apply_partner_swapping(line, partner_swapping):
    for i, program in enumerate(line):
        line[i] = partner_swapping[program]
        

def parse_commands(string_input):
    command_strings = string_input.next().strip().split(",")

    commands = []
    for command in command_strings:
        if command.startswith("s"):
            amount = int(command[1:])
            commands.append(("s", amount))

        elif command.startswith("x"):
            sx, sy = command[1:].split("/")
            commands.append(("x", int(sx), int(sy)))

        elif command.startswith("p"):
            a, b = command[1:].split("/")
            commands.append(("p", a, b))

    return commands

def line_str(line):
    return "".join(line)

def print_line(line):
    print line_str(line)
        

    
if __name__ == "__main__":
    commands = parse_commands(fileinput.input())
    position_mapping = derive_position_mapping(commands)
    partner_swapping = derive_partner_swapping(commands)

    line = deque(ORIGINAL_LINE)
    dance(line, commands)
    line2 = deque(ORIGINAL_LINE)
    target = [None for x in line2]
    line2 = apply_position_mapping(line2, position_mapping, target)
    line2 = target
    apply_partner_swapping(line2, partner_swapping)

    print "Answer 1"
    print_line(line)


    seen = set((ORIGINAL_LINE, line_str(line)))
    target = [None for x in line2] # Pre-allocated to help speed maybe
    for x in xrange(100000000000- 1):
        apply_position_mapping(line2, position_mapping, target)

        temp = line2
        line2 = target
        target = temp

        apply_partner_swapping(line2, partner_swapping)

        dance(line, commands)

        out = line_str(line)
        if out in seen:
            print x, line_str(line), len(seen)

        seen.add(out)

    print "Answer 2"
    print_line(line2)
    
    
