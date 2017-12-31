import fileinput
import knot2 as knot

# There are much cleaner ways to do this (without any strings), but I'm on an
# airplane and not feeling very elegant.
def generate_disk_row(row_input):
    bits_hex = knot.knot128(row_input)
    # print row_input, "\t",  bits_hex
    row = []
    for h in bits_hex:
        binary_string = bin(int(h, base=16) + 16)[-4:]
        row.extend(map(lambda x: bool(int(x)), binary_string))

    return row

def generate_disk_layout(puzzle_input):
    result = []
    for row_i in xrange(128):
        result.append(generate_disk_row(puzzle_input+"-"+str(row_i)))
        
    return result

def print_grid(grid, lmbd):
    for row in grid:
        print "".join(map(lmbd, row))
    

def print_disk_layout(disk_layout):
    print_grid(disk_layout, lambda used: "#" if used else ".")

def print_region_map(region_map):
    print_grid(region_map, region_to_string)

region_charset = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def region_to_string(region):
    if region is None:
        return "."

    return region_charset[region % len(region_charset)]

def count_trues(row):
    return sum(map(lambda used: 1 if used else 0, row))

def count_disk_usage(disk_layout):
    return sum(map(count_trues, disk_layout))

def count_regions(disk_layout):
    r = 0
    # Create a None-initialized 128x128 array
    region_map = [[None for x in xrange(128)] for y in xrange(128)]
    for x in xrange(128):
        for y in xrange(128):
            used = disk_layout[x][y] == 1
            if not used:
                continue

            already_seen = region_map[x][y] is not None
            if already_seen:
                continue

            extend_region(region_map, disk_layout, r, x, y)
            r += 1

    print_region_map(region_map)

    return r
            

# Extend region if possible
def extend_region(region_map, disk_layout, region_id, x, y):
    if x < 0 or y < 0 or x >= 128 or y >= 128:
        return

    used = disk_layout[x][y] == 1
    if not used:
        return

    existing_region_id = region_map[x][y]
    if existing_region_id is not None and existing_region_id != region_id:
        raise Exception("%s %s %s %s" % (x,y,existing_region_id, region_id))

    elif existing_region_id == region_id:
        return

    region_map[x][y] = region_id
    extend_region(region_map, disk_layout, region_id, x+1, y  )
    extend_region(region_map, disk_layout, region_id, x  , y+1)
    extend_region(region_map, disk_layout, region_id, x-1, y  )
    extend_region(region_map, disk_layout, region_id, x  , y-1)



if __name__ == "__main__":
    puzzle_input = next(fileinput.input()).strip()

    disk_layout = generate_disk_layout(puzzle_input)

    print_disk_layout(disk_layout)

    print "Answer 1"
    print count_disk_usage(disk_layout)
    print
    print "Answer 2"
    print count_regions(disk_layout)
    
