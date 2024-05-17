from tkinter import Tk, BOTH, Canvas
import sys
import time
import random
from typing import Dict, List


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

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

    def __init__(
        self,
        walls: Dict[str, bool],
        _x1,
        _y1,
        _x2,
        _y2,
        _win,
        _visited=False,
        active_wall_color="black",
        inactive_wall_color="white",
    ):
        self.walls = walls
        self._x1 = _x1
        self._y1 = _y1
        self._x2 = _x2
        self._y2 = _y2
        self._win = _win
        self._visited = _visited
        self.active_wall_color = active_wall_color
        self.inactive_wall_color = inactive_wall_color
        self._walls = {
            "left": Line(Point(self._x1, self._y1), Point(self._x1, self._y2)),
            "right": Line(Point(self._x2, self._y1), Point(self._x2, self._y2)),
            "top": Line(Point(self._x1, self._y1), Point(self._x2, self._y1)),
            "bottom": Line(Point(self._x1, self._y2), Point(self._x2, self._y2)),
        }

    def __repr__(self):
        return f"<Cell: wall: {self.walls} p1: ({self._x1}, {self._y1}) p2: ({self._x2}, {self._y2})"

    def draw(self):
        for direction, has_wall in self.walls.items():
            self._win.draw_line(
                self._walls[direction],
                fill_color=self.active_wall_color
                if has_wall
                else self.inactive_wall_color,
            )

    def draw_move(self, to_cell, undo=False):
        origin_cell_center = Point(
            self._x1 + ((self._x2 - self._x1) / 2),
            self._y1 + ((self._y2 - self._y1) / 2),
        )
        to_cell_center = Point(
            to_cell._x1 + ((to_cell._x2 - to_cell._x1) / 2),
            to_cell._y1 + ((to_cell._y2 - to_cell._y1) / 2),
        )
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

        print(
            f"""creating maze:
                x,y: ({self.x1}, {self.y1})
                {self.num_rows} rows
                {self.num_cols} cols
                {self.cell_size_x} X cell size
                {self.cell_size_y} Y cell size"""
        )

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)

    def _create_cells(self):
        all_cells = []
        for col in range(self.num_cols):
            cell_col = []
            for row in range(self.num_rows):
                px1 = self.x1 + (col * self.cell_size_x)
                py1 = self.y1 + (row * self.cell_size_y)
                px2 = px1 + self.cell_size_x
                py2 = py1 + self.cell_size_y
                cell = Cell(
                    {"right": True, "left": True, "top": True, "bottom": True},
                    px1,
                    py1,
                    px2,
                    py2,
                    self.win,
                )
                cell_col.append(cell)
            all_cells.append(cell_col)

        self._cells = all_cells

        for j in range(self.num_rows):
            for i in range(self.num_cols):
                self._cells[i][j].draw()

    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        entrance_cell = self._cells[0][0]
        exit_cell = self._cells[self.num_cols - 1][self.num_rows - 1]
        entrance_cell.walls["top"] = False
        exit_cell.walls["bottom"] = False
        entrance_cell.draw()
        exit_cell.draw()

    def _break_walls_r(self, i, j):
        current_cell = self._cells[i][j]
        current_cell._visited = True

        while True:
            to_visit = []
            # left
            if i > 0 and not self._cells[i - 1][j]._visited:
                to_visit.append((i - 1, j))
            # right
            if i < self.num_cols - 1 and not self._cells[i + 1][j]._visited:
                to_visit.append((i + 1, j))
            # up
            if j > 0 and not self._cells[i][j - 1]._visited:
                to_visit.append((i, j - 1))
            # down
            if j < self.num_rows - 1 and not self._cells[i][j + 1]._visited:
                to_visit.append((i, j + 1))

            if len(to_visit) == 0:
                self._cells[i][j].draw()
                return

            next_location = random.choice(to_visit)

            next_cell = self._cells[next_location[0]][next_location[1]]

            # break the call between the current cell and next cell
            # note that in order to do this correctly we will have to erase the
            # wall for both the current and the next cell
            # right
            if next_location[0] == i + 1:
                current_cell.walls["right"] = False
                next_cell.walls["left"] = False
            # left
            if next_location[0] == i - 1:
                current_cell.walls["left"] = False
                next_cell.walls["right"] = False
            # up
            if next_location[1] == j - 1:
                current_cell.walls["top"] = False
                next_cell.walls["bottom"] = False
            # down
            if next_location[1] == j + 1:
                current_cell.walls["bottom"] = False
                next_cell.walls["top"] = False

            self._break_walls_r(next_location[0], next_location[1])


def main():
    if len(sys.argv) == 1:
        rows = 5
        cols = 5
    else:
        rows = int(sys.argv[1])
        cols = int(sys.argv[2])
    win = Window(800, 600)
    Maze(10, 10, rows, cols, 50, 50, win)
    win.wait_for_close()


if __name__ == "__main__":
    main()
