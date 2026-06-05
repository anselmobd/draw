from abc import ABC, abstractmethod


class Renderer(ABC):
    @abstractmethod
    def get_start_pos(self) -> tuple[int, int]:
        """Retorna a posição (x, y) inicial para o desenho."""
        pass

    @abstractmethod
    def set_color(self, index: int):
        """Define a cor atual baseada no índice (0-15)."""
        pass

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
