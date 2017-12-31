import fileinput
from itertools import imap, izip, islice, ifilter

def generator(starting_value, factor):
    previous_value = starting_value
    while True:
        value = previous_value * factor % 2147483647
        previous_value = value
        yield value


def picky_generator(starting_value, factor, divisor):
    core = generator(starting_value, factor)
    return ifilter(lambda x: x % divisor == 0, core)


def lower_16_matches(a,b):
    matches = a & 2**16-1 == b & 2**16-1
    #if matches:
    #    print a, "\t", hex(a), "\t", b, "\t", hex(b), "\t", hex(a & 2**16-1), "\t", hex( b & 2**16-1)

    return matches


def judge(gen_a, gen_b, iterations):
    pairs = izip(gen_a, gen_b)
    first_i_pairs = islice(pairs, iterations)
    return sum(imap(lambda pair: lower_16_matches(*pair), first_i_pairs))
    

def parse_initial_value(line):
    return int(line.split()[-1])


def parse_initial_values(lines):
    gen_a_initial = parse_initial_value(next(lines))
    gen_b_initial = parse_initial_value(next(lines))
    return gen_a_initial, gen_b_initial


if __name__ == "__main__":
    gen_a_initial, gen_b_initial = parse_initial_values(fileinput.input())

    gen_a = generator(gen_a_initial, 16807)
    gen_b = generator(gen_b_initial, 48271)

    #for x in xrange(5):
    #    print next(gen_a), next(gen_b)

    
    print "Answer 1"
    print judge(gen_a, gen_b, 40000000)


    gen_a_picky = picky_generator(gen_a_initial, 16807, 4)
    gen_b_picky = picky_generator(gen_b_initial, 48271, 8)
    
    #for x in xrange(5):
    #    a = next(gen_a_picky)
    #    b = next(gen_b_picky)
    #    print a, b, lower_16_matches(a,b)
    

    print "Answer 2"
    print judge(gen_a_picky, gen_b_picky, 5000000)
    
