import copy


class Node:
    def __init__(self, number):
        self.number = number
        self.parent = None
        self.adjacent_nodes = []  # list of adjacent nodes (must be from Node class)
        self.domain = []  # list of colors
        self.marked = False
        self.assigned_value = None

    def __eq__(self, other):
        return self.number == other.number

    def remove_inconsistent(self):  # removes inconsistent values from node's parent
        for color in self.parent.domain:
            is_consistent = False
            for my_color in self.domain:
                if my_color != color:
                    is_consistent = True
                    break
            if not is_consistent:
                if color in self.domain:
                    self.parent.domain.remove(color)


n, m, k = map(int, input().split())  # n = number of vertices, m = number of edges, k = number of colors
nodes = []  # keeps track of all nodes
for i in range(n):
    new_node = Node(i + 1)
    new_node.domain = list(map(int, input().split()))
    nodes.append(new_node)
for i in range(m):
    first, second = map(int, input().split())
    if first == 1:
        nodes[0].adjacent_nodes.append(nodes[second - 1])
    elif second == 1:
        nodes[0].adjacent_nodes.append(nodes[first - 1])
    else:
        nodes[first - 1].adjacent_nodes.append(nodes[second - 1])
        nodes[second - 1].adjacent_nodes.append(nodes[first - 1])
# now we have to set the parents from node 2 and save the topological sort
queue = []
nodes[1].marked = True
partial_order = []  # keep track of node's numbers in the partial order
queue.append(nodes[1])
while len(queue) != 0:  # BFS
    w = queue.pop(0)
    for adjacent in w.adjacent_nodes:
        if not adjacent.marked:
            adjacent.marked = True
            queue.append(adjacent)
            partial_order.append(adjacent.number)
            adjacent.parent = w
real_order = partial_order.copy()
partial_order.reverse()
print_no = True
for color in nodes[0].domain:
    continue_this_loop = False
    copy_nodes = copy.deepcopy(nodes)
    copy_nodes[0].assigned_value = color
    for node in copy_nodes[0].adjacent_nodes:
        if color in node.domain:
            node.domain.remove(color)
        if len(node.domain) == 0:
            continue_this_loop = True
            break
    if continue_this_loop:
        continue
    for node_number in partial_order:
        copy_nodes[node_number - 1].remove_inconsistent()
    continue_the_loop = False
    for node in copy_nodes:
        if len(node.domain) == 0:
            continue_the_loop = True
    if continue_the_loop:
        continue
    if len(copy_nodes[1].domain) == 0:
        continue
    copy_nodes[1].assigned_value = copy_nodes[1].domain[0]
    for number in real_order:
        for node_color in copy_nodes[number - 1].domain:
            if node_color != copy_nodes[number - 1].parent.assigned_value:
                copy_nodes[number - 1].assigned_value = node_color
                break
    for node in copy_nodes:
        print(node.assigned_value, end=' ')
    print_no = False
    break

if print_no:
    print("NO")
