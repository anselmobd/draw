import tkinter as tk
import time
import json
import os
from draw.renderers.base import Renderer


class TkinterRenderer(Renderer):
    def __init__(
        self, title="Interpretador Clássico do Comando DRAW", width=640, height=480
    ):
        self.root = tk.Tk()
        self.root.title(title)
        self.width = width
        self.height = height

        # Arquivo para salvar o estado da janela
        self.config_file = os.path.join(os.getcwd(), ".draw_config.json")
        self._load_window_state()

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

    def _load_window_state(self):
        """Carrega a posição da janela do arquivo de configuração e valida se está visível."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                    pos = config.get("window_position")
                    if pos:
                        x, y = int(pos["x"]), int(pos["y"])

                        # Validação básica para garantir que a janela não abra "fora" da tela
                        # (Ex: após desconectar um monitor)
                        screen_w = self.root.winfo_screenwidth()
                        screen_h = self.root.winfo_screenheight()

                        # Se a posição salva estiver muito fora dos limites atuais, ignora
                        if 0 <= x < screen_w - 50 and 0 <= y < screen_h - 50:
                            self.root.geometry(f"+{x}+{y}")
            except (json.JSONDecodeError, IOError, ValueError):
                pass

    def _save_window_state(self):
        """Salva a posição atual da janela."""
        try:
            # geometry() retorna string 'WIDTHxHEIGHT+X+Y'
            geo = self.root.geometry()
            parts = geo.split("+")
            if len(parts) >= 3:
                x, y = parts[1], parts[2]
                config = {"window_position": {"x": x, "y": y}}
                with open(self.config_file, "w") as f:
                    json.dump(config, f)
        except Exception:
            pass

    def set_color(self, index):
        self.color_index = index

    def limpar_tela(self):
        self.canvas.delete("all")

    def draw_line(self, x1, y1, x2, y2):
        color = self.colors.get(self.color_index, "white")
        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=1)

    def wait(self, seconds):
        self.root.update()
        time.sleep(seconds)

    def wait_for_exit(self):
        # Fecha a janela ao pressionar qualquer tecla
        def on_exit(event=None):
            self._save_window_state()
            self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", on_exit)
        self.root.bind("<Key>", on_exit)
        self.root.mainloop()

    def finalize(self):
        pass
