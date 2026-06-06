import os
import sys
import time
from draw.renderers.base import Renderer


class ConsoleRenderer(Renderer):
    def __init__(self, headless=False, pixel_size=(1, 1)):
        # No Windows, precisamos garantir que as sequências ANSI sejam processadas
        if os.name == "nt":
            os.system("")

        super().__init__(pixel_size=pixel_size)
        self.atualizar_tamanho_terminal()
        self.fg_code = "37"  # Branco frontal padrão
        self.bg_code = "40"  # Preto de fundo padrão
        self.screen_buffer = {}  # Armazena as cores (fg, bg) de cada célula (row, col)
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
        if not headless:
            self.limpar_tela()

    def get_start_pos(self):
        w, h = self.get_resolution()
        return w // 2, h // 2

    def get_resolution(self):
        pw, ph = self.pixel_size
        return self.width // pw, self.logical_height // ph

    def atualizar_tamanho_terminal(self):
        try:
            tamanho = os.get_terminal_size()
            self.width = tamanho.columns
            self.height = tamanho.lines
        except OSError:
            self.width = 80
            self.height = 24

        # Cada célula do terminal tem 2 "pixels" verticais (usando ▀)
        self.logical_height = self.height * 2

    @property
    def is_discrete(self) -> bool:
        return True

    def limpar_tela(self):
        # Limpa o buffer interno para não sobrar pixels de desenhos anteriores
        self.screen_buffer = {}
        os.system("cls" if os.name == "nt" else "clear")
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    def set_color(self, index):
        self.fg_code, self.bg_code = self.colors.get(index, ("37", "40"))

    def draw_line(self, x1, y1, x2, y2):
        # Algoritmo de Bresenham para garantir linhas simétricas e sem gaps
        # Trabalhamos diretamente no grid discreto (pixels)
        x1_i, y1_i = int(x1 + 0.5), int(y1 + 0.5)
        x2_i, y2_i = int(x2 + 0.5), int(y2 + 0.5)

        dx = abs(x2_i - x1_i)
        dy = abs(y2_i - y1_i)
        sx = 1 if x1_i < x2_i else -1
        sy = 1 if y1_i < y2_i else -1
        err = dx - dy

        curr_x, curr_y = x1_i, y1_i

        while True:
            self._plot(curr_x, curr_y)
            if curr_x == x2_i and curr_y == y2_i:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                curr_x += sx
            if e2 < dx:
                err += dx
                curr_y += sy

    def _plot(self, x, y):
        # x e y aqui já são inteiros vindos do Bresenham.
        cx, cy = int(x), int(y)
        pw, ph = self.pixel_size

        # Se houver escala de pixel, desenhamos múltiplos sub-pixels no grid ANSI
        for py in range(ph):
            for px in range(pw):
                self._plot_single(cx * pw + px, cy * ph + py)

    def _plot_single(self, cx, cy):
        if 1 <= cx <= self.width and 1 <= cy <= self.logical_height:
            # Algoritmo de mapeamento para sub-pixel ANSI:
            # Cada célula do terminal (row) tem 2 pixels verticais.
            # cy=1 (Top), cy=2 (Bottom) -> row 1
            # Para garantir que o pico de um triângulo (cy=1) seja desenhado
            # como um único bloco central '▄' em vez de '▄▀▄', usamos:
            char_row = (cy + 1) // 2
            is_top = cy % 2 != 0

            cell_key = (char_row, cx)
            if cell_key not in self.screen_buffer:
                self.screen_buffer[cell_key] = [
                    None,
                    None,
                ]  # None significa "transparente/fundo"

            if is_top:
                self.screen_buffer[cell_key][0] = self.fg_code
            else:
                self.screen_buffer[cell_key][1] = self.fg_code

            c_top = self.screen_buffer[cell_key][0]
            c_bottom = self.screen_buffer[cell_key][1]

            # Lógica de renderização para preservar transparência e cores:
            # Se apenas uma metade estiver pintada, usamos o caractere específico (▀ ou ▄)
            # com fundo padrão (49) para não "manchar" a outra metade com Preto (30/40).
            if c_top is not None and c_bottom is not None:
                # Ambas preenchidas: usa ▀ com FG em cima e BG embaixo
                fg = c_top
                if ";1" in c_bottom:
                    bg = c_bottom.replace("3", "10", 1).replace(";1", "")
                else:
                    bg = c_bottom.replace("3", "4", 1)
                char = "▀"
            elif c_top is not None:
                # Só em cima: usa ▀ com fundo transparente
                fg = c_top
                bg = "49"
                char = "▀"
            else:  # c_bottom is not None
                # Só embaixo: usa ▄ com fundo transparente
                fg = c_bottom
                bg = "49"
                char = "▄"

            sys.stdout.write(f"\033[{char_row};{cx}H\033[{fg};{bg}m{char}")
            sys.stdout.flush()

    def wait(self, seconds):
        time.sleep(seconds)

    def wait_for_exit(self):
        # Aguarda qualquer tecla para sair no console
        # Removida mensagem para não interferir no desenho visual

        if os.name == "nt":
            import msvcrt

            msvcrt.getch()
        else:
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
