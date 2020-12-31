import math
import random
import time


class Graph:
    def __init__(self, number_of_vertices):
        self.number_of_vertices = int(number_of_vertices)
        self.neighbors_list = []
        for i in range(number_of_vertices):
            self.neighbors_list.append([])

    def add_edge(self, u, v):
        u = int(u)
        v = int(v)
        self.neighbors_list[v].append(u)
        self.neighbors_list[u].append(v)
        pass

    def make_random_set(self):
        set_one = random.sample(range(0, self.number_of_vertices), int(self.number_of_vertices / 2))
        random_set = set()
        for i in set_one:
            random_set.add(i)
        return random_set

    def calculate_number_of_edges(self, set_one):
        set_one = set(set_one)
        number_of_edges = 0

        for node in set_one:
            node = int(node)
            for j in self.neighbors_list[node]:
                if j not in set_one:
                    number_of_edges = number_of_edges + 1
                    pass
                pass
            pass
        return number_of_edges


class State:
    def __init__(self, graph, set_one):
        self.set_one = set(set_one)
        self.value = Graph.calculate_number_of_edges(graph, set_one)
        self.set_two = set()
        for i in range(graph.number_of_vertices):
            if i not in set_one:
                self.set_two.add(i)

    def __eq__(self, other):
        if self.set_one == other.set_one or self.set_one == other.set_two:
            return True
        return False

    def get_lowest_child(self, graph):
        global lowest_child
        value = math.pow(graph.number_of_vertices, 2)
        for i in self.set_one:
            for j in self.set_two:
                first_set = self.set_one.copy()
                first_set.discard(i)
                first_set.add(j)
                new_child = State(graph, first_set)
                if new_child.value < value:
                    lowest_child = new_child
                    value = new_child.value

        return lowest_child
        pass

    def get_random_child(self, graph):
        global lowest_child
        children = []
        for i in self.set_one:
            for j in self.set_two:
                first_set = self.set_one.copy()
                first_set.discard(i)
                first_set.add(j)
                new_child = State(graph, first_set)
                children.append(new_child)

        rand_index = random.randint(0, len(children) - 1)
        return children[rand_index]
        pass


def decision(probability):
    probability = float(probability)
    rand = float(random.uniform(0, 1))
    if rand < probability:
        return True
    return False


def hill_climbing(initial_state, graph):
    current = initial_state
    i = 0
    while True:
        # for checking time
        if i % 50 == 0:
            if time.time() - start_time > 270:  # 4.5 minutes
                break

        what_to_do = random.randint(0, 2)
        if what_to_do == 0:
            neighbor = current.get_lowest_child(graph)
            if neighbor.value > current.value:  # allows side-way moves
                continue
            current = neighbor
        elif what_to_do == 1:
            current_set = graph.make_random_set()
            new_current = State(graph, current_set)
            if new_current.value < current.value:
                current = new_current
        else:
            neighbor = current.get_random_child(graph)
            if neighbor.value > current.value:  # allows random moves
                continue
            current = neighbor
        i += 1
    return current
    pass


start_time = time.time()
n = int(input())
m = int(input())
graph = Graph(n)
for i in range(m):
    first, second = input().split()
    first = int(first)
    second = int(second)
    graph.add_edge(first - 1, second - 1)
    pass

initial_state_set = graph.make_random_set()
initial_state = State(graph, initial_state_set)
final_state = hill_climbing(initial_state, graph)
print(final_state.value)
for i in final_state.set_one:
    print(i + 1, end='')
    print(" ", end='')
print()
for i in final_state.set_two:
    print(i + 1, end='')
    print(" ", end='')

