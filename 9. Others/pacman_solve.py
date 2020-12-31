class State:
    def __init__(self, coordinate):
        self.coordinate = coordinate
        self.height = 0

    def find_children(self):
        row = self.coordinate[0]
        column = self.coordinate[1]
        children = []  # moving nowhere
        if row - 1 >= 0:
            if game_grid[row - 1][column] != 2:  # moving upward
                children.append(State((row - 1, column)))
        if row + 1 <= m - 1:
            if game_grid[row + 1][column] != 2:  # moving downward
                children.append(State((row + 1, column)))
        if column - 1 >= 0:
            if game_grid[row][column - 1] != 2:  # moving left
                children.append(State((row, column - 1)))
        if column + 1 <= n - 1:
            if game_grid[row][column + 1] != 2:  # moving right
                children.append(State((row, column + 1)))
        return children

    def __eq__(self, other):
        return self.coordinate[0] == other.coordinate[0] and self.coordinate[1] == other.coordinate[1]


def find_minimum_steps(state, target_row, target_col):
    # use bfs to find smallest path between the pac_man and the cell in (target_row,target_col)
    fringe = [state]
    explored = []
    while len(fringe) > 0:
        s = fringe.pop(0)
        explored.append(s)
        if s.coordinate[0] == target_row and s.coordinate[1] == target_col:
            return s.height
        for child in s.find_children():
            if child not in fringe and child not in explored:
                child.height = s.height + 1
                fringe.append(child)
    return 0


def find_all_pac_mans():
    all_pac_mans = []
    for i in range(m):
        for j in range(n):
            if game_grid[i][j] == 3:
                all_pac_mans.append(State((i, j)))
    return all_pac_mans


# m = number of rows, n = number of columns
m, n = map(int, input().split())
game_grid = [None] * m
for i in range(m):
    numbers = [int(num) for num in input().split(" ", n - 1)]
    game_grid[i] = numbers

all_pac_mans = find_all_pac_mans()
lengths = []
for i in range(m):
    for j in range(n):
        inner_lengths = []
        if game_grid[i][j] != 2:
            for pac_man in all_pac_mans:
                x = find_minimum_steps(pac_man, i, j)
                if x != 0:
                    inner_lengths.append(x)
            if len(inner_lengths) != 0:
                lengths.append(max(inner_lengths))
print(min(lengths))
