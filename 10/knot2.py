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
    return map(ord, lines.readline().strip())


# In-place modifiation
def knot_inner(source, lengths):
    curs = 0
    skip = 0
    for round_num in xrange(64):
        for length in lengths:
            #print source
            twist(source, length, curs)
            curs += length + skip
            skip += 1

    return source


# In-place
def twist(source, length, curs):
    replacement = reversed(ringslice(source, curs, curs + length))
    for i, x in enumerate(replacement):
        ringset(source, curs + i, x)


def dense(sparse):
    dense = []
    for i in xrange(0,len(sparse),16):
        dense.append(reduce(lambda x,y: x^y, sparse[i:i+16]))
    return dense


def tohex(num):
    # 2-digit hex representation
    s = hex(num)[2:4]
    if len(s) == 1:
        s = "0" + s

    return s


def knot128(input_string):
    lengths = map(ord, input_string) + [17,31,73,47,23]
    data = range(256)
    knot_inner(data, lengths)
    dense_hash = dense(data)
    hex_string = reduce(lambda accum, y: accum + tohex(y), dense_hash, str())
    return hex_string

        
if __name__ == "__main__":
    lengths = parse_input(fileinput.input()) + [17, 31, 73, 47, 23]
    print lengths

    data = range(256)
    knot_inner(data, lengths)

    dense_hash = dense(data)

    hex_string = reduce(lambda accum, y: accum + tohex(y), dense_hash, str())

    print len(hex_string)
    print hex_string
