import os
import sys
import time
import math
import signal
import select
from draw.renderers.base import Renderer


class ConsoleRenderer(Renderer):
    def __init__(self, headless=False, pixel_size=(1, 1)):
        # No Windows, precisamos garantir que as sequências ANSI sejam processadas
        if os.name == "nt":
            os.system("")

        super().__init__(pixel_size=pixel_size)
        self.needs_redraw = False
        self.old_term_state = None
        self.atualizar_tamanho_terminal()

        # Registra o signal handler para redimensionamento (apenas Unix/Linux)
        if os.name != "nt":
            signal.signal(signal.SIGWINCH, self._handle_sigwinch)

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
    def should_redraw(self) -> bool:
        return self.needs_redraw

    @property
    def is_discrete(self) -> bool:
        return True

    def limpar_tela(self):
        # Limpa o buffer interno para não sobrar pixels de desenhos anteriores
        self.screen_buffer = {}
        # Garante que as cores sejam resetadas antes de limpar a tela,
        # para evitar que o terminal preencha o fundo com a última cor ativa (Background Color Erase)
        sys.stdout.write("\033[0m")
        sys.stdout.flush()
        os.system("cls" if os.name == "nt" else "clear")
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    def set_color(self, index):
        self.fg_code, self.bg_code = self.colors.get(index, ("37", "40"))

    def draw_line(self, x1, y1, x2, y2):
        # Algoritmo de Bresenham para garantir linhas simétricas e sem gaps
        # Trabalhamos diretamente no grid discreto (pixels)
        x1_i, y1_i = int(math.floor(x1 + 0.5)), int(math.floor(y1 + 0.5))
        x2_i, y2_i = int(math.floor(x2 + 0.5)), int(math.floor(y2 + 0.5))

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
        # As coordenadas cx e cy no buffer são 0-indexadas:
        # cx: 0 até width-1
        # cy: 0 até logical_height-1
        if 0 <= cx < self.width and 0 <= cy < self.logical_height:
            # Algoritmo de mapeamento para sub-pixel ANSI:
            # Cada célula do terminal (row) tem 2 pixels verticais.
            # cy=0 (Top) e cy=1 (Bottom) pertencem à row 1 (ANSI é 1-indexado para cursor)
            char_row = (cy // 2) + 1
            char_col = cx + 1
            is_top = cy % 2 == 0

            cell_key = (char_row, char_col)
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
                if c_top == c_bottom:
                    # Ambas com a mesma cor: usa o caractere de bloco cheio
                    fg = c_top
                    bg = "49"
                    char = "█"
                else:
                    # Ambas preenchidas com cores diferentes: usa ▀ com FG em cima e BG embaixo
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

            # Escreve o pixel e reseta as cores para evitar "vazamento" de cor de fundo
            # se o terminal redimensionar/rolar durante a renderização.
            sys.stdout.write(f"\033[{char_row};{char_col}H\033[{fg};{bg}m{char}\033[0m")
            sys.stdout.flush()

    def _handle_sigwinch(self, signum, frame):
        """Signal handler para o redimensionamento do terminal."""
        self.needs_redraw = True

    def prepare_for_redraw(self):
        """Atualiza as dimensões e limpa a flag de redraw."""
        self.needs_redraw = False
        self.atualizar_tamanho_terminal()

    def wait(self, seconds):
        try:
            time.sleep(seconds)
        except InterruptedError:
            # Em caso de interrupção (ex: SIGWINCH), o tempo de espera pode ser menor
            pass

    def wait_for_exit(self):
        """Aguarda as teclas Espaço ou Enter para sair no console, ou sinal de redraw."""
        if not os.isatty(sys.stdin.fileno()):
            sys.stdin.read(1)
            return

        fd = sys.stdin.fileno()
        try:
            while True:
                if self.needs_redraw:
                    self.needs_redraw = False
                    self.atualizar_tamanho_terminal()
                    if self.on_resize_callback:
                        self.on_resize_callback()
                    continue

                # Espera por entrada no stdin com timeout curto para checar flags de redraw
                r, _, _ = select.select([fd], [], [], 0.05)
                if r:
                    try:
                        data = os.read(fd, 1024)
                        # Sair apenas se houver Espaço (32) ou Enter (13 ou 10)
                        if any(c in data for c in (32, 13, 10)):
                            break
                    except OSError:
                        break
        except Exception:
            pass

    def __enter__(self):
        """Configura o terminal para leitura de teclas (modo cbreak)."""
        if os.name != "nt" and sys.stdin.isatty():
            try:
                import tty
                import termios

                self.old_term_state = termios.tcgetattr(sys.stdin)
                tty.setcbreak(sys.stdin.fileno())
            except Exception:
                pass
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Restaura o terminal e finaliza o renderer."""
        self.finalize()
        if self.old_term_state:
            try:
                import termios
                import time

                # Pequena pausa para garantir o dreno do buffer antes de restaurar
                time.sleep(0.05)
                termios.tcsetattr(
                    sys.stdin.fileno(), termios.TCSAFLUSH, self.old_term_state
                )
            except Exception:
                pass

    def finalize(self):
        # Desabilita o signal handler de redimensionamento
        if os.name != "nt":
            try:
                signal.signal(signal.SIGWINCH, signal.SIG_DFL)
            except Exception:
                pass
        sys.stdout.write(f"\033[{self.height};1H\033[0m\n")
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
