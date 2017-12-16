#!/usr/bin/python

import fileinput

depth = 0
state = "group"
total = 0
garbage = 0
for c in fileinput.input().readline():
    if state is "group":
        if c is "{":
            depth += 1

        elif c is "}":
            total += depth
            depth -= 1

        elif c is "<":
            state = "garbage"


    elif state is "garbage":
        if c is ">":
            state = "group"

        elif c is "!":
            state = "ignore"

        else:
            garbage += 1

    elif state is "ignore":
        state = "garbage"

print total
print garbage


    
    
