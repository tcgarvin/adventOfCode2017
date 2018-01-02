
from __future__ import print_function

import fileinput
from collections import defaultdict, namedtuple

NodeData = namedtuple('NodeData', ['name', 'weight', 'children_names'])

class Node:
    def __init__(self, name, weight, children = None):
        self.name = name
        self.weight = weight
        self.children = children if children is not None else []
        self.parent = None

        # Doesn't belong here
        for child in children:
            assert not child.has_parent()
            child.parent = self

    def has_children(self):
        return len(self.children) > 0

    def has_parent(self):
        return self.parent is not None

    def total_weight(self):
        return self.weight + sum(child.total_weight() for child in self.children)

    def find_unbalanced_child(self):
        counts = defaultdict(list)

        for child in self.children:
            counts[child.total_weight()].append(child)

        if len(counts) > 1:
            print(self)
            for child in self.children:
                print("\t%s\t%s" % (child.total_weight(), child))
            print("")

            # We know there's only one out of balance
            for children in counts.itervalues():
                if len(children) == 1:
                    return children[0]

        return None

    def __repr__(self):
        return "Node(%s, %s, %s)" % (self.name, self.weight, [c.name for c in self.children])


def parse_input(input):
    index = {}
    for line in input:
        node_data = parse_line(line)
        index[node_data.name] = node_data

    return index


# The input is mercifully well-ordered
def parse_line(line):
    tokens = line.split(" ")
    name = tokens[0]
    weight = int(tokens[1].strip().strip("()"))
    children_names = (t.strip().strip(",") for t in tokens[3:])
    return NodeData(name, weight, children_names)


# The idea is to build parts of the tree and stitch it together using the
# input and a record of which nodes we've already built.
def build_tree(input_index):
    node_index = {}
    for name, data in input_index.iteritems():
        if name in node_index:
            continue
        node_index[name] = instantiate_node(data, input_index, node_index)

    curs = next(node_index.itervalues())
    while curs.has_parent():
        curs = curs.parent

    return curs


def instantiate_node(data, input_index, node_index):
    if data.name in node_index:
        return node_index[data.name]

    children = (instantiate_node(input_index[name], input_index, node_index) for name in data.children_names)
    node = Node(data.name, data.weight, children)

    node_index[data.name] = node
    return node


def find_unbalanced_decendant(node):
    candidate = node

    while candidate is not None:
        next_candidate = candidate.find_unbalanced_child()
        if next_candidate is None:
            break
        candidate = next_candidate

    return candidate

    
if __name__ == "__main__":

    input_index = parse_input(fileinput.input())
    
    root_node = build_tree(input_index)

    print(find_unbalanced_decendant(root_node))
