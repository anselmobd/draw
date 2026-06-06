import argparse
import sys
from draw.core.engine import DrawEngine
from draw.renderers.console_renderer import ConsoleRenderer
from draw.renderers.tkinter_renderer import TkinterRenderer
from draw.renderers.mock_renderer import MockRenderer


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
        "-m",
        "--mock",
        action="store_true",
        help="Executa em modo mock (apenas listagem de coordenadas no console)",
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
    parser.add_argument(
        "-p",
        "--pixel-size",
        type=str,
        default="1x1",
        help="Tamanho do pixel (ex: 2 ou 2x3)",
    )

    args = parser.parse_args()

    if not (args.command or args.file or args.test):
        parser.print_help()
        sys.exit(0)

    return args


def main():
    args = parse_args()

    if args.test and args.app == "g":
        args.pixel_size = "8"

    # Processa o tamanho do pixel
    try:
        if "x" in args.pixel_size:
            w_p, h_p = map(int, args.pixel_size.split("x"))
            pixel_size = (w_p, h_p)
        else:
            p = int(args.pixel_size)
            pixel_size = (p, p)
    except ValueError:
        print(f"Erro: Formato de pixel inválido '{args.pixel_size}'. Use '2' ou '2x3'.")
        sys.exit(1)

    # Define o modo de janela para o renderer de GUI
    window_mode = "normal"
    if args.fullscreen:
        window_mode = "fullscreen"
    elif args.maximize:
        window_mode = "maximized"

    if args.app == "c":
        renderer = ConsoleRenderer(headless=args.mock, pixel_size=pixel_size)
    else:
        renderer = TkinterRenderer(
            window_mode=window_mode, headless=args.mock, pixel_size=pixel_size
        )

    if args.mock:
        w, h = renderer.get_resolution()
        renderer = MockRenderer(
            width=w,
            height=h,
            verbose=True,
            is_discrete=renderer.is_discrete,
            pixel_size=pixel_size,
        )

    engine = DrawEngine(renderer, delay_ms=args.slow)

    if args.test:
        engine.execute_file("assets/teste.drw")

    if args.command:
        engine.execute(args.command)

    if args.file:
        engine.execute_file(args.file)

    renderer.wait_for_exit()
    renderer.finalize()


if __name__ == "__main__":
    main()
