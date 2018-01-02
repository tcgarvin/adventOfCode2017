import fileinput

from math import sqrt
from itertools import izip, chain

# Here's another example that would be a lot easier with pandas, but hacking it
# with the standard library is fun?

# All grids are squares of Trues and Falses
class Grid(object):
    
    @classmethod
    def stitch(cls, squares):
        #print "Stitching:"
        #for square in squares:
        #    print square
        #    print ""

        square_size = squares[0].size
        squares_per_row = int(sqrt(len(squares)))
        rows_of_squares = squares_per_row

        element_list = []
        for row_of_squares in xrange(0, rows_of_squares):
            for r in xrange(0, square_size):
                for square_i in xrange(row_of_squares * squares_per_row, (row_of_squares + 1) * squares_per_row):
                    element_list.extend(squares[square_i].grid[r])

        result = Grid(element_list)

        #print "Stitch result"
        #print result
        #print ""
        return result


    @classmethod
    def from_element_string(cls, element_string):
        cleaned = element_string.strip().replace("/", "")
        return Grid([True if l is "#" else False for l in cleaned])


    def __init__(self, elements):
        self.size = int(sqrt(len(elements)))
        self.fill = sum(elements) # Sum of bools is number of Trues
        self.grid = [elements[x * self.size : (x+1) * self.size] for x in xrange(self.size)]


    def _scanner(self, mapper):
        for i in xrange(self.size**2):
            yield mapper(i)

    def get_basic_scan_plan(self):
        s = self.size
        return self._scanner(lambda i: (i / s, i % s))


    def get_scan_plans(self):
        # Though it's not true for 2x2 squares, we'll treat every square as
        # having 8 possible flip/rotate combinations.  A little matrix work
        # would help here too, but I will demur

        s = self.size
        yield self._scanner(lambda i: (i/s          , i%s          ))
        yield self._scanner(lambda i: (s - (i/s) - 1, i%s          ))
        yield self._scanner(lambda i: (i/s           ,s - (i%s) - 1))
        yield self._scanner(lambda i: (s - (i/s) - 1 ,s - (i%s) - 1))
        yield self._scanner(lambda i: (i%s          , i/s          ))
        yield self._scanner(lambda i: (s - (i%s) - 1, i/s          ))
        yield self._scanner(lambda i: (i%s           ,s - (i/s) - 1))
        yield self._scanner(lambda i: (s - (i%s) - 1 ,s - (i/s) - 1))


    def matches(self, other):
        if self.size != other.size:
            return False

        if self.size is 3 and self.grid[1][1] is not other.grid[1][1]:
            return False

        if self.fill != other.fill:
            return False

        for scan_plan in self.get_scan_plans():
            seen_differences = False
            for mycoord, othercoord in izip(self.get_basic_scan_plan(), scan_plan):
                x,y = mycoord
                i,j = othercoord

                if self.grid[x][y] != other.grid[i][j]:
                    seen_differences = True
                    break

            if not seen_differences:
                return True

        return False


    def break_up(self):
        if self.size % 2 == 0:
            return self._break_up(2)

        elif self.size % 3 == 0:
            return self._break_up(3)

        raise Exception("Unable to break up grid")


    def _break_up(self, desired_size):
        result = []
        for j in xrange(0, self.size, desired_size):
            for i in xrange(0, self.size, desired_size):
                # Generate a SxS grid with origin at i,j
                block = [self.grid[r][i:i+desired_size] for r in xrange(j, j+desired_size)]
                square = Grid(list(chain(*block)))
                result.append(square)

        return result


    def row_string(self, row):
        return "".join(map(lambda b: "#" if b else ".", row))


    def __str__(self):
        return "\n".join((self.row_string(row) for row in self.grid))
    


STARTING_GRID_STRING = ".#./..#/###"
def generate_starting_grid():
    return Grid.from_element_string(STARTING_GRID_STRING)


def enhance_square(square, rules):
    for matcher, enhancement in rules:
        if matcher.matches(square):
            return Grid.from_element_string(enhancement)

    raise Exception("All squares should be matched")


def enhance(grid, rules):
    squares = grid.break_up()
    enhanced_squares = map(lambda sq: enhance_square(sq, rules), squares)
    result = Grid.stitch(enhanced_squares)
    return result


def iterate_enhancement(grid, rules, iterations):
    iteratively_enhanced_grid = grid
    for i in xrange(iterations):
        print i
        print iteratively_enhanced_grid
        print ""
        iteratively_enhanced_grid = enhance(iteratively_enhanced_grid, rules)

    print iterations
    print iteratively_enhanced_grid
    print ""

    return iteratively_enhanced_grid


def parse_enhancement_rule(line):
    matcher, enhancement = line.split("=>")
    matcher = Grid.from_element_string(matcher)
    enhancement = enhancement.strip()
    return (matcher, enhancement)
    

def parse_enhancement_rules(lines):
    return map(parse_enhancement_rule, lines)


def number_of_pixels_on(grid):
    return sum(map(sum, grid.grid))


if __name__ == "__main__":
    enhancement_rules = parse_enhancement_rules(fileinput.input())
    starting_grid = generate_starting_grid()

    result = iterate_enhancement(starting_grid, enhancement_rules, 5)
    print "Answer 1"
    print number_of_pixels_on(result)

    print ""
    starting_grid = generate_starting_grid()
    result2 = iterate_enhancement(starting_grid, enhancement_rules, 18)
    print "Answer 2"
    print number_of_pixels_on(result2)



