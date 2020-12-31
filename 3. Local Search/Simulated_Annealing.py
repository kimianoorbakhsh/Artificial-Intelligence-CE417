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

    def select_random_successor(self, graph):
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


def decision(probability):
    probability = float(probability)
    rand = float(random.uniform(0, 1))
    if rand < probability:
        return True
    return False


def simulated_annealing(initial_state, graph):
    current = initial_state
    final = initial_state
    T = 80
    i = 0
    while True:
        # for checking time
        if i % 50 == 0:
            if time.time() - start_time > 270:  # 4.5 minutes
                break

        next = current.select_random_successor(graph)
        delta = next.value - current.value
        if delta <= 0:
            current = next
            final = next

        else:
            prob = decision(math.pow(math.e, (-1 * delta) / T))
            if prob:
                current = next

        i += 1
        T = 0.9 * T

    if final.value < current.value:
        return final
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
final_state = simulated_annealing(initial_state, graph)
print(final_state.value)
for i in final_state.set_one:
    print(i + 1, end='')
    print(" ", end='')
print()
for i in final_state.set_two:
    print(i + 1, end='')
    print(" ", end='')
