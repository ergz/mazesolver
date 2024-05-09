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
    def __init__(self):
        ...


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


def main():
    win = Window(800, 600)
    line = Line(Point(0, 0), Point(100, 100))
    line2 = Line(Point(110, 110), Point(100, 100))
    line3 = Line(Point(130, 50), Point(100, 100))
    win.draw_line(line, "red")
    win.draw_line(line2, "blue")
    win.draw_line(line3, "green")
    win.wait_for_close()


if __name__ == "__main__":
    main()
