import random


class BayesNet:
    def __init__(self):
        self.variables = {}
        self.letters = []
        self.query = None
        self.letters = None

    def add_children(self, variable, parents):
        # Adds variable to the children list of each parent
        for parent in parents:
            if variable not in self.variables[parent].children:
                self.variables[parent].children.append(variable)

    def topological_Sort_Util(self, var, stack):
        var.marked = True
        # Recur for all the vertices adjacent to this vertex
        for i in var.children:
            if not self.variables[i].marked:
                self.topological_Sort_Util(self.variables[i], stack)
                # Push current vertex to stack which stores result
        stack.insert(0, var.letter)

    def topological_sort(self):
        stack = []
        for var in self.letters:
            if not self.variables[var].marked:
                self.topological_Sort_Util(self.variables[var], stack)
        return stack

    def sample(self, probability):
        return random.uniform(0.0, 1.0) < probability

    def prior_sample(self):
        values = {}
        for letter in self.letters:
            prob = self.variables[letter].get_probability(values)
            values[letter] = self.sample(prob)
        return values

    def is_consistent(self, event):
        # Is event consistent with the given evidence?
        return all(self.query.evidence.get(k, v) == v for k, v in event.items())

    def rejection_sample(self, number_of_samples):
        counts = {x: 0 for x in [True, False]}
        for j in range(number_of_samples):
            sample = self.prior_sample()
            if self.is_consistent(sample):
                counts[sample[self.query.variable]] += 1
        return counts[True] / (counts[True] + counts[False])  # normalizing

    def weighted_sample(self):
        # Samples an event from bayes net that's consistent with the evidence, returns the event and its weight
        weight = 1
        event = dict(self.query.evidence)
        for variable in self.letters:
            x_i = variable
            if x_i in self.query.evidence:
                if event[x_i]:
                    weight *= self.variables[variable].get_probability(event)
                else:
                    weight *= 1 - self.variables[variable].get_probability(event)
            else:
                prob = self.variables[variable].get_probability(event)
                event[x_i] = self.sample(prob)
        return event, weight

    def likelihood_sample(self, number_of_samples):
        weights = {x: 0 for x in [True, False]}
        for j in range(number_of_samples):
            sample, weight = self.weighted_sample()
            weights[sample[self.query.variable]] += weight
        return weights[True] / (weights[True] + weights[False])  # normalizing

    def sample_from_markov_blanket(self, some_node, event):
        # The Markov blanket of node is node's parents, children, and its children's parents
        # event has the values of the variables
        node = self.variables[some_node]
        new_distribution = ProbabilityDistribution(some_node)
        for value in [True, False]:
            event_i = make_dict(event, some_node, value)
            if value:
                prob = node.get_probability(event)
            else:
                prob = 1 - node.get_probability(event)
            product = 1
            for child in node.children:
                # Joining the probabilities
                if event_i[child]:
                    product = product * self.variables[child].get_probability(event_i)
                else:
                    product = product * (1 - self.variables[child].get_probability(event_i))
            new_distribution[value] = prob * product
        sum_of_all = sum(new_distribution.probability.values())
        if sum_of_all == 0:
            returned_value = self.sample(0)
        else:
            returned_value = self.sample(new_distribution.normalize()[True])
        return returned_value

    def gibbs_sampling(self, number_of_samples):
        count_list = {x: 0 for x in [True, False]}
        # Z is defined as in slide 64
        Z = [variable for variable in self.variables if variable not in self.query.evidence]
        state = dict(self.query.evidence)
        for variable in Z:
            # assigns randomly
            state[variable] = random.choice([True, False])
        for i in range(number_of_samples):
            # now re-sample according to the markov blanket
            for variable in Z:
                state[variable] = self.sample_from_markov_blanket(variable, state)
                count_list[state[self.query.variable]] += 1
        return count_list[True] / (count_list[True] + count_list[False])  # normalizing


def make_dict(s, variable, value):
    # Copies dict s and extend it by setting variable to value; return copy
    return eval('{**s, variable: value}')


class Variable:
    def __init__(self, letter):
        self.letter = letter
        self.distribution = {}  # Maps values of parents (ex: True, True, False) to
        self.parents = []
        self.children = []
        self.probability = 0.0  # Only for variables with no parents
        self.marked = False

    def get_probability(self, values):
        if len(self.parents) == 0:
            return self.probability
        else:
            key = tuple([values[letter] for letter in self.parents])
            # always returns the True value of the query
            return self.distribution[key]

    def __eq__(self, other):
        return self.letter == other.letter


class Query:

    def __init__(self, variable, evidence):
        self.variable = variable
        self.evidence = {}
        for s in evidence:
            self.evidence[s[1]] = (s[0] == "+")


class ProbabilityDistribution:

    def __init__(self, name='unknown', distribution=None):
        self.probability = {}
        self.name = name
        self.values = []
        if distribution:
            for (variable, probability) in distribution.items():
                self[variable] = probability
            self.normalize()

    def normalize(self):
        # Returns the normalized distribution
        total_sum = sum(self.probability.values())
        for value in self.probability:
            self.probability[value] /= total_sum
        return self

    def __setitem__(self, value, p):
        # sets probability(value) = p
        if value not in self.values:
            self.values.append(value)
        self.probability[value] = p

    def __getitem__(self, val):
        # Given a value, return probability(value)
        return self.probability[val]


bayes_net = BayesNet()
n = int(input())
letters = input()
bayes_net.letters = letters.split(' ')
for letter in bayes_net.letters:
    bayes_net.variables[letter] = Variable(letter)
m = int(input())
for i in range(m):
    line = input()
    parts = line.split(' ')
    probability = float(parts.pop())
    dependent_variable = parts.pop()
    parents = [s[1] for s in parts]
    values = tuple((s[0] == "+") for s in parts)

    if len(parents) > 0:
        bayes_net.variables[dependent_variable].parents = parents
        bayes_net.add_children(dependent_variable, parents)
        bayes_net.variables[dependent_variable].distribution[values] = probability
    else:
        bayes_net.variables[dependent_variable].probability = probability
line = input()
query_parts = line.split(' ')
dependent_variable = query_parts.pop(0)
bayes_net.query = Query(dependent_variable, query_parts)
bayes_net.letters = bayes_net.topological_sort()
# print("Rejection Sampling : ", end="")
print(bayes_net.rejection_sample(100000))
# print("Likelihood Sampling : ", end="")
print(bayes_net.likelihood_sample(100000))
# print("Gibbs Sampling : ", end="")
print(bayes_net.gibbs_sampling(50000))
