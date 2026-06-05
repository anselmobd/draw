import argparse
import math
import os
import re
import sys
import time


class ConsoleDrawInterpreter:
    def __init__(self, delay_ms=20):
        # DETECÇÃO DINÂMICA: Pega o tamanho real do terminal atual
        self.atualizar_tamanho_terminal()

        self.scale = 4
        self.angle = 0
        self.color_code = "37"  # Branco padrão ANSI
        self.delay = delay_ms / 1000.0

        # Paleta de Cores ANSI mapeada a partir do clássico (Aproximado)
        # 30=Preto, 34=Azul, 32=Verde, 36=Ciano, 31=Vermelho, 35=Magenta, 33=Amarelo, 37=Branco
        # Adicionando ";1" ativamos o modo brilhante (Cores 8 a 15)
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

    def atualizar_tamanho_terminal(self):
        try:
            # Obtém as colunas (width) e linhas (height) atuais do console
            tamanho = os.get_terminal_size()
            self.width = tamanho.columns
            self.height = tamanho.lines
        except OSError:
            # Valores de segurança caso o script seja rodado onde não há um terminal real
            self.width = 80
            self.height = 24

        # Reposiciona o cursor no centro exato da tela detectada
        self.x = self.width // 2
        self.y = self.height // 2

    def limpar_tela(self):
        # Limpa o terminal usando comandos do sistema operacional
        os.system("cls" if os.name == "nt" else "clear")
        # Esconde o cursor piscante do terminal para melhorar o visual
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    def mudar_cor(self, index):
        self.color_code = self.colors.get(index, "37")

    def desenhar_ponto_terminal(self, x, y):
        # Proteção para não desenhar fora dos limites físicos do terminal
        cx = int(round(x))
        cy = int(round(y))
        # Agora valida o desenho usando os limites dinâmicos da tela
        if 1 <= cx <= self.width and 1 <= cy <= self.height:
            # Sequência ANSI: \033[Y;XH move o cursor para a linha Y, coluna X
            # \033[CORm define a cor do texto. O caractere '█' simula o pixel.
            sys.stdout.write(f"\033[{cy};{cx}H\033[{self.color_code}m█")
            sys.stdout.flush()

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
                self.mudar_cor(int(arg) if arg else 15)
            elif token == "S":
                self.scale = int(arg) if arg else 4
            elif token == "A":
                self.angle = (int(arg) if arg else 0) * 90
            elif token == "TA":
                self.angle = float(arg) if arg else 0.0

            i += 1
            # Pausa para ver o desenho sendo construído
            if self.delay > 0:
                time.sleep(self.delay)

    def _move_command(self, cmd, arg, blind, noupdate):
        # Em modo texto, passos curtos (escala menor) funcionam melhor devido ao tamanho das letras
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
                    self._render_line(mx, my, blind, noupdate)
                    return

        if self.angle != 0 and cmd != "M":
            rad = math.radians(-self.angle)
            rx = dx * math.cos(rad) - dy * math.sin(rad)
            ry = dx * math.sin(rad) + dy * math.cos(rad)
            dx, dy = rx, ry

        self._render_line(self.x + dx, self.y + dy, blind, noupdate)

    def _render_line(self, nx, ny, blind, noupdate):
        # Algoritmo de Bresenham/DDA simplificado para traçar linhas usando blocos de texto
        if not blind:
            x1, y1 = self.x, self.y
            x2, y2 = nx, ny
            points_to_draw = []

            distance = max(abs(x2 - x1), abs(y2 - y1))
            if distance == 0:
                points_to_draw.append((x1, y1))
            else:
                x_inc = (x2 - x1) / distance
                y_inc = (y2 - y1) / distance
                cx, cy = x1, y1
                for _ in range(int(round(distance)) + 1):
                    points_to_draw.append((cx, cy))
                    cx += x_inc
                    cy += y_inc

            for pt in points_to_draw:
                self.desenhar_ponto_terminal(pt[0], pt[1])

        if not noupdate:
            self.x = nx
            self.y = ny


def carregar_do_arquivo(caminho_arquivo, interpretador):
    try:
        with open(caminho_arquivo, "r") as f:
            conteudo = " ".join(
                [
                    linha.strip()
                    for linha in f
                    if linha.strip() and not linha.startswith("#")
                ]
            )
            interpretador.execute(conteudo)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")


# --- Execução Principal ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interpretador DRAW no Console")
    parser.add_argument(
        "command", type=str, nargs="?", help="Executa uma string de comandos DRAW"
    )
    parser.add_argument(
        "-f", "--file", type=str, help="Executa comandos DRAW de um arquivo"
    )
    parser.add_argument(
        "-t", "--test", action="store_true", help="Executa o teste padrão"
    )
    parser.add_argument(
        "-s", "--slow", type=int, default=0, help="Atraso entre comandos (milisegundos)"
    )

    args = parser.parse_args()

    # Se nenhum argumento for passado, mostra o help
    if not (args.command or args.file or args.test):
        parser.print_help()
        sys.exit(0)

    # Inicializa o interpretador (ele vai detectar o tamanho sozinho)
    interpreter = ConsoleDrawInterpreter(delay_ms=args.slow)

    if args.test:
        # IMPORTANTE: Como caracteres de texto são maiores que pixels, use distâncias menores!
        # Desenha um quadrado vermelho (C4), pula posição (BM), faz uma cruz amarela (C14) com N (no-update)
        string_terminal = "C4 U6 R12 D6 L12 BM +20,+2 C14 NU4 NR8 ND4 NL8"
        interpreter.execute(string_terminal)
        carregar_do_arquivo("desenho_console.txt", interpreter)

    if args.command:
        interpreter.execute(args.command)

    if args.file:
        carregar_do_arquivo(args.file, interpreter)

    # Move o cursor para a última linha do terminal atualizado para não bagunçar o prompt
    sys.stdout.write(f"\033[{interpreter.height};1H\033[0m\n")
    sys.stdout.write("\033[?25h")  # Devolve o cursor piscante ao sistema
    sys.stdout.flush()
