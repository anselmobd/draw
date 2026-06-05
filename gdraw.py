import argparse
import sys
import tkinter as tk
import time
from engine import DrawEngine, carregar_do_arquivo

class TkinterRenderer:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.root = canvas.winfo_toplevel()
        self.width = width
        self.height = height
        self.color_index = 15
        self.colors = {
            0: "black", 1: "blue", 2: "green", 3: "cyan", 4: "red", 5: "magenta", 6: "brown", 7: "lightgray",
            8: "darkgray", 9: "lightblue", 10: "lightgreen", 11: "lightcyan", 12: "pink", 13: "purple", 14: "yellow", 15: "white",
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

# --- Inicialização da Interface Gráfica ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interpretador DRAW Gráfico")
    parser.add_argument("command", type=str, nargs="?", help="Executa uma string de comandos DRAW")
    parser.add_argument("-f", "--file", type=str, help="Executa comandos DRAW de um arquivo")
    parser.add_argument("-t", "--test", action="store_true", help="Executa o teste padrão")
    parser.add_argument("-s", "--slow", type=int, default=0, help="Atraso entre comandos (milisegundos)")

    args = parser.parse_args()

    if not (args.command or args.file or args.test):
        parser.print_help()
        sys.exit(0)

    root = tk.Tk()
    root.title("Interpretador Clássico do Comando DRAW")

    canvas_width, canvas_height = 640, 480
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="black")
    canvas.pack()

    renderer = TkinterRenderer(canvas, canvas_width, canvas_height)
    engine = DrawEngine(renderer, delay_ms=args.slow)

    if args.test:
        string_teste = "C4 U40 R40 D40 L40 BM +60,+60 C14 TA45 U40 R40 D40 L40"
        engine.execute(string_teste)
        carregar_do_arquivo("desenho.txt", engine)

    if args.command:
        engine.execute(args.command)

    if args.file:
        carregar_do_arquivo(args.file, engine)

    root.mainloop()
