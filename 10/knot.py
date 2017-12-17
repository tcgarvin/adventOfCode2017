import fileinput

# Modulus operators.
def ringset(l, i, x):
    l[i % len(l)] = x


def ringslice(l, start, end):
    length = len(l)

    result = None
    if start / length < end / length:
        result = l[start % length:] + l[:end % length]

    else:
        result = l[start % length : end % length]

    #print "slice:", l, start, end
    #print "slice:", result

    return result


def parse_input(lines):
    return map(int, lines.readline().split(","))


# In-place modifiation
def knot(source, lengths):
    curs = 0
    skip = 0
    for length in lengths:
        print source
        twist(source, length, curs)
        curs += length + skip
        skip += 1

    return source


# In-place
def twist(source, length, curs):
    replacement = reversed(ringslice(source, curs, curs + length))
    for i, x in enumerate(replacement):
        ringset(source, curs + i, x)

        
if __name__ == "__main__":
    lengths = parse_input(fileinput.input())
    print lengths
    data = range(256)
    knot(data, lengths)
    print data
    print data[0] * data[1]
