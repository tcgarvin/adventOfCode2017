#!/usr/bin/python

# I'm disappointed at the speed of jumps.hs, and wonder if I'm missing
# something.  This (much smaller) python also solves the problem, and uses
# mutable data structures and a loop instead of immutable and recursion.

# This code is way faster and easier to read than the .hs code.  Guess I
# need to learn more Haskell

import fileinput

jumps = map(int, fileinput.input())

cursor = 0
iterations = 0
while cursor >= 0 and cursor < len(jumps):
    iterations += 1
    jump = jumps[cursor]
    jumps[cursor] += (-1 if jump >= 3 else 1)
    cursor += jump

print iterations
	
