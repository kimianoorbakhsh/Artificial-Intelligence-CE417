import copy


class Node(object):
    def __init__(self, name=""):
        # parents and children dictionary is like (key = name, value = Node object)
        self.name = name
        self.parents = dict()
        self.children = dict()
        self.cause_node = None

    def add_parent(self, parent):
        # parent must be instance of Node class
        parent_name = parent.name
        self.parents[parent_name] = parent

    def add_child(self, child):
        # child must be instance of Node class
        cname = child.name
        self.children[cname] = child

    def add_cause_node(self, cause_node):
        self.cause_node = cause_node


class BayesNet(object):

    def __init__(self):
        # nodes are a dictionary such that (key = name, value = Node object)
        self.nodes = dict()

    def add_edge(self, edge):
        # edge is a tuple like (a,b) such that a,b are the names of nodes
        (parent_name, child_name) = edge

        # construct a new node if it doesn't exist
        if parent_name not in self.nodes:
            self.nodes[parent_name] = Node(name=parent_name)
        if child_name not in self.nodes:
            self.nodes[child_name] = Node(name=child_name)

        # add edge
        parent = self.nodes.get(parent_name)
        child = self.nodes.get(child_name)
        parent.add_child(child)
        child.add_parent(parent)

    def find_parents_of_evidence_nodes(self, evidence):
        # Traverse the graph, find all nodes that have evidence descendants. (child or child of child)
        # evidence: a list of strings, names of the observed nodes.
        # return a list of strings for the nodes' names for all nodes  with evidence descendants.
        visit_nodes = copy.copy(evidence)  # nodes to visit
        parents_of_evidence_nodes = set()  # evidence nodes and their ancestors
        # repeatedly visit the nodes' parents
        while len(visit_nodes) > 0:
            next_node = self.nodes[visit_nodes.pop()]
            # add its' parents
            for parent in next_node.parents:
                parents_of_evidence_nodes.add(parent)
        return parents_of_evidence_nodes

    def is_d_separated(self, start, end, evidence):
        # all nodes having evidence descendants.
        parents_of_evidence_nodes = self.find_parents_of_evidence_nodes(evidence)
        # Try all active paths starting from the node "start".
        # If any of the paths reaches the node "end", then "start" and "end" are *not* d-separated.
        # "up" if traveled from child to parent, and "down" otherwise.
        nodes_to_visit = [(start, "up")]  # we just add active paths to see if we reach the end by an active path
        visited = set()  # keep track of visited nodes to avoid cyclic paths/ a set of tuples
        while len(nodes_to_visit) > 0:
            (node_name, direction) = nodes_to_visit.pop()
            current_node = self.nodes[node_name]
            # skip visited nodes
            if (node_name, direction) not in visited:
                visited.add((node_name, direction))
                # if reaches the node "end", then it is not d-separated
                if node_name not in evidence and node_name == end:
                    return False, current_node
                # if traversing from children, then it won't be a v-structure (a->b->c)
                # the path is active as long as the current node is unobserved
                if direction == "up" and node_name not in evidence:  # (1) a<-b->c where b is unobserved
                    for parent in current_node.parents:
                        nodes_to_visit.append((parent, "up"))
                        parent_node = self.nodes[parent]
                        if parent_node.cause_node is None:
                            parent_node.add_cause_node(current_node)
                    for child in current_node.children:
                        nodes_to_visit.append((child, "down"))
                        child_node = self.nodes[child]
                        if child_node.cause_node is None:
                            child_node.add_cause_node(current_node)
                # if traversing from parents, then need to check v-structure
                elif direction == "down":
                    # path to children is always active
                    if node_name not in evidence:  # (2) a->b->c where b is not observed
                        for child in current_node.children:
                            nodes_to_visit.append((child, "down"))
                            child_node = self.nodes[child]
                            if child_node.cause_node is None:
                                child_node.add_cause_node(current_node)
                    # path to parent forms a v-structure
                    if node_name in evidence or node_name in parents_of_evidence_nodes:
                        # (3) a->b<-c such that b or one of its descendants is observed
                        for parent in current_node.parents:
                            nodes_to_visit.append((parent, "up"))
                            parent_node = self.nodes[parent]
                            if parent_node.cause_node is None:
                                parent_node.add_cause_node(current_node)

        # if we reach here, there there was no active paths
        return True, []


bayes_net = BayesNet()
evidence_nodes = []
path = []
n, m, z = map(int, input().split())
for i in range(m):
    v1, v2 = map(int, input().split())
    bayes_net.add_edge((v1, v2))
for i in range(z):
    evidence_nodes.append(int(input()))
start_node, end_node = map(int, input().split())
result = bayes_net.is_d_separated(start_node, end_node, evidence_nodes)
if result[0]:
    print("independent")
else:
    node = result[1]
    while node.name != start_node:
        path.append(node.name)
        node = node.cause_node
    path.append(start_node)
    path.reverse()
    for i in range(len(path)):
        if i != len(path) - 1:
            print(path[i], end=", ")
        else:
            print(path[i])
