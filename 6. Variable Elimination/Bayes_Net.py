import numpy


class ProbabilityDistribution:

    def __init__(self, name='unknown', distribution=None):
        self.probability = {}
        self.name = name
        self.values = []
        if distribution:
            for (variable, probability) in distribution.items():
                self[variable] = probability
            self.normalize()

    def __setitem__(self, value, p):
        # sets P(value) = p
        if value not in self.values:
            self.values.append(value)
        self.probability[value] = p

    def normalize(self):
        # Returns the normalized distribution.
        sum_of_all = sum(self.probability.values())
        for value in self.probability:
            self.probability[value] /= sum_of_all
        return self


class Node:

    def __init__(self, variable_name, parents, cpt):
        self.variable = variable_name
        self.children = []
        # a dict {(v1, v2, ...): p, ...}, the distribution P(X=true | parent1=v1, parent2=v2, ...) = p.
        if isinstance(parents, str):
            parents = parents.split()  # to split the parents string into list
        if isinstance(cpt, (float, int)):  # no parents, 0-tuple
            cpt = {(): cpt}
        elif isinstance(cpt, dict):  # one parent, 1-tuple
            if cpt and isinstance(list(cpt.keys())[0], bool):
                cpt = {(variable,): p for variable, p in cpt.items()}

        self.parents = parents
        self.cpt = cpt

    def probability(self, value, event):
        # Return the conditional probability P(X=value | parents=parent_values), event assigns each parent a value.
        true_probability = self.cpt[event_variables_values(event, self.parents)]
        if value:
            return true_probability
        return 1 - true_probability


def variable_values(variable):
    # Returns the domain of var
    return [True, False]


class BayesNet:

    def __init__(self):
        # Nodes must be ordered with parents before children.
        self.nodes = []
        self.variables = []

    def add(self, new_node):
        # Adds a node to the bayes net
        node = Node(*new_node)  # tuple
        self.nodes.append(node)
        self.variables.append(node.variable)
        for parent in node.parents:
            self.variable_node(parent).children.append(node)  # adds the new_node to its parents children

    def variable_node(self, variable_name):
        # Return the node for the variable named variable_name
        for node in self.nodes:
            if node.variable == variable_name:
                return node


class Factor:

    def __init__(self, variables, cpt):
        self.variables = variables
        self.cpt = cpt

    def point_wise_product(self, other, bayes_net):
        # Multiply two factors, combining their variables
        variables = list(set(self.variables) | set(other.variables))  # finds both variables in self and other
        cpt = {event_variables_values(event, variables): self.probability(event) * other.probability(event) for event in
               all_events(variables, bayes_net, {})}
        return Factor(variables, cpt)

    def sum_out(self, variable, bayes_net):
        # Makes a factor eliminating var by summing over its values
        variables = [var for var in self.variables if var != variable]
        cpt = {event_variables_values(event, variables): sum(
            self.probability(extend(event, variable, val)) for val in variable_values(variable))
            for event in all_events(variables, bayes_net, {})}
        return Factor(variables, cpt)

    def normalize(self):
        return ProbabilityDistribution(self.variables[0], {key: value for ((key,), value) in self.cpt.items()})

    def probability(self, event):
        return self.cpt[event_variables_values(event, self.variables)]


def variable_elimination(variable_name, evidence, bayes_net):
    factors = []
    for variable in reversed(bayes_net.variables):
        factors.append(make_factor(variable, evidence, bayes_net))
        if hidden(variable, variable_name, evidence):
            factors = sum_out(variable, factors, bayes_net)
    return point_wise_product(factors, bayes_net).normalize()


def hidden(variable, query, evidence):
    # is the variable a hidden variable when elimination
    if variable not in evidence:
        return variable != query


def make_factor(variable, evidence, bayes_net):
    node = bayes_net.variable_node(variable)
    variables = [X for X in [variable] + node.parents if X not in evidence]
    cpt = {event_variables_values(event, variables): node.probability(event[variable], event)
           for event in all_events(variables, bayes_net, evidence)}
    return Factor(variables, cpt)


def extend(s, variable, value):
    # Copies dict s and extend it by setting variable to value; return copy
    return eval('{**s, variable: value}')


def point_wise_product(factors, bayes_net):
    import functools
    return functools.reduce(lambda f, g: f.point_wise_product(g, bayes_net), factors)


def sum_out(variable, factors, bn):
    # eliminate the variable from all factors by summing over its values
    result, variable_factors = [], []
    for factor in factors:
        (variable_factors if variable in factor.variables else result).append(factor)
    result.append(point_wise_product(variable_factors, bn).sum_out(variable, bn))
    return result


def event_variables_values(event, variables):
    # Returns a tuple of the values of variables in the event.
    if isinstance(event, tuple) and len(event) == len(variables):
        return event
    else:
        return tuple([event[variable] for variable in variables])


def all_events(variables, bayes_net, event):
    # Yield every way of extending e with values for all variables
    if not variables:
        yield event
    else:
        query = variables[0]
        rest = variables[1:]
        for event_1 in all_events(rest, bayes_net, event):
            for x in variable_values(query):
                yield extend(event_1, query, x)


net = BayesNet()
while True:
    s = input()
    if s == ".":
        break
    s = s[1:]
    s = s[:-1]
    array_of_strings = s.split(", [")
    name = array_of_strings[0]
    evidences = array_of_strings[1][:-1]
    evidences = evidences.replace(", ", " ")
    probabilities = array_of_strings[2][:-1].split(", ")
    number_of_digits = "{0:b}".format(len(probabilities) - 1).__len__()
    cpt = dict()
    if len(probabilities) == 1:
        net.add((name, evidences, float(probabilities[0])))
        continue
    elif len(probabilities) == 2:
        cpt[True] = float(probabilities[0])
        cpt[False] = float(probabilities[1])
        net.add((name, evidences, cpt))
        continue
    for i in range(len(probabilities) - 1, -1, -1):
        table = "{0:b}".format(i)
        for j in range(number_of_digits - len(table)):
            table = "0" + table
        t = ()
        for j in range(len(table)):
            if table[j] == "1":
                t = t + (True,)
            else:
                t = t + (False,)
        cpt[t] = float(probabilities[len(probabilities) - 1 - i])
    net.add((name, evidences, cpt))
while True:
    s = input()
    if s == ".":
        break
    s = s[1:]
    s = s[:-1]
    array_of_strings = s.split(", [")
    variable_name = array_of_strings[0][1:]
    variable_name = variable_name[:-1]
    evidences = array_of_strings[1][:-1]
    evidences = evidences.replace(", ", " ")
    true_or_false = array_of_strings[2][:-1].split(", ")
    evidence = evidences.split(" ")
    e = dict()
    for i in range(len(evidence)):
        if true_or_false[i] == "1":
            e[evidence[i]] = True
        else:
            e[evidence[i]] = False
    query = variable_elimination(variable_name, e, net)
    print("{:.2f}".format(query.probability[1]))
    print("{:.2f}".format(query.probability[0]))
