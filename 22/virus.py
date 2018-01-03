import fileinput

directions = ["UP", "LEFT", "DOWN", "RIGHT"]
def turn(shift, direction):
    return directions[(directions.index(direction) + shift) % len(directions)]
    

def turn_left(direction):
    return turn(1, direction)


def turn_right(direction):
    return turn(-1, direction)


def move(x, y, direction):
    if direction == "UP":
        y -= 1
    elif direction == "DOWN":
        y += 1
    elif direction == "LEFT":
        x -= 1
    elif direction == "RIGHT":
        x += 1

    return (x,y)


def sporifica(grid, center_x, center_y, iterations):
    infected = 0
    cleaned = 0
    x = center_x
    y = center_y
    direction = "UP"
    for i in xrange(iterations):
        #print_grid(grid, x, y)
        #print direction
        #print ""
        if (x,y) in grid:
            direction = turn_right(direction)
            del grid[(x,y)]
            cleaned += 1

        else:
            direction = turn_left(direction)
            grid[(x,y)] = True
            infected += 1

        x,y = move(x, y, direction)

    #print_grid(grid, x, y)
    #print direction
    #print ""

    return infected, cleaned


def parse_grid_line(line):
    return map(lambda c: c is "#", line.strip())


def parse_grid(lines):
    dense_grid = map(parse_grid_line, lines)
    height = len(dense_grid)
    width = len(dense_grid[0])

    grid = {}
    for y, row in enumerate(dense_grid):
        for x, cell in enumerate(row):
            if cell is True:
                grid[(x,y)] = cell
            
    return (grid, height, width)


def print_grid(grid, highlight_x, highlight_y):
    min_x = highlight_x
    max_x = highlight_x
    min_y = highlight_y
    max_y = highlight_y
    for x,y in grid.iterkeys():
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)


    for y in xrange(min_y, max_y+1):
        row = []
        for x in xrange(min_x, max_x+1):
            char = "#" if (x,y) in grid else "."

            if x == highlight_x and y == highlight_y:
                char = "@" if char == "#" else "_"
            row.append(char)

        print "".join(row)

if __name__ == "__main__":
    grid, height, width = parse_grid(fileinput.input())
     

    center_x = height / 2
    center_y = width / 2

    #print grid, center_x, center_y

    infected, cleaned = sporifica(grid, center_x, center_y, 10000)

    print ""
    print "Answer 1"
    print infected
