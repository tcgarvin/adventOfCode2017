PUZZLE_INPUT = 355

def build_buffer(last_value, skips):
    result = [0]
    curs = 0
    for to_insert in xrange(1, last_value + 1):
        curs = ((curs + skips) % len(result)) + 1
        result.insert(curs, to_insert)

    return result


def build_second_element_of_buffer(last_value, skips):
    size = 1
    second_el = None
    curs = 0
    for to_insert in xrange(1, last_value + 1):
        curs = ((curs + skips) % size) + 1
        if (curs == 1):
            second_el = to_insert

        size += 1

    return second_el
        

if __name__ == "__main__":
    circular_buffer = build_buffer(2017, PUZZLE_INPUT)

    print "Answer 1"
    print circular_buffer[(circular_buffer.index(2017) + 1) % len(circular_buffer)]


    circular2 = build_second_element_of_buffer(50000000, PUZZLE_INPUT)

    print "Answer 2"
    print circular2
        
        


