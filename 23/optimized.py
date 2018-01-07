from math import sqrt

b = 57 * 100 + 100000
c = b + 17000

h = 0
while True:
    f = 1
    for factor in xrange(2, b):
        if b % factor == 0:
            f = 0
            break

    if f == 0:
        h += 1

    if b - c == 0:
        break

    b += 17
    
print h


        
        




