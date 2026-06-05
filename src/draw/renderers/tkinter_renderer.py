import tkinter as tk
import time


class TkinterRenderer:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.root = canvas.winfo_toplevel()
        self.width = width
        self.height = height
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
