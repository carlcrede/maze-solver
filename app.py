from graphics import Window
from maze import Maze

if __name__ == "__main__":
    window = Window(1920, 1080)

    margin = 50

    maze1 = Maze(
        x1=margin,
        y1=margin,
        num_rows=100,
        num_cols=100,
        cell_size_x=10,
        cell_size_y=10,
        window=window,
    )

    solved = maze1.solve(alg='iterative')

    window.wait_for_close()
