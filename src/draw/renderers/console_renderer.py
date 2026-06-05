import os
import sys
import time


class ConsoleRenderer:
    def __init__(self):
        self.atualizar_tamanho_terminal()
        self.fg_code = "37"  # Branco frontal padrão
        self.bg_code = "40"  # Preto de fundo padrão
        self.colors = {
            # Cores frontais (3x) e fundos (4x)
            0: ("30", "40"),  # Preto
            1: ("34", "44"),  # Azul
            2: ("32", "42"),  # Verde
            3: ("36", "46"),  # Ciano
            4: ("31", "41"),  # Vermelho
            5: ("35", "45"),  # Magenta
            6: ("33", "43"),  # Marrom/Amarelo escuro
            7: ("37", "47"),  # Cinza claro
            8: ("30;1", "100"),  # Cinza escuro
            9: ("34;1", "104"),  # Azul claro
            10: ("32;1", "102"),  # Verde claro
            11: ("36;1", "106"),  # Ciano claro
            12: ("31;1", "101"),  # Vermelho claro
            13: ("35;1", "105"),  # Magenta claro
            14: ("33;1", "103"),  # Amarelo
            15: ("37;1", "107"),  # Branco
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
        self.fg_code, self.bg_code = self.colors.get(index, ("37", "40"))

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
            # \033[fg;bgm -> define cor frontal e fundo
            sys.stdout.write(f"\033[{cy};{cx}H\033[{self.fg_code};{self.bg_code}m█")
            sys.stdout.flush()

    def wait(self, seconds):
        time.sleep(seconds)

    def wait_for_exit(self):
        # Aguarda qualquer tecla para sair no console (Linux/macOS)
        # Removida mensagem para não interferir no desenho visual

        fd = sys.stdin.fileno()
        if os.isatty(fd):
            import tty
            import termios

            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        else:
            sys.stdin.read(1)

    def finalize(self):
        sys.stdout.write(f"\033[{self.height};1H\033[0m\n")
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
