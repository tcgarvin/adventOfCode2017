import fileinput

# Mapping the grid like so:
#       
#       (1,1)
#(0,1) \ n  /   (1,0)
#    nw +--+ ne
#      /    \
#    -+      +-
#      \    /
#    sw +--+ se
#(-1,0)/ s  \   (0,-1)
#      (-1,-1)

move_map = {
    "n":  ( 1, 1),
    "ne": ( 1, 0),
    "se": ( 0,-1),
    "s":  (-1,-1),
    "sw": (-1, 0),
    "nw": ( 0, 1)
}

def parse_moves(text):
    return text.strip().split(",")


def moveTuple(move):
    return move_map[move]


def combineTuple(a,b):
    return (a[0] + b[0], a[1] + b[1])


# This could be done more formally, but intuitively:
#    -If the two coordinates are the same sign, they can diminish back to 0
#     together, since we have both a (1,1) and (-1,-1) move available to us.
#     So we just take max( |x| , |y| )
#
#    -If the two coordinates have different signs, we'll need to draw down
#     each one on it's own.  Therefore, sum( |x| , |y| )
def shortest_path_number_moves(destination):
    x = destination[0]
    y = destination[1]

    if x < 0 ^ y < 0:
        return abs(x) + abs(y)

    return max(abs(x), abs(y))
        

def combine_moves(moves):
    current = (0,0)
    furthest = current
    furthest_distance = shortest_path_number_moves(furthest)
    for move in map(moveTuple, moves):
        current = combineTuple(current, move)
        current_distance = shortest_path_number_moves(current)

        if current_distance > furthest_distance:
            furthest = current
            furthest_distance = current_distance

    return current, furthest


if __name__ == "__main__":
    moves = parse_moves(fileinput.input().readline())
    destination, furthest = combine_moves(moves)
    print destination
    print shortest_path_number_moves(destination)
    print furthest
    print shortest_path_number_moves(furthest)

