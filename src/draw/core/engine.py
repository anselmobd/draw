import math
import re

__all__ = [
    "DrawEngine",
]


class DrawEngine:
    def __init__(self, renderer, delay_ms=0):
        self.renderer = renderer
        self.x, self.y = renderer.get_start_pos()
        self.scale = 4
        self.angle = 0
        self.color_index = 15
        self.delay = delay_ms / 1000.0

    def execute(self, draw_string):
        tokens = re.findall(r"([A-Za-z]+|[-+]?\d+[\s,]*[-+]?\d*|[-+]?\d+)", draw_string)

        i = 0
        while i < len(tokens):
            token = tokens[i].upper().strip()

            blind = False
            noupdate = False
            if "B" in token:
                blind = True
                token = token.replace("B", "")
            if "N" in token:
                noupdate = True
                token = token.replace("N", "")

            if not token and i + 1 < len(tokens):
                i += 1
                next_tok = tokens[i].upper()
                if "B" in next_tok:
                    blind = True
                if "N" in next_tok:
                    noupdate = True
                token = re.sub(r"[BN]", "", next_tok)

            arg = ""
            if i + 1 < len(tokens) and re.match(r"^[-+]?\d+", tokens[i + 1]):
                i += 1
                arg = tokens[i].strip()

            if token in ["U", "D", "L", "R", "E", "F", "G", "H", "M"]:
                self._move_command(token, arg, blind, noupdate)
            elif token == "C":
                self.color_index = int(arg) if arg else 15
                self.renderer.set_color(self.color_index)
            elif token == "S":
                self.scale = int(arg) if arg else 4
            elif token == "A":
                self.angle = (int(arg) if arg else 0) * 90
            elif token == "TA":
                self.angle = float(arg) if arg else 0.0

            i += 1
            if self.delay > 0:
                self.renderer.wait(self.delay)

    def execute_file(self, file_path):
        try:
            with open(file_path, "r") as f:
                content = " ".join(
                    [
                        line.strip()
                        for line in f
                        if line.strip() and not line.startswith("#")
                    ]
                )
                self.execute(content)
        except FileNotFoundError:
            print(f"Erro: Arquivo '{file_path}' não encontrado.")

    def _move_command(self, cmd, arg, blind, noupdate):
        dist = float(arg) * (self.scale / 4.0) if arg and cmd != "M" else 0

        dx, dy = 0, 0
        if cmd == "U":
            dy = -dist
        elif cmd == "D":
            dy = dist
        elif cmd == "L":
            dx = -dist
        elif cmd == "R":
            dx = dist
        elif cmd == "E":
            dx, dy = dist, -dist
        elif cmd == "F":
            dx, dy = dist, dist
        elif cmd == "G":
            dx, dy = -dist, dist
        elif cmd == "H":
            dx, dy = -dist, -dist
        elif cmd == "M":
            is_relative = "+" in arg or "-" in arg
            coords = [c.strip() for c in arg.split(",")]
            if len(coords) == 2:
                mx, my = float(coords[0]), float(coords[1])
                if is_relative:
                    dx, dy = mx * (self.scale / 4.0), my * (self.scale / 4.0)
                else:
                    self._do_draw(mx, my, blind, noupdate)
                    return

        if self.angle != 0 and cmd != "M":
            rad = math.radians(-self.angle)
            rx = dx * math.cos(rad) - dy * math.sin(rad)
            ry = dx * math.sin(rad) + dy * math.cos(rad)
            dx, dy = rx, ry

        self._do_draw(self.x + dx, self.y + dy, blind, noupdate)

    def _do_draw(self, nx, ny, blind, noupdate):
        target_x, target_y = nx, ny

        # Em renderizadores que trabalham com grid discreto (ex: Console, Tkinter),
        # arredondar as coordenadas antes de desenhar garante que os renderizadores
        # recebam pontos exatos, evitando gaps em vértices e mantendo a simetria.
        if self.renderer.is_discrete:
            target_x = float(math.floor(nx + 0.5))
            target_y = float(math.floor(ny + 0.5))

        if not blind:
            self.renderer.draw_line(self.x, self.y, target_x, target_y)

        if not noupdate:
            self.x = target_x
            self.y = target_y
