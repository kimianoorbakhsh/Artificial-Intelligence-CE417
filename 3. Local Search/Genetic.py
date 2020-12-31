import random
import time


class State:
    def __init__(self, strings):
        strings = list(strings)
        self.strings = strings
        self.real_lengths = self.get_real_lengths()
        self.chromosome = self.get_chromosome()
        self.cost = self.calculate_total_cost(cc, table, alphabet)

    def __eq__(self, other):
        if self.chromosome == other.chromosome:
            return True
        return False

    def get_chromosome(self):
        chromosome = []
        for str in self.strings:
            count = 0
            for c in str:
                if c == '-':
                    count += 1
                else:
                    chromosome.append(count)
                    count = 0
            chromosome.append(count)
        return chromosome

    def get_real_lengths(self):
        strings_copy = self.strings.copy()
        for i in range(len(strings_copy)):
            strings_copy[i] = strings_copy[i].replace("-", "")
        real_lengths = []
        for str in strings_copy:
            real_lengths.append(len(str))
        return real_lengths

    def calculate_conversion_cost(self, cc):
        number_of_dashes = 0
        for i in range(len(self.chromosome)):
            number_of_dashes = number_of_dashes + self.chromosome[i]
        return number_of_dashes * cc

    def calculate_matching_cost(self, table, alphabet):
        total_sum = 0
        for i in range(len(self.strings)):
            for j in range(len(self.strings)):
                if j > i:
                    total_sum = total_sum + calculate_matching_cost_for_two(self.strings[i], self.strings[j], table,
                                                                            alphabet)
        return total_sum

    def calculate_total_cost(self, cc, table, alphabet):
        conversion = self.calculate_conversion_cost(cc)
        matching = self.calculate_matching_cost(table, alphabet)
        return conversion + matching


def calculate_matching_cost_for_two(string_1, string_2, table, alphabet):  # make sure len(string_1==len(string_2)
    alphabet = dict(alphabet)
    table = list(list(table))
    sum = 0
    for k in range(len(string_1)):
        char_1 = string_1[k]
        char_2 = string_2[k]
        if char_1 != "-" and char_2 != "-":
            i = alphabet.get(char_1)
            j = alphabet.get(char_2)
            sum = sum + table[i][j]
        elif char_1 != "-":
            i = alphabet.get(char_1)
            sum = sum + table[i][len(alphabet)]
        elif char_2 != "-":
            j = alphabet.get(char_2)
            sum = sum + table[len(alphabet)][j]
        else:
            sum = sum + table[len(alphabet)][len(alphabet)]
    return sum
    pass


def make_random_state(strings):
    random_additional_dashes = 0
    # random.randint(0, 5)
    strings = list(strings)
    number_of_dashes = []
    max_length = len(max(strings, key=len))
    for str in strings:
        number_of_dashes.append(max_length - len(str))
    new_strings = []
    for i in range(len(strings)):
        copy_string = strings[i]
        for j in range(number_of_dashes[i] + random_additional_dashes):
            rand = random.randint(0, len(copy_string))
            copy_string = copy_string[:rand] + '-' + copy_string[rand:]
        new_strings.append(copy_string)

    return State(new_strings)


def initialize_population(strings):
    population = []
    for i in range(14):  # ********
        state = make_random_state(strings)
        population.append(state)
    return population


def decision(probability):
    probability = float(probability)
    rand = float(random.uniform(0, 1))
    if rand < probability:
        return True
    return False


def selection_of_population(population):
    selected_population = []
    prob = decision(0.6)
    if prob:
        states = []  # ************
        for i in range(len(population)):
            states.append(population[i])
        costs = []
        for i in range(len(population)):
            costs.append(states[i].cost)
        total_cost = 0
        for i in range(len(population)):
            total_cost = total_cost + costs[i]
        weights = []
        for i in range(len(population)):
            weights.append((total_cost - costs[i]))
        sample_population = list(range(len(population)))
        selected_numbers = random.choices(population=sample_population, weights=weights, k=len(population))
        for i in range(len(population)):
            selected_population.append(population[selected_numbers[i]])
    else:
        selected_population = initialize_population(strings)
    return selected_population


def make_state_from_chromosome(strings, chromosome):
    lengths = []  # length[i] represents the real length of i th string
    state_strings = []
    for str in strings:
        lengths.append(len(str) + 1)
    index = 0
    for i in range(len(strings)):
        number_of_dashes_added = 0
        copy_string = strings[i]
        for j in range(len(copy_string) + 1):
            for k in range(chromosome[index]):
                ind = j + number_of_dashes_added
                copy_string = copy_string[:ind] + '-' + copy_string[ind:]
                number_of_dashes_added = number_of_dashes_added + 1
            index = index + 1
        state_strings.append(copy_string)
    #   use normalize function
    return State(normalize_state(state_strings))


def normalize_state(state_strings):
    state_strings = list(state_strings)
    copy_strings = state_strings.copy()
    max_length = len(max(copy_strings, key=len))
    for i in range(len(copy_strings)):
        length = len(copy_strings[i])
        for j in range(max_length - len(copy_strings[i])):
            rand = random.randint(0, len(copy_strings[i]))
            copy_strings[i] = copy_strings[i][:rand] + '-' + copy_strings[i][rand:]
    return copy_strings


def cross_over(population, strings):
    random.shuffle(population)
    crossed_over_population = []
    for i in range(0, 14, 2):
        state_1 = population[i]
        state_2 = population[i + 1]
        chromosome_1 = state_1.chromosome
        chromosome_2 = state_2.chromosome
        chromosome_length = len(chromosome_1)
        cut_points = random.sample(range(chromosome_length), 2)
        cut_point_1 = cut_points[0]
        cut_point_2 = cut_points[1]
        first_1 = chromosome_1[0:cut_point_1]
        second_1 = chromosome_1[cut_point_1:cut_point_2]
        third_1 = chromosome_1[cut_point_2:len(chromosome_1)]
        first_2 = chromosome_2[0:cut_point_1]
        second_2 = chromosome_2[cut_point_1:cut_point_2]
        third_2 = chromosome_2[cut_point_2:len(chromosome_2)]
        new_chromosome_1 = first_1 + second_2 + third_1
        new_chromosome_2 = first_2 + second_1 + third_2
        new_state_1 = make_state_from_chromosome(strings, new_chromosome_1)
        new_state_2 = make_state_from_chromosome(strings, new_chromosome_2)
        crossed_over_population.append(new_state_1)
        crossed_over_population.append(new_state_2)
    return crossed_over_population


def mutation(population, strings):
    new_population = []
    for i in range(len(population)):
        k = 0
        chromosome = population[i].chromosome
        for j in range(len(chromosome)):
            if chromosome[j] != 0:
                k = j
                break
        first = chromosome[k]
        second = chromosome[k + 1]
        chromosome[k] = second
        chromosome[k + 1] = first
        new_population.append(make_state_from_chromosome(strings, chromosome))
    return new_population
    pass


def genetic_algorithm(strings):
    initial_population = initialize_population(strings)
    population = initial_population.copy()
    final_cost = 100000
    final_state = population[0]
    i = 0
    while True:
        # for checking time
        if i % 50 == 0:
            if time.time() - start_time > 270:  # 4.5 minutes
                break

        selected_population = selection_of_population(population)
        population = cross_over(selected_population, strings)
        if i % 100 == 0:
            population = mutation(population, strings)
        min_state = min(population, key=lambda x: x.cost)
        if min_state.cost < final_cost:
            final_cost = min_state.cost
            final_state = min_state
        i += 1
    return final_state


start_time = time.time()
alphabet_length = int(input())
alphabet_list = input().split(", ")  # a list of alphabet
alphabet = dict()
for i in range(alphabet_length):  # stores the alphabet and their index in the alphabet list
    alphabet[alphabet_list[i]] = i
k = int(input())
strings = []
for i in range(k):
    str = input()
    strings.append(str)
cc = int(input())
table = []
for i in range(alphabet_length + 1):
    table.append([])
for i in range(alphabet_length + 1):
    numbers_list = list(map(int, input().split()))
    for number in numbers_list:
        table[i].append(number)

final_state = genetic_algorithm(strings)
print(final_state.cost)
for str in final_state.strings:
    print(str)
