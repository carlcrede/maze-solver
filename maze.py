import time, random
from cell import Cell
from graphics import Window
from typing import List


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        window=None,
        seed=None,
    ) -> None:
        if seed:
            random.seed(seed)
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._window: Window = window
        self._cells: List[List[Cell]] = []
        self._create_cells()
        self._break_entrance_and_exit()
        # self._break_walls_r(0, 0)
        self._break_walls_i(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._window))
            self._cells.append(col_cells)

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i: int, j: int):
        if self._window is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        # self._animate()

    def _animate(self, secs: float = 0.025):
        if self._window is None:
            return
        self._window.redraw()
        time.sleep(secs)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(0, 0)
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_wall(self, i, j, direction):
        if direction == "left":
            self._cells[i][j].has_left_wall = False
        if direction == "top":
            self._cells[i][j].has_top_wall = False
        if direction == "right":
            self._cells[i][j].has_right_wall = False
        if direction == "bottom":
            self._cells[i][j].has_bottom_wall = False

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        while True:
            possible_cells_to_visit = []

            # check left
            if not i == 0:
                if not (self._cells[i - 1][j].visited):
                    possible_cells_to_visit.append(((i - 1, j), "left"))

            # check top
            if not i == 0 and not j == 0:
                if not (self._cells[i][j - 1].visited):
                    possible_cells_to_visit.append(((i, j - 1), "top"))

            # check right
            if not i == (self._num_cols - 1):
                if not (self._cells[i + 1][j].visited):
                    possible_cells_to_visit.append(((i + 1, j), "right"))

            # check bottom
            if not j == (self._num_rows - 1):
                if not (self._cells[i][j + 1].visited):
                    possible_cells_to_visit.append(((i, j + 1), "bottom"))

            if len(possible_cells_to_visit) == 0:
                self._draw_cell(i, j)
                break

            next_cell, direction = possible_cells_to_visit[
                random.randint(0, len(possible_cells_to_visit) - 1)
            ]

            # Knock down the walls between the current cell and the chosen cell.
            if direction == "left":
                self._cells[i][j].has_left_wall = False
            if direction == "top":
                self._cells[i][j].has_top_wall = False
            if direction == "right":
                self._cells[i][j].has_right_wall = False
            if direction == "bottom":
                self._cells[i][j].has_bottom_wall = False

            self._break_walls_r(i=next_cell[0], j=next_cell[1])

    def _break_walls_i(self, i, j):
        stack = [(i, j)]

        while stack:
            i, j = stack[-1]
            self._cells[i][j].visited = True
            possible_cells_to_visit = []

            # check left
            if i > 0 and not self._cells[i - 1][j].visited:
                possible_cells_to_visit.append(((i - 1, j), "left"))

            # check top
            if j > 0 and not self._cells[i][j - 1].visited:
                possible_cells_to_visit.append(((i, j - 1), "top"))

            # check right
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                possible_cells_to_visit.append(((i + 1, j), "right"))

            # check bottom
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                possible_cells_to_visit.append(((i, j + 1), "bottom"))

            if possible_cells_to_visit:
                next_cell, direction = random.choice(possible_cells_to_visit)
                self._break_wall(i, j, direction)
                stack.append(next_cell)
            else:
                self._draw_cell(i, j)
                stack.pop()

    def _reset_cells_visited(self):
        for i in range(0, self._num_cols):
            for j in range(0, self._num_rows):
                self._cells[i][j].visited = False

    def solve(self, alg) -> bool:
        if alg == "recursive":
            return self._solve_r(i=0, j=0)

        if alg == "iterative":
            return self._solve_i(0, 0)

    def _solve_r(self, i, j) -> bool:
        # self._animate()

        self._cells[i][j].visited = True

        if i == (self._num_cols - 1) and j == (self._num_rows - 1):
            return True

        # check left
        if (
            i > 0
            and not self._cells[i][j].has_left_wall
            and not self._cells[i - 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            solved = self._solve_r(i=i - 1, j=j)
            if solved:
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], undo=True)

        # check top
        if (
            j > 0
            and not self._cells[i][j].has_top_wall
            and not self._cells[i][j - 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            solved = self._solve_r(i=i, j=j - 1)
            if solved:
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], undo=True)

        # check right
        if (
            i < self._num_cols - 1
            and not self._cells[i][j].has_right_wall
            and not self._cells[i + 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            solved = self._solve_r(i=i + 1, j=j)
            if solved:
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], undo=True)

        # check bottom
        if (
            j < self._num_rows - 1
            and not self._cells[i][j].has_bottom_wall
            and not self._cells[i][j + 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            solved = self._solve_r(i=i, j=j + 1)
            if solved:
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], undo=True)

        return False

    def _solve_i(self, i, j) -> bool:
        stack = [(i, j)]

        while stack:
            i, j = stack[-1]
            # self._animate(secs=.000001)
            self._cells[i][j].visited = True

            if i == (self._num_cols - 1) and j == (self._num_rows - 1):
                return True

            directions = [
                ((-1, 0), "has_left_wall", "draw_move"),
                ((0, -1), "has_top_wall", "draw_move"),
                ((1, 0), "has_right_wall", "draw_move"),
                ((0, 1), "has_bottom_wall", "draw_move"),
            ]

            for direction, wall, _ in directions:
                di, dj = direction
                ni, nj = i + di, j + dj
                if (
                    0 <= ni < self._num_cols
                    and 0 <= nj < self._num_rows
                    and not getattr(self._cells[i][j], wall)
                    and not self._cells[ni][nj].visited
                ):
                    self._cells[i][j].draw_move(self._cells[ni][nj])
                    stack.append((ni, nj))
                    break
            else:
                i, j = stack.pop()
                if stack:
                    self._cells[i][j].draw_move(
                        self._cells[stack[-1][0]][stack[-1][1]], undo=True
                    )

        return False
