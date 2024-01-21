from tkinter import Tk, BOTH, Canvas


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class Line:
    def __init__(self, point_a: Point, point_b: Point) -> None:
        self.point_a = point_a
        self.point_b = point_b

    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(
            self.point_a.x,
            self.point_a.y,
            self.point_b.x,
            self.point_b.y,
            fill=fill_color,
            width=2,
        )
        canvas.pack(fill=BOTH, expand=1)


class Window:
    def __init__(self, width, height) -> None:
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, width=width, height=height, background="white")
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def draw_line(self, line: Line, fill_color: str = "black"):
        line.draw(self.__canvas, fill_color)

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False
