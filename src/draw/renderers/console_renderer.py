import os
import sys
import time


class ConsoleRenderer:
    def __init__(self):
        self.atualizar_tamanho_terminal()
        self.color_code = "37"  # Branco padrão ANSI
        self.colors = {
            0: "30",
            1: "34",
            2: "32",
            3: "36",
            4: "31",
            5: "35",
            6: "33",
            7: "37",
            8: "30;1",
            9: "34;1",
            10: "32;1",
            11: "36;1",
            12: "31;1",
            13: "35;1",
            14: "33;1",
            15: "37;1",
        }
        self.limpar_tela()

    def get_start_pos(self):
        return self.width // 2, self.height // 2

    def atualizar_tamanho_terminal(self):
        try:
            tamanho = os.get_terminal_size()
            self.width = tamanho.columns
            self.height = tamanho.lines
        except OSError:
            self.width = 80
            self.height = 24

    def limpar_tela(self):
        os.system("cls" if os.name == "nt" else "clear")
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    def set_color(self, index):
        self.color_code = self.colors.get(index, "37")

    def draw_line(self, x1, y1, x2, y2):
        distance = max(abs(x2 - x1), abs(y2 - y1))
        if distance == 0:
            self._plot(x1, y1)
        else:
            x_inc = (x2 - x1) / distance
            y_inc = (y2 - y1) / distance
            cx, cy = x1, y1
            for _ in range(int(round(distance)) + 1):
                self._plot(cx, cy)
                cx += x_inc
                cy += y_inc

    def _plot(self, x, y):
        cx = int(round(x))
        cy = int(round(y))
        if 1 <= cx <= self.width and 1 <= cy <= self.height:
            sys.stdout.write(f"\033[{cy};{cx}H\033[{self.color_code}m█")
            sys.stdout.flush()

    def wait(self, seconds):
        time.sleep(seconds)

    def wait_for_exit(self):
        # Opcional: espera um enter para não fechar o terminal imediatamente se rodado fora de um shell persistente
        pass

    def finalize(self):
        sys.stdout.write(f"\033[{self.height};1H\033[0m\n")
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
