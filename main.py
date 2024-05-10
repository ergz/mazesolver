from tkinter import Tk, BOTH, Canvas


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point<x:{self.x}, y:{self.y}>"


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )


class Cell:
    """
    Cell

    Creates a Cell starting a point (_x1, _y1) to (_x2, _y2). The lines are drawn with
    color specified in `fill_color` this is black by default. Walls for the cell can added
    by passing in a tuple for `wall`, the indices in this represent `(left, right, top, bottom)`.

    """

    def __init__(self, walls, _x1, _y1, _x2, _y2, _win, fill_color="black"):
        self.walls = walls
        self._x1 = _x1
        self._y1 = _y1
        self._x2 = _x2
        self._y2 = _y2
        self._win = _win
        self.fill_color = fill_color

    def draw(self):
        if self.walls[0]:
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            self._win.draw_line(line, fill_color=self.fill_color)
        if self.walls[1]:
            line = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            self._win.draw_line(line, fill_color=self.fill_color)
        if self.walls[2]:
            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            self._win.draw_line(line, fill_color=self.fill_color)
        if self.walls[3]:
            line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            self._win.draw_line(line, fill_color=self.fill_color)

    def draw_move(self, to_cell, undo=False):
        origin_cell_center = Point(
            self._x1 + ((self._x2 - self._x1) / 2),
            self._y1 + ((self._y2 - self._y1) / 2),
        )
        print(f"the origin cell: {origin_cell_center}")
        to_cell_center = Point(
            to_cell._x1 + ((to_cell._x2 - to_cell._x1) / 2),
            to_cell._y1 + ((to_cell._y2 - to_cell._y1) / 2),
        )
        print(f"to cell: {to_cell_center}")
        line = Line(origin_cell_center, to_cell_center)
        fill_color = "grey" if undo else "red"
        self._win.draw_line(line, fill_color=fill_color)


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.__root = Tk(screenName="Hello world")
        self.canvas = Canvas(height=self.height, width=self.width)
        self.is_running = False
        self.canvas.pack()
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.canvas, fill_color=fill_color)

    def wait_for_close(self):
        self.is_running = True
        while self.is_running:
            self.redraw()

    def close(self):
        self.is_running = False


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        self._create_cells()

    def _create_cells(self):
        all_cells = []
        walls = (1, 1, 1, 1)
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                px1 = self.x1 + (row * self.cell_size_x)
                py1 = self.y1 + (col * self.cell_size_y)
                px2 = px1 + self.cell_size_x
                py2 = py1 + self.cell_size_y
                cell = Cell(walls, px1, py1, px2, py2, self.win)
                all_cells.append(cell)
        self._cells = all_cells

        for i in range(len(self._cells)):
            self._cells[i].draw()


def main():
    win = Window(800, 600)
    maze = Maze(10, 10, 10, 10, 50, 50, win)
    win.wait_for_close()


if __name__ == "__main__":
    main()
