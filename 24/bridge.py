import fileinput
from collections import defaultdict

def index_by_ports(parts):
    index = defaultdict(set)
    for part in parts:
        index[part[0]].add(part)
        index[part[1]].add(part)

    return index


def get_part_strength(part):
    return part[0] + part[1]


def recurse_strongest_bridge(parts_seen, part_index, next_port):
    compatible_parts = part_index[next_port]
    # We get to make a nice assumption that parts are unique
    available_parts = filter(lambda p: p not in parts_seen, compatible_parts)

    best_strength = 0
    best_bridge = []
    for part in available_parts:
        open_port = part[0]
        if next_port == open_port:
            open_port = part[1]

        part_strength = get_part_strength(part)
        
        # Going to make a silly pre-optimization here, where we re-use and
        # increment/decrement parts_seen instead of maing copies
        parts_seen.add(part)
        sub_bridge, sub_strength = recurse_strongest_bridge(parts_seen, part_index, open_port)
        parts_seen.remove(part)

        bridge_strength = sub_strength + part_strength
        if bridge_strength > best_strength:
            best_strength = bridge_strength
            sub_bridge.insert(0, part)
            best_bridge = sub_bridge

    return best_bridge, best_strength
    

def strongest_bridge(parts):
    part_index = index_by_ports(parts)

    best_bridge, best_strength = recurse_strongest_bridge(set(), part_index, 0)

    return (best_bridge, best_strength)


def recurse_longest_bridge(parts_seen, part_index, next_port):
    compatible_parts = part_index[next_port]
    # We get to make a nice assumption that parts are unique
    available_parts = filter(lambda p: p not in parts_seen, compatible_parts)

    best_strength = 0
    best_bridge = []
    for part in available_parts:
        open_port = part[0]
        if next_port == open_port:
            open_port = part[1]

        part_strength = get_part_strength(part)
        
        # Going to make a silly pre-optimization here, where we re-use and
        # increment/decrement parts_seen instead of maing copies
        parts_seen.add(part)
        sub_bridge, sub_strength = recurse_longest_bridge(parts_seen, part_index, open_port)
        parts_seen.remove(part)

        sub_bridge.insert(0, part)
        bridge_strength = sub_strength + part_strength
        if (len(sub_bridge) > len(best_bridge) 
                or (len(sub_bridge) == len(best_bridge) 
                    and bridge_strength > best_strength)):
            best_strength = bridge_strength
            best_bridge = sub_bridge

    return best_bridge, best_strength


def longest_bridge(parts):
    part_index = index_by_ports(parts)

    longest_bridge, bridge_strength = recurse_longest_bridge(set(), part_index, 0)
    return longest_bridge, bridge_strength


def parse_part(line):
    ports = line.split("/")
    return (int(ports[0]), int(ports[1]))

def parse_parts(lines):
    return map(parse_part, lines)

if __name__ == "__main__":
    parts = parse_parts(fileinput.input())

    bridge_parts, bridge_strength = strongest_bridge(parts)

    print "Answer 1"
    print bridge_strength
    print ""

    longest_bridge_parts, longest_bridge_strength = longest_bridge(parts)
    print longest_bridge_parts

    print "Answer 2"
    print longest_bridge_strength


    
