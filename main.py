from tkinter import Tk, BOTH, Canvas
import time
import random


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

    def __init__(
        self,
        walls,
        _x1,
        _y1,
        _x2,
        _y2,
        _win,
        _visited=False,
        wall_color="black",
        empty_wall_color="#f0f0f0",
    ):
        self.walls = walls
        self._x1 = _x1
        self._y1 = _y1
        self._x2 = _x2
        self._y2 = _y2
        self._win = _win
        self._visited = _visited
        self.wall_color = wall_color
        self.empty_wall_color = empty_wall_color

    def draw(self):
        cell_walls = [
            Line(Point(self._x1, self._y1), Point(self._x1, self._y2)),
            Line(Point(self._x2, self._y1), Point(self._x2, self._y2)),
            Line(Point(self._x1, self._y1), Point(self._x2, self._y1)),
            Line(Point(self._x1, self._y2), Point(self._x2, self._y2)),
        ]
        for i in range(len(self.walls)):
            self._win.draw_line(
                cell_walls[i],
                fill_color=self.wall_color if self.walls[i] else self.empty_wall_color,
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

    def break_wall_to(self, to_cell):
        # need to determine the wall that is shared between these two cells
        current_vertices = [
            (self._x1, self._y1),
            (self._x2, self._y1),
            (self._x2, self._y2),
            (self._x1, self._y2),
        ]
        next_vertices = [
            (to_cell._x1, to_cell._y1),
            (to_cell._x2, to_cell._y1),
            (to_cell._x2, to_cell._y2),
            (to_cell._x1, to_cell._y2),
        ]

        for v1 in current_vertices:
            for v2 in next_vertices:
                if v1 == v2:
                    line = Line(Point(v1[0], v1[1]), Point(v2[0], v2[1]))
                    line.draw(fill_color="white")


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
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)

    def _create_cells(self):
        all_cells = []
        walls = (1, 1, 1, 1)
        for col in range(self.num_cols):
            cell_col = []
            for row in range(self.num_rows):
                px1 = self.x1 + (row * self.cell_size_x)
                py1 = self.y1 + (col * self.cell_size_y)
                px2 = px1 + self.cell_size_x
                py2 = py1 + self.cell_size_y
                cell = Cell(walls, px1, py1, px2, py2, self.win)
                cell_col.append(cell)
            all_cells.extend([cell_col])
        self._cells = all_cells

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j].draw()

    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        top_left_cell = self._cells[0][0]
        bottom_right_cell = self._cells[self.num_cols - 1][self.num_rows - 1]
        top_left_cell.walls = (1, 1, 0, 1)
        bottom_right_cell.walls = (1, 1, 1, 0)
        top_left_cell.draw()
        bottom_right_cell.draw()

    def _break_walls_r(self, i, j):
        current_cell = self._cells[i][j]
        current_cell._visited = True
        moves = [(-1, 0), (0, -1), (1, 0), (0, 1)]

        while True:
            to_visit = []
            for m in range(len(moves)):
                possible_position_i = i + moves[m][0]
                possible_position_j = j + moves[m][1]

                if possible_position_i < 0 or possible_position_i > (self.num_cols - 1):
                    continue
                elif possible_position_j < 0 or possible_position_j > (
                    self.num_rows - 1
                ):
                    continue
                else:
                    to_visit.append((possible_position_i, possible_position_j))

            possible_locations_not_visited = [
                (i, j) for (i, j) in to_visit if not self._cells[i][j]._visited
            ]

            if len(possible_locations_not_visited) == 0:
                break

            random_index = random.randint(0, len(possible_locations_not_visited) - 1)
            next_location = possible_locations_not_visited[random_index]

            current_cell = self._cells[i][j]
            next_cell = self._cells[next_location[0]][next_location[1]]
            current_vertices = [
                (current_cell._x1, current_cell._y1),
                (current_cell._x2, current_cell._y1),
                (current_cell._x2, current_cell._y2),
                (current_cell._x1, current_cell._y2),
            ]
            next_vertices = [
                (next_cell._x1, next_cell._y1),
                (next_cell._x2, next_cell._y1),
                (next_cell._x2, next_cell._y2),
                (next_cell._x1, next_cell._y2),
            ]

            break_outer = False
            for i in range(len(current_vertices)):
                for j in range(len(next_vertices)):
                    if current_vertices[i] == next_vertices[j]:
                        new_walls = [1, 1, 1, 1]
                        new_walls[i] = 0
                        new_walls = tuple(new_walls)
                        current_cell.walls = new_walls
                        current_cell.draw()
                        break_outer = True
                        break
                if break_outer:
                    break

            self._break_walls_r(next_location[0], next_location[1])


def main():
    win = Window(800, 600)
    maze = Maze(10, 10, 10, 10, 50, 50, win)
    win.wait_for_close()


if __name__ == "__main__":
    main()
