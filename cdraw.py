import argparse
import os
import sys
import time
from engine import DrawEngine, carregar_do_arquivo

class ConsoleRenderer:
    def __init__(self):
        self.atualizar_tamanho_terminal()
        self.color_code = "37"  # Branco padrão ANSI
        self.colors = {
            0: "30", 1: "34", 2: "32", 3: "36", 4: "31", 5: "35", 6: "33", 7: "37",
            8: "30;1", 9: "34;1", 10: "32;1", 11: "36;1", 12: "31;1", 13: "35;1", 14: "33;1", 15: "37;1",
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

    def finalize(self):
        sys.stdout.write(f"\033[{self.height};1H\033[0m\n")
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

# --- Execução Principal ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interpretador DRAW no Console")
    parser.add_argument("command", type=str, nargs="?", help="Executa uma string de comandos DRAW")
    parser.add_argument("-f", "--file", type=str, help="Executa comandos DRAW de um arquivo")
    parser.add_argument("-t", "--test", action="store_true", help="Executa o teste padrão")
    parser.add_argument("-s", "--slow", type=int, default=20, help="Atraso entre comandos (milisegundos)")

    args = parser.parse_args()

    if not (args.command or args.file or args.test):
        parser.print_help()
        sys.exit(0)

    renderer = ConsoleRenderer()
    engine = DrawEngine(renderer, delay_ms=args.slow)

    if args.test:
        string_terminal = "C4 U6 R12 D6 L12 BM +20,+2 C14 NU4 NR8 ND4 NL8"
        engine.execute(string_terminal)
        carregar_do_arquivo("desenho_console.txt", engine)

    if args.command:
        engine.execute(args.command)

    if args.file:
        carregar_do_arquivo(args.file, engine)

    renderer.finalize()
