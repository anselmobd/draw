import math
import re

__all__ = [
    "DrawEngine",
]


class DrawEngine:
    def __init__(self, renderer, delay_ms=0):
        self.renderer = renderer
        self.renderer.set_on_resize(self.redraw)
        self.initial_renderer_state = {"start_pos": renderer.get_start_pos()}
        self.x, self.y = self.initial_renderer_state["start_pos"]
        self.scale = 4
        self.angle = 0
        self.color_index = 15
        self.delay = delay_ms / 1000.0
        self.command_history = []
        self._is_running = False
        self._run_id = 0
        self.commands_info = {
            "U": "Move para Cima (Up) n unidades.",
            "D": "Move para Baixo (Down) n unidades.",
            "L": "Move para a Esquerda (Left) n unidades.",
            "R": "Move para a Direita (Right) n unidades.",
            "E": "Move para o Nordeste (diagonal cima-direita) n unidades.",
            "F": "Move para o Sudeste (diagonal baixo-direita) n unidades.",
            "G": "Move para o Sudoeste (diagonal baixo-esquerda) n unidades.",
            "H": "Move para o Noroeste (diagonal cima-esquerda) n unidades.",
            "M x,y": "Move para coordenada absoluta (x,y) ou relativa (+x,+y).",
            "C n": "Define a cor atual (índice 0-15).",
            "S n": "Define a escala do desenho (padrão 4).",
            "A n": "Rotaciona em múltiplos de 90 graus (n=0 a 3).",
            "TA n": "Rotaciona em um ângulo arbitrário (0-359 graus).",
            "B": "Prefixo: Move sem desenhar (Blind).",
            "N": "Prefixo: Desenha sem atualizar a posição final (No Update).",
        }
        self.colors_info = {
            0: "Preto",
            1: "Azul",
            2: "Verde",
            3: "Ciano",
            4: "Vermelho",
            5: "Magenta",
            6: "Marrom / Amarelo Escuro",
            7: "Cinza Claro",
            8: "Cinza Escuro",
            9: "Azul Claro",
            10: "Verde Claro",
            11: "Ciano Claro",
            12: "Vermelho Claro",
            13: "Magenta Claro",
            14: "Amarelo",
            15: "Branco",
        }

    def get_help_text(self):
        """Retorna uma string formatada com a ajuda de todos os comandos DRAW."""
        help_lines = ["\nComandos DRAW Disponíveis:", "=" * 30]
        for cmd, desc in self.commands_info.items():
            help_lines.append(f"  {cmd.ljust(8)} : {desc}")

        help_lines.append("\nPaleta de Cores (C n):")
        help_lines.append("=" * 30)
        # Organiza as cores em colunas para economizar espaço vertical
        for i in range(0, 16, 2):
            c1 = f"{i}: {self.colors_info[i]}"
            c2 = f"{i + 1}: {self.colors_info[i + 1]}"
            help_lines.append(f"  {c1.ljust(26)} | {c2}")

        help_lines.append("=" * 30)
        return "\n".join(help_lines)

    def execute(self, draw_string, record=True):
        if record:
            self.command_history.append(draw_string)

        self._is_running = True
        self._run_id += 1
        current_run_id = self._run_id

        tokens = re.findall(r"([A-Za-z]+|[-+]?\d+[\s,]*[-+]?\d*|[-+]?\d+)", draw_string)

        i = 0
        while i < len(tokens) and current_run_id == self._run_id:
            # Verifica se o renderer solicitou um redesenho (ex: redimensionamento)
            if self.renderer.should_redraw:
                self._is_running = False
                # Não chamamos _do_redraw aqui para evitar recursão.
                # O controle volta para quem chamou execute (wait_for_exit ou run_application)
                return

            if not self.renderer.is_alive():
                self.stop()
                return

            token = tokens[i].upper().strip()

            # ... (Lógica de prefixos B/N)
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
            if self.delay > 0 and current_run_id == self._run_id:
                self.renderer.wait(self.delay)

        if current_run_id == self._run_id:
            self._is_running = False

    def stop(self):
        """Solicita a interrupção da execução atual incrementando o run_id."""
        self._run_id += 1
        self._is_running = False

    def reset(self):
        """Reinicia o estado da engine para a posição original, mantendo o histórico."""
        self.x, self.y = self.renderer.get_start_pos()
        self.scale = 4
        self.angle = 0
        self.color_index = 15
        self.renderer.set_color(self.color_index)

    def redraw(self):
        """Limpa o renderer e reexecuta todo o histórico de comandos."""
        self.stop()
        self._do_redraw()

    def _do_redraw(self):
        """Lógica interna de redesenho."""
        self.renderer.prepare_for_redraw()
        self.renderer.limpar_tela()
        self.reset()
        full_history = " ".join(self.command_history)
        self.execute(full_history, record=False)

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
