from graphics import Window, Line, Point


class Cell:
    def __init__(
        self,
        window: Window | None = None,
    ) -> None:
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self.__window = window
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        if self.__window is None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2

        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self.__window.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x1, y2))
            self.__window.draw_line(line, "white")
        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self.__window.draw_line(line)
        else:
            line = Line(Point(x2, y1), Point(x2, y2))
            self.__window.draw_line(line, "white")
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self.__window.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x2, y1))
            self.__window.draw_line(line, "white")
        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self.__window.draw_line(line)
        else:
            line = Line(Point(x1, y2), Point(x2, y2))
            self.__window.draw_line(line, "white")

    def draw_move(self, to_cell: "Cell", undo=False):
        if self.__window is None:
            return
        center_point = lambda cell: Point(
            cell._x1 + abs(cell._x1 - cell._x2) / 2,
            cell._y1 + abs(cell._y1 - cell._y2) / 2,
        )

        source_point = center_point(self)
        target_point = center_point(to_cell)

        fill_color = "gray" if undo else "red"

        self.__window.draw_line(Line(source_point, target_point), fill_color)
