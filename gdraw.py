import math
import re
import tkinter as tk
from tkinter import messagebox


class BasicDrawInterpreter:
    def __init__(self, canvas, width=640, height=480):
        self.canvas = canvas
        # Inicializa o cursor no centro da tela (padrão do BASIC)
        self.x = width // 2
        self.y = height // 2
        self.scale = 4  # Escala padrão 4 (significa 1:1)
        self.angle = 0  # Ângulo em graus (usado pelo TA)
        self.color_index = 15  # Cor padrão (Branco no MSX/DOS clássico)

        # Paleta de Cores Clássica (Simulando o padrão EGA de 16 cores)
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

    def execute(self, draw_string):
        # Limpa espaços e divide letras de números usando Regex
        # Ex: "C4U20" vira ['C', '4', 'U', '20']
        tokens = re.findall(r"([A-Za-z]+|[-+]?\d+[\s,]*[-+]?\d*|[-+]?\d+)", draw_string)

        i = 0
        while i < len(tokens):
            token = tokens[i].upper().strip()

            # Verifica prefixos modificadores
            blind = False
            noupdate = False
            if "B" in token:
                blind = True
                token = token.replace("B", "")
            if "N" in token:
                noupdate = True
                token = token.replace("N", "")

            # Se sobrou apenas o comando vazio (ex: era só "B" isolado antes de outro comando)
            if not token and i + 1 < len(tokens):
                i += 1
                next_tok = tokens[i].upper()
                if "B" in next_tok:
                    blind = True
                if "N" in next_tok:
                    noupdate = True
                token = re.sub(r"[BN]", "", next_tok)

            # Captura o argumento numérico do comando se houver
            arg = ""
            if i + 1 < len(tokens) and re.match(r"^[-+]?\d+", tokens[i + 1]):
                i += 1
                arg = tokens[i].strip()

            if token in ["U", "D", "L", "R", "E", "F", "G", "H", "M"]:
                self._move_command(token, arg, blind, noupdate)
            elif token == "C":
                self.color_index = int(arg) if arg else 15
            elif token == "S":
                self.scale = int(arg) if arg else 4
            elif token == "A":
                # A0=0, A1=90, A2=180, A3=270 graus
                a_val = int(arg) if arg else 0
                self.angle = a_val * 90
            elif token == "TA":
                # Rotação livre (Turn Angle) do QBasic
                self.angle = float(arg) if arg else 0.0

            i += 1

    def _move_command(self, cmd, arg, blind, noupdate):
        # Calcula a distância baseada na escala (passo real = n * (scale / 4))
        dist = float(arg) * (self.scale / 4.0) if arg and cmd != "M" else 0

        dx, dy = 0, 0

        # Define as direções padrão dos eixos cartesianos
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
            # Movimento absoluto ou relativo
            is_relative = "+" in arg or "-" in arg
            coords = [c.strip() for c in arg.split(",")]
            if len(coords) == 2:
                mx, my = float(coords[0]), float(coords[1])
                if is_relative:
                    dx, dy = mx * (self.scale / 4.0), my * (self.scale / 4.0)
                else:
                    # Absoluto ignora rotação e escala
                    new_x, new_y = mx, my
                    self._draw_line_to(new_x, new_y, blind, noupdate)
                    return

        # Aplica a rotação do ângulo atual (A ou TA) para comandos direcionais/relativos
        if self.angle != 0 and cmd != "M":
            rad = math.radians(
                -self.angle
            )  # Negativo porque o eixo Y do canvas é invertido
            rx = dx * math.cos(rad) - dy * math.sin(rad)
            ry = dx * math.sin(rad) + dy * math.cos(rad)
            dx, dy = rx, ry

        new_x = self.x + dx
        new_y = self.y + dy
        self._draw_line_to(new_x, new_y, blind, noupdate)

    def _draw_line_to(self, nx, ny, blind, noupdate):
        color = self.colors.get(self.color_index, "white")

        # Desenha apenas se o modo oculto (Blind) não estiver ativo
        if not blind:
            self.canvas.create_line(self.x, self.y, nx, ny, fill=color, width=1)

        # Atualiza a posição do cursor (a menos que N esteja ativo)
        if not noupdate:
            self.x = nx
            self.y = ny


# --- Função para ler de um arquivo ---
def carregar_do_arquivo(caminho_arquivo, interpretador):
    try:
        with open(caminho_arquivo, "r") as f:
            # Lê todas as linhas do arquivo e junta em uma única string de comandos
            conteudo = " ".join(
                [
                    linha.strip()
                    for linha in f
                    if linha.strip() and not linha.startswith("#")
                ]
            )
            interpretador.execute(conteudo)
    except FileNotFoundError:
        messagebox.showerror("Erro", f"Arquivo '{caminho_arquivo}' não encontrado.")


# --- Inicialização da Interface Gráfica ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Interpretador Clássico do Comando DRAW")

    # Cria uma tela preta simulando o monitor antigo
    canvas_width, canvas_height = 640, 480
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="black")
    canvas.pack()

    interpreter = BasicDrawInterpreter(canvas, canvas_width, canvas_height)

    # --- EXEMPLO DE USO 1: String Direta ---
    # Desenha um quadrado vermelho (C4), salta de posição (BM), muda para amarelo (C14) e rotaciona em 45° (TA45)
    string_teste = "C4 U40 R40 D40 L40 BM +60,+60 C14 TA45 U40 R40 D40 L40"
    interpreter.execute(string_teste)

    # --- EXEMPLO DE USO 2: Lendo de um arquivo ---
    # Descomente a linha abaixo para testar a leitura de arquivo.
    # Crie um arquivo 'desenho.txt' na mesma pasta e coloque os comandos nele.

    carregar_do_arquivo("desenho.txt", interpreter)

    root.mainloop()
