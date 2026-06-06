from abc import ABC, abstractmethod


class Renderer(ABC):
    def __init__(self, pixel_size=(1, 1)):
        self.window_mode = "normal"  # "normal", "fullscreen", "maximized"
        self.pixel_size = pixel_size  # (width, height) base para cada "pixel" lógico
        self.on_resize_callback = None

    def set_on_resize(self, callback):
        """Define o callback a ser chamado em caso de redimensionamento."""
        self.on_resize_callback = callback

    def is_alive(self) -> bool:
        """Retorna se o renderizador ainda está ativo para desenho."""
        return True

    @abstractmethod
    def get_start_pos(self) -> tuple[int, int]:
        """Retorna a posição (x, y) inicial para o desenho."""
        pass

    @abstractmethod
    def set_color(self, index: int):
        """Define a cor atual baseada no índice (0-15)."""
        pass

    @abstractmethod
    def get_resolution(self) -> tuple[int, int]:
        """Retorna a resolução (largura, altura) do renderer."""
        pass

    @property
    def is_discrete(self) -> bool:
        """Indica se o renderer trabalha com um grid discreto de pixels."""
        return False

    @abstractmethod
    def draw_line(self, x1: float, y1: float, x2: float, y2: float):
        """Desenha uma linha entre dois pontos."""
        pass

    @abstractmethod
    def limpar_tela(self):
        """Limpa a área de desenho."""
        pass

    @abstractmethod
    def wait(self, seconds: float):
        """Pausa a execução por um determinado tempo."""
        pass

    @abstractmethod
    def wait_for_exit(self):
        """Aguarda uma interação do usuário para encerrar o programa."""
        pass

    @abstractmethod
    def finalize(self):
        """Executa limpezas finais antes do encerramento."""
        pass
