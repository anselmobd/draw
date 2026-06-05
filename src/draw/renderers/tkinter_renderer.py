import tkinter as tk
import time


class TkinterRenderer:
    def __init__(
        self, title="Interpretador Clássico do Comando DRAW", width=640, height=480
    ):
        self.root = tk.Tk()
        self.root.title(title)
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg="black")
        self.canvas.pack()
        self.color_index = 15
        self.colors = {
            0: "black",
            1: "blue",
            2: "green",
            3: "cyan",
            4: "red",
            5: "magenta",
            6: "brown",
            7: "lightgray",
            8: "darkgray",
            9: "lightblue",
            10: "lightgreen",
            11: "lightcyan",
            12: "pink",
            13: "purple",
            14: "yellow",
            15: "white",
        }

    def get_start_pos(self):
        return self.width // 2, self.height // 2

    def set_color(self, index):
        self.color_index = index

    def draw_line(self, x1, y1, x2, y2):
        color = self.colors.get(self.color_index, "white")
        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=1)

    def wait(self, seconds):
        self.root.update()
        time.sleep(seconds)

    def wait_for_exit(self):
        self.root.mainloop()

    def finalize(self):
        pass
