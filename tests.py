import unittest
from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._cells), num_cols)
        self.assertEqual(len(m1._cells[0]), num_rows)

    def test_maze_create_cells2(self):
        num_cols = 1
        num_rows = 123
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._cells), num_cols)
        self.assertEqual(len(m1._cells[0]), num_rows)

    def test_maze_create_cells3(self):
        num_cols = 1
        num_rows = 1
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._cells), num_cols)
        self.assertEqual(len(m1._cells[0]), num_rows)

    def test_reset_cells_visited(self):
        num_cols = 10
        num_rows = 10
        m1 = Maze(0, 1, num_rows, num_cols, 10, 10)
        visited_cells = 0
        for i in range(0, num_cols):
            for j in range(0, num_rows):
                if m1._cells[i][j].visited: visited_cells += 1
        self.assertEqual(visited_cells, 0)


if __name__ == "__main__":
    unittest.main()
