import argparse
import sys
import tkinter as tk
from draw.core.engine import DrawEngine, carregar_do_arquivo
from draw.renderers.console_renderer import ConsoleRenderer
from draw.renderers.tkinter_renderer import TkinterRenderer


def main():
    parser = argparse.ArgumentParser(description="Interpretador DRAW Unificado")
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
    parser.add_argument(
        "-a",
        "--app",
        choices=["g", "c"],
        default="g",
        help="Escolha a apresentação: g (gráfico, padrão) ou c (console)",
    )

    args = parser.parse_args()

    if not (args.command or args.file or args.test):
        parser.print_help()
        sys.exit(0)

    if args.app == "c":
        renderer = ConsoleRenderer()

    else:
        root = tk.Tk()
        root.title("Interpretador Clássico do Comando DRAW")
        canvas_width, canvas_height = 640, 480
        canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="black")
        canvas.pack()
        renderer = TkinterRenderer(canvas, canvas_width, canvas_height)

    engine = DrawEngine(renderer, delay_ms=args.slow)

    if args.test:
        if args.app == "c":
            engine.execute("C4 U6 R12 D6 L12 BM +20,+2 C14 NU4 NR8 ND4 NL8")
            carregar_do_arquivo("assets/desenho_console.txt", engine)
        else:
            engine.execute("C4 U40 R40 D40 L40 BM +60,+60 C14 TA45 U40 R40 D40 L40")
            carregar_do_arquivo("assets/desenho.txt", engine)

    if args.command:
        engine.execute(args.command)

    if args.file:
        carregar_do_arquivo(args.file, engine)

    if args.app == "c":
        renderer.finalize()
    else:
        root.mainloop()


if __name__ == "__main__":
    main()
