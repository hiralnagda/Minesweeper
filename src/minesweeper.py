from tkinter import *
import numpy as np
from random import *
from find_neighbours import return_neighbours
from gui import GUI


class Minesweeper:
    def __init__(self, rows, columns, mines, interactive):
        self.mine_cells = []
        self.cells_explored = []
        self.prob_threshold = 0.2
        self.rows = rows
        self.columns = columns
        self.cell_prob = np.array([[1 for count_col in range(columns)] for
                                   count_row in range(rows)], dtype=np.float)
        self.inp = self.build_board(mines)
        self.cells = [[9 for i in range(self.columns)] for j in range(self.rows)]
        self.interactive = interactive
        self.game_over = False
        self.app = GUI(self.rows, self.columns)
        self.app.title('Minesweeper')

    def build_board(self, mines):
        board = []
        count = 0
        mine_locations = []
        while count < mines:
            row = randint(0, self.rows-1)
            col = randint(0, self.columns-1)
            if [row, col] not in mine_locations:
                count += 1
                mine_locations.append([row, col])
        for j in range(self.rows):
            board.append([0] * self.columns)
        for i in mine_locations:
            x, y = i
            board[x][y] = -2
            for j in return_neighbours(i, self.rows, self.columns):
                if j in mine_locations:
                    pass
                else:
                    board[j[0]][j[1]] += 1
        return board

    def is_known(self, point):
        if self.cells[point[0]][point[1]] != 9 and self.cells != -2:
            return True

    def get_value_from_user(self, a):
        if not self.interactive:
            value = self.inp[a[0]][a[1]]
        else:
            self.app.popup(a)
            value = int(self.app.entry_value())
        if value in [10]:
            sys.exit()
        elif value in [-2]:
            self.game_over = True
            if self.interactive is True:
                self.app.endpopup('The AI couldn\'t win:' + str(a))
                self.app.isopen = False
        else:
            return value

    def outer_cells(self, point):
        row = self.rows
        col = self.columns
        if (point[0] in [0, row - 1]) and (point[1] in [0, col - 1]):
            return 3
        elif (col - 1 > point[1] >= 1 and (point[0] == 0 or point[0] == row - 1)) or (row - 1 > point[0] >= 1 and (point[1] == 0 or point[1] == col - 1)):
            return 5
        else:
            return 8

    def known_neighbours(self, point):
        unknown_neighbours = []
        cell = mine = 0
        for neighbour in return_neighbours(point, self.rows, self.columns):
            if neighbour in self.mine_cells:
                mine = mine + 1
            elif self.is_known(neighbour):
                cell = cell + 1
            else:
                unknown_neighbours.append(neighbour)
        return [unknown_neighbours, cell, mine]

    def show_cell_prob(self):
        for row in range(self.rows):
            print(self.cell_prob[row][:])

    def choose_action(self):
        num = uniform(0, 1)
        if num > 0.005:
            self.update_cell_prob()
            minimum = np.where(self.cell_prob == np.min(self.cell_prob))
            maxval = len(minimum[0]) - 1
            index = randint(0, maxval)
            x = [minimum[0][index], minimum[1][index]]
            if self.prob_threshold <= self.cell_prob[x[0]][x[1]]:
                minimum = np.where(self.cell_prob == 1)
                if not len(minimum[0]):
                    return x
                index = randint(0, maxval)
                return [minimum[0][index], minimum[1][index]]
            return x
        else:
            point = [randint(0, self.rows - 1), randint(0, self.columns - 1)]
            while self.is_known(point):
                point = [randint(0, self.rows - 1), randint(0, self.columns - 1)]
            return point

    def update_cell_prob(self):
        for row in range(self.rows):
            for col in range(self.columns):
                d = self.known_neighbours([row, col])
                if len(d[0]) == 0 or self.cells[row][col] == 0 or self.cells[row][col] == -2:
                    self.cell_prob[row][col] = 2
                elif self.is_known([row, col]):
                    self.cell_prob[row][col] = 2
                    num = self.cells[row][col] - d[2]
                    den = len(d[0])
                    prob = num / den
                    for k in d[0]:
                        if self.cell_prob[k[0]][k[1]] == 1:
                            self.cell_prob[k[0]][k[1]] = prob
                        else:
                            if prob > self.cell_prob[k[0]][k[1]]:
                                self.cell_prob[k[0]][k[1]] = prob

                elif len(d[0]) == 0 or self.cells[row][col] == 0 or self.cells[row][col] == -2:
                    self.cell_prob[row][col] = 2

    def explore_helper(self, x):
        for i in return_neighbours(x, self.rows, self.columns):
            self.explore_cell(i)

    def add_mine_cells(self, cell):
        if cell in self.mine_cells:
            pass
        else:
            self.mine_cells.append(cell)

    def set_cell_value(self, point, is_mine):
        if is_mine:
            self.cells[point[0]][point[1]] = -2
            self.show(point)
            return
        else:
            if self.is_known(point):
                pass
            else:
                user_val = self.get_value_from_user(point)
                self.cells[point[0]][point[1]] = user_val
                self.show(point)
                if not user_val:
                    for neighbour in return_neighbours(point, self.rows, self.columns):
                        if not self.is_known(neighbour):
                            self.set_cell_value(neighbour, False)
                    return

    def show(self, loc):
        val = self.cells[loc[0]][loc[1]]
        if val != -2 and self.interactive is False:
            val = ''

        if self.app.isopen:
            self.app.redraw(loc, val)
            self.app.update_idletasks()
            self.app.update()

    def explore_cell(self, x):
        [row, col] = x
        if self.is_known(x):
            cell = self.cells[row][col]
            nbor = self.known_neighbours([row, col])
            outer = self.outer_cells([row, col])
            if cell == nbor[2]:
                for k in nbor[0]:
                    self.set_cell_value(k, False)
                    self.explore_helper(k)
            elif (outer - nbor[1]) == cell:
                for l in nbor[0]:
                    self.add_mine_cells(l)
                    self.set_cell_value(l, True)

    def set_explored_cells(self):
        self.cells_explored = []
        row = 0
        while row < self.rows:
            col = 0
            while col < self.columns:
                if self.is_known([row, col]):
                    if len(self.known_neighbours([row, col])[0]) == 0:
                        pass
                    else:
                        self.cells_explored.append([row, col])
                col += 1
            row += 1

    def explore_cells(self):
        row = 0
        while row < self.rows:
            col = 0
            while col < self.columns:
                if self.is_known([row, col]):
                    cell = self.cells[row][col]
                    nbor = self.known_neighbours([row, col])
                    outer = self.outer_cells([row, col])
                    if cell == nbor[2]:
                        for k in nbor[0]:
                            self.set_cell_value(k, False)
                            self.explore_helper(k)
                    elif cell == (outer - nbor[1]):
                        for l in nbor[0]:
                            self.add_mine_cells(l)
                            self.set_cell_value(l, True)
                            self.explore_helper([l[0], l[1]])
                col += 1
            row += 1

    def repeat_func(self, x, y):
        self.add_mine_cells([x[0], x[1]])
        self.set_cell_value([x[0], x[1]], True)
        self.set_cell_value([y[0], y[1]], False)

    def solve_sets(self):
        second = []
        for k in self.cells_explored:
            for j in self.cells_explored:
                if k != j:
                    a = k
                    c = self.known_neighbours(a)
                    first = [tuple(i) for i in c[0]]
                    b = j
                    d = self.known_neighbours(b)
                    for y in d[0]:
                        second.append(tuple(y))
                    inter = set(first).intersection(second)
                    if len(inter) != 0:
                        if len(set(second) - set(first)) == 0 and len(first) > len(second):
                            d2 = abs(self.cells[b[0]][b[1]] - d[2] - self.cells[a[0]][a[1]] + c[2])
                            d1 = set(first) - set(second)
                            if d2 != 0:
                                if len(d1) == d2:
                                    for i in list(d1):
                                        self.add_mine_cells([i[0], i[1]])
                                        self.set_cell_value([i[0], i[1]], True)
                            else:
                                for i in list(d1):
                                    self.set_cell_value([i[0], i[1]], False)

                    if len(second) == len(first):
                        g = set(second) - inter
                        h = set(first) - inter
                        if len(g) == 1:
                            if len(h) == 1:
                                g = list(g)[0]
                                f = self.cells[g[0]][g[1]]
                                h = list(h)[0]
                                s = self.cells[h[0]][h[1]]
                                if abs(s - f) == 1:
                                    if f < s:
                                        self.repeat_func(h, g)
                                    else:
                                        self.repeat_func(g, h)

                    if len(set(first) - set(second)) == 0 and len(second) > len(first):
                        d1 = set(second) - set(first)
                        d2 = abs(self.cells[a[0]][a[1]] - c[2] - self.cells[b[0]][b[1]] + d[2])
                        if d2 != 0:
                            if len(d1) == d2:
                                for i in list(d1):
                                    self.add_mine_cells([i[0], i[1]])
                                    self.set_cell_value([i[0], i[1]], True)
                        else:
                            for i in list(d1):
                                self.set_cell_value([i[0], i[1]], False)

    def cells_changed(self):
        count = 0
        row = 0
        while row < self.rows:
            col = 0
            while col < self.columns:
                if self.cells[row][col] != 9:
                    count += 1
                col += 1
            row += 1
        return count

    def run(self):
        self.app.protocol("WM_DELETE_WINDOW", self.app.on_close)
        while not self.is_game_over() and not self.game_over:
            self.set_cell_value(self.choose_action(), False)
            cells_changed = self.cells_changed()
            self.repeat_task()
            while self.cells_changed() > cells_changed:
                cells_changed = self.cells_changed()
                self.repeat_task()

        if self.app.isopen:
            if self.interactive is True:
                self.app.endpopup("AI WINS!")

    def repeat_task(self):
        self.explore_cells()
        self.set_explored_cells()
        self.solve_sets()

    def is_game_over(self):
        row = 0
        while row < self.rows:
            if 9 in self.cells[row][:]:
                return False
            row += 1
        if self.interactive is True:
            print("AI WINS!")
        return True
