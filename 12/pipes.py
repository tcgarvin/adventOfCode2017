import fileinput

def parse_graph(lines):
    return map(parse_connections, lines)


def parse_connections(line):
    connections_substring = line[line.index(">") + 2:]
    return map(int, connections_substring.strip().split(","))


def get_group_containing(graph, member):
    seen = set()
    recurse(graph, member, seen)
    return seen
    

def recurse(graph, member, seen):
    if member in seen:
        return

    seen.add(member)

    for neighbor in graph[member]:
        recurse(graph, neighbor, seen)


def get_number_of_groups(graph):
    seen = set()
    groups = []

    for member in xrange(len(graph)):
        if member in seen:
            continue

        group = get_group_containing(graph, member)
        groups.append(group)
        seen = seen | group

    return len(groups)
    

if __name__ == "__main__":
    graph = parse_graph(fileinput.input())

    #members = get_group_containing(graph, 0)
    #print len(members)

    print get_number_of_groups(graph)
