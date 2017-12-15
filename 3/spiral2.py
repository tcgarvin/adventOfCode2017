import sys

def diff(prev, current):
    px = prev[0]
    py = prev[1]
    cx = current[0]
    cy = current[1]
    return (cx - px, cy - py)


def rotate_diff_left(d):
    dx = d[0]
    dy = d[1]
    return (dy * -1, dx)
    

def straight_ahead(prev, current):
    d = diff(prev, current)
    dx = d[0]
    dy = d[1]
    cx = current[0]
    cy = current[1]
    return (cx + dx, cy + dy)


def left_turn(prev, current):
    d = rotate_diff_left(diff(prev, current))
    dx = d[0]
    dy = d[1]
    cx = current[0]
    cy = current[1]
    return (cx + dx, cy + dy)

    
def spiral():
    # Lazy
    seen = set()

    current = (0,0)
    seen.add(current)
    yield current

    prev = current
    current = (1,0)
    seen.add(current)
    yield current

    while True:
        left = left_turn(prev,current)

        if left in seen:
            straight = straight_ahead(prev,current)
            prev = current
            current = straight

        else:
            prev = current
            current = left

        seen.add(current)
        yield current


SURROUNDING_DIFFS = (
    (1,1),
    (1,0),
    (1,-1),
    (0,1),
    (0,-1),
    (-1,1),
    (-1,0),
    (-1,-1))

def surrounding_cells(coord):
    return map(lambda d: (d[0] + coord[0], d[1] + coord[1]), SURROUNDING_DIFFS)


def sum_of_surrounding(coord, grid):
    return sum(map(lambda c: grid.get(c, 0), surrounding_cells(coord)))
    

def spiral_until(target):
    grid = {}

    for i, coord in enumerate(spiral()):
        if i == 0:
            grid[coord] = 1
            continue

        cell_value = sum_of_surrounding(coord, grid)

        print i, coord, cell_value
        
        if cell_value > target:
            return cell_value

        grid[coord] = cell_value
        
    
if __name__ == "__main__":
    target = int(sys.argv[1])

    print spiral_until(target)
