import tkinter as tk
import time
import json
import os
import math
from draw.renderers.base import Renderer


class TkinterRenderer(Renderer):
    def __init__(
        self,
        title="Interpretador Clássico do Comando DRAW",
        width=640,
        height=480,
        window_mode="normal",
        headless=False,
        pixel_size=(1, 1),
    ):
        super().__init__(pixel_size=pixel_size)
        self.window_mode = window_mode
        self.root = tk.Tk()
        if headless:
            self.root.withdraw()
        self.root.title(title)
        self.alive = True

        # Aplica o modo de janela antes de carregar posição salva
        if self.window_mode == "fullscreen":
            self.root.attributes("-fullscreen", True)
        elif self.window_mode == "maximized":
            if os.name == "nt":
                self.root.state("zoomed")
            else:
                self.root.attributes("-zoomed", True)

        self.width = width
        self.height = height

        # Se estiver em tela cheia, atualizamos a largura e altura para as do monitor
        if self.window_mode in ["fullscreen", "maximized"]:
            self.root.update()  # Garante que as dimensões foram aplicadas
            self.width = self.root.winfo_width()
            self.height = self.root.winfo_height()

        # Arquivo para salvar o estado da janela
        self.config_file = os.path.join(os.getcwd(), ".draw_config.json")
        if self.window_mode == "normal":
            self._load_window_state()

        self.canvas = tk.Canvas(
            self.root,
            width=self.width,
            height=self.height,
            bg="black",
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)
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

        self._resize_timer = None
        self.root.bind("<Configure>", self._on_window_configure)

    def _on_window_configure(self, event):
        """Manipula o redimensionamento da janela com debounce."""
        # Filtra eventos internos (o canvas disparando configure no root etc)
        if event.widget != self.root:
            return

        # Só reage se as dimensões realmente mudaram significativamente
        if event.width == self.width and event.height == self.height:
            return

        self.width = event.width
        self.height = event.height

        # Debounce: cancela o timer anterior e inicia um novo
        if self._resize_timer:
            self.root.after_cancel(self._resize_timer)

        # Chama o callback após 100ms de inatividade
        self._resize_timer = self.root.after(100, self._trigger_resize)

    def _trigger_resize(self):
        if self.on_resize_callback and self.alive:
            self.on_resize_callback()

    def is_alive(self) -> bool:
        return self.alive

    def get_start_pos(self):
        w, h = self.get_resolution()
        return w // 2, h // 2

    def get_resolution(self):
        pw, ph = self.pixel_size
        return self.width // pw, self.height // ph

    @property
    def is_discrete(self) -> bool:
        return True

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
        if not self.alive:
            return
        color = self.colors.get(self.color_index, "white")
        pw, ph = self.pixel_size

        # Se o pixel for 1x1, usamos a linha padrão (mais eficiente)
        if pw == 1 and ph == 1:
            try:
                # Usamos capstyle=PROJECTING para garantir que os pixels de extremidade sejam pintados
                # em linhas de 1 pixel de largura, evitando gaps em vértices de diagonais.
                self.canvas.create_line(
                    x1, y1, x2, y2, fill=color, width=1, capstyle=tk.PROJECTING
                )
            except tk.TclError:
                self.alive = False
            return

        # Para pixels maiores, simulamos a linha desenhando "blocos" ao longo da trajetória
        # usando Bresenham para consistência com o motor.
        x1_i, y1_i = int(math.floor(x1 + 0.5)), int(math.floor(y1 + 0.5))
        x2_i, y2_i = int(math.floor(x2 + 0.5)), int(math.floor(y2 + 0.5))

        dx = abs(x2_i - x1_i)
        dy = abs(y2_i - y1_i)
        sx = 1 if x1_i < x2_i else -1
        sy = 1 if y1_i < y2_i else -1
        err = dx - dy

        cx, cy = x1_i, y1_i
        while self.alive:
            try:
                # Desenha o "pixel gigante"
                # (cx, cy) são as coordenadas lógicas. Multiplicamos pelo tamanho do pixel.
                self.canvas.create_rectangle(
                    cx * pw,
                    cy * ph,
                    (cx + 1) * pw,
                    (cy + 1) * ph,
                    fill=color,
                    outline="",
                )
            except tk.TclError:
                self.alive = False
                break

            if cx == x2_i and cy == y2_i:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                cx += sx
            if e2 < dx:
                err += dx
                cy += sy

    def wait(self, seconds):
        if not self.alive:
            return
        try:
            self.root.update()
            time.sleep(seconds)
        except tk.TclError:
            self.alive = False

    def wait_for_exit(self):
        """Aguardar as teclas Espaço ou Enter para sair da aplicação."""
        if not self.alive:
            return

        try:
            self.root.protocol("WM_DELETE_WINDOW", self._on_exit)
            # Vincula apenas as teclas solicitadas (Enter e Espaço)
            self.root.bind("<space>", self._on_exit)
            self.root.bind("<Return>", self._on_exit)
            self.root.mainloop()
        except (tk.TclError, KeyboardInterrupt):
            self.alive = False

    def _on_exit(self, event=None):
        if self.alive:
            self.alive = False
            self._save_window_state()
            try:
                self.root.destroy()
            except tk.TclError:
                pass

    def finalize(self):
        """Garante o fechamento da janela ao finalizar."""
        self._on_exit()
