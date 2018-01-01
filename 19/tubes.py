import fileinput
from collections import defaultdict

def get_starting_coords(grid):
    return (0, grid[0].index("|"))


paths = set("|-ABCDEFGHIJKLMNOPQRSTUVWXYZ")
def is_path(char):
    return char in paths


def is_turn(char):
    return char is "+"


checkpoints = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
def is_checkpoint(char):
    return char in checkpoints


right_hand = ["DOWN", "RIGHT", "UP", "LEFT"]
def take_turn(grid, y, x, movement):
    i_of_path_back = right_hand.index(movement) + 2

    for candidate_i_forward in xrange(i_of_path_back + 1, i_of_path_back + 4):
        candidate_movement = right_hand[candidate_i_forward % len(right_hand)]
        next_y, next_x = move(y, x, candidate_movement)
        # print next_x, next_y, grid[next_y][next_x]
        if is_path(grid[next_y][next_x]):
            return candidate_movement

    print_detail(grid, y-5, y+5, x-5, x+5)
    print x, y, movement
    raise Exception("No path from turn found")
    

def move(y, x, movement):
    next_y = y
    next_x = x

    if movement == "DOWN":
        next_y += 1
    elif movement == "UP":
        next_y -= 1
    elif movement == "LEFT":
        next_x -= 1
    elif movement == "RIGHT":
        next_x += 1

    return next_y, next_x


def traverse_route(grid):
    # Couple of hacks.  Will treat `|` and `-` and all letters equivalently, as
    # all `+` seem to never be tangential to other paths. 

    steps = 0
    seen = []
    loop_detection = defaultdict(int)
    y, x = get_starting_coords(grid)
    movement = "DOWN"

    terminated = False
    while not terminated:
        loop_detection[(y,x)] += 1
        if loop_detection[(y,x)] > 2:
            print_detail(grid, y-5, y+5, x-5, x+5)
            print x,y,movement
            raise Exception("Infinite loop detected")

        current_char = grid[y][x]

        if is_checkpoint(current_char):
            seen.append(current_char)

        if is_turn(current_char):
            #print_detail(grid, y-5, y+5, x-5, x+5)
            #print x,y,movement
            movement = take_turn(grid, y, x, movement)
        elif not is_path(current_char):
            terminated = True
            steps -= 1

        y, x = move(y, x, movement)
        steps += 1

    return seen, steps


def parse_grid(lines):
    return list(map(list, map(lambda l: l.strip("\n"), lines)))


def print_detail(grid, y0 = None, y1 = None, x0 = None, x1 = None):
    y0 = y0 if y0 is not None and y0 >= 0 else 0
    y1 = y1 if y1 is not None and y1 < len(grid) else len(grid)
    x0 = x0 if x0 is not None and x0 >= 0 else 0
    x1 = x1 if x1 is not None and x1 < len(grid[0]) else len(grid[0])

    for y in xrange(y0, y1):
        print "".join(grid[y][x0:x1])


if __name__ == "__main__":
    grid = parse_grid(fileinput.input())

    checkpoints, steps = traverse_route(grid)

    print "Answer 1"
    print "".join(checkpoints)
    print ""
    print "Answer 2"
    print steps
