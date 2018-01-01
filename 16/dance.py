import fileinput
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
    line = deque(ORIGINAL_LINE)
    dance(line, commands)

    print "Answer 1"
    print_line(line)


    seen = set((ORIGINAL_LINE,))
    lookup = [ORIGINAL_LINE]
    line2 = deque(ORIGINAL_LINE)
    generating = True
    x = 1
    while generating:
        dance(line2, commands)
        result = line_str(line2)
        if result in seen:
            generating = False
        seen.add(result)
        lookup.append(result)
        x += 1


    print "Answer 2"
    print_line(lookup[1000000000 % len(lookup)])
