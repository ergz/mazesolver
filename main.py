from tkinter import Tk, BOTH, Canvas
import sys
import time
import random


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
        self._walls = {
            "left": Line(Point(self._x1, self._y1), Point(self._x1, self._y2)),
            "right": Line(Point(self._x2, self._y1), Point(self._x2, self._y2)),
            "top": Line(Point(self._x1, self._y1), Point(self._x2, self._y1)),
            "bottom": Line(Point(self._x1, self._y2), Point(self._x2, self._y2)),
        }

    def __repr__(self):
        return f"<Cell: wall: {self.walls} p1: ({self._x1}, {self._y1}) p2: ({self._x2}, {self._y2})"

    def draw(self):
        wall_lines = list(self._walls.values())
        for i in range(len(self.walls)):
            self._win.draw_line(
                wall_lines[i],
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

    def get_wall_to_break(self, target):
        for w_dir, w in self._walls.items():
            for v_dir, v in target._walls.items():
                if w.p1 == v.p1 and w.p2 == v.p2:
                    print(f"(get_cell_to_break): {w.p1} == {v.p1} and {w.p2} == {v.p2}")
                    print(f"(get_cell_to_break): Corresponds to wall: {w_dir}")
                    return w_dir


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
        walls = [1, 1, 1, 1]
        for col in range(self.num_cols):
            cell_col = []
            for row in range(self.num_rows):
                px1 = self.x1 + (col * self.cell_size_x)
                py1 = self.y1 + (row * self.cell_size_y)
                px2 = px1 + self.cell_size_x
                py2 = py1 + self.cell_size_y
                cell = Cell(walls, px1, py1, px2, py2, self.win)
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
        top_left_cell = self._cells[0][0]
        bottom_right_cell = self._cells[self.num_cols - 1][self.num_rows - 1]
        top_left_cell.walls = [1, 1, 0, 1]
        bottom_right_cell.walls = [1, 1, 1, 0]
        top_left_cell.draw()
        bottom_right_cell.draw()

    def _break_walls_r(self, i, j):
        current_cell = self._cells[i][j]
        print("-----------------------------")
        print(f"at location: {i},{j}")
        current_cell._visited = True
        # moves: left (-1, 0), up (0, -1), right (1, 0), down (0, 1)
        moves = [(-1, 0), (0, -1), (1, 0), (0, 1)]

        while True:
            to_visit = []
            for move in moves:
                possible_position_i = i + move[0]
                possible_position_j = j + move[1]

                # Ensure the possible positions are within the bounds of the grid
                if (
                    0 <= possible_position_i < self.num_cols
                    and 0 <= possible_position_j < self.num_rows
                ):
                    to_visit.append((possible_position_i, possible_position_j))

            possible_locations_not_visited = list(
                filter(lambda pos: not self._cells[pos[0]][pos[1]]._visited, to_visit)
            )
            print(f"possible locations: {possible_locations_not_visited}")

            # If there are no unvisited adjacent cells, backtrack
            if len(possible_locations_not_visited) == 0:
                print("the length of possible locations is zero **returning**")
                current_cell.draw()
                return

            # Randomly choose the next cell to visit
            next_location = random.choice(possible_locations_not_visited)
            print(f"Next Cell: {self._cells[next_location[0]][next_location[1]]}")

            next_cell = self._cells[next_location[0]][next_location[1]]
            wall_to_break = current_cell.get_wall_to_break(next_cell)
            directions = ["left", "right", "top", "bottom"]
            idx = directions.index(wall_to_break)
            current_cell.walls[idx] = 0
            current_cell.draw()

            self._break_walls_r(next_location[0], next_location[1])

            # Check if the next location is the end of the maze
            if (
                next_location[0] == self.num_cols - 1
                and next_location[1] == self.num_rows - 1
            ):
                print("reached the end of the puzzle, returning")
                return


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
