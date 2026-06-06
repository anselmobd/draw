import argparse
import sys
from draw.core.engine import DrawEngine
from draw.renderers.console_renderer import ConsoleRenderer
from draw.renderers.tkinter_renderer import TkinterRenderer


def parse_args():
    parser = argparse.ArgumentParser(
        description="Interpretador DRAW Unificado",
        epilog="Nota: O programa aguarda o pressionamento de qualquer tecla para encerrar após o desenho.",
    )
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
    parser.add_argument(
        "-F",
        "--fullscreen",
        action="store_true",
        help="Abre a janela gráfica em modo tela cheia",
    )
    parser.add_argument(
        "-M", "--maximize", action="store_true", help="Abre a janela gráfica maximizada"
    )

    args = parser.parse_args()

    if not (args.command or args.file or args.test):
        parser.print_help()
        sys.exit(0)

    return args


def main():
    args = parse_args()

    # Define o modo de janela para o renderer de GUI
    window_mode = "normal"
    if args.fullscreen:
        window_mode = "fullscreen"
    elif args.maximize:
        window_mode = "maximized"

    if args.app == "c":
        renderer = ConsoleRenderer()
    else:
        renderer = TkinterRenderer(window_mode=window_mode)

    engine = DrawEngine(renderer, delay_ms=args.slow)

    if args.test:
        if args.app == "c":
            engine.execute("C4 U6 R12 D6 L12 BM +20,+2 C14 NU4 NR8 ND4 NL8")
            engine.execute_file("assets/desenho_console.txt")
        else:
            engine.execute("C4 U40 R40 D40 L40 BM +60,+60 C14 TA45 U40 R40 D40 L40")
            engine.execute_file("assets/desenho.txt")

    if args.command:
        engine.execute(args.command)

    if args.file:
        engine.execute_file(args.file)

    renderer.wait_for_exit()
    renderer.finalize()


if __name__ == "__main__":
    main()
