from draw.renderers.base import Renderer


class MockRenderer(Renderer):
    def __init__(self, width=800, height=600, verbose=False, is_discrete=False):
        self.width = width
        self.height = height
        self.verbose = verbose
        self._is_discrete = is_discrete
        self.lines = []  # Lista de tuplas ((x1, y1), (x2, y2), color_index)
        self.color_index = 15
        self.history = []  # Log de operações para auditoria detalhada

    @property
    def is_discrete(self):
        return self._is_discrete

    def get_start_pos(self):
        return self.width // 2, self.height // 2

    def get_resolution(self):
        return self.width, self.height

    def set_color(self, index):
        self.color_index = index
        self.history.append(("set_color", index))

    def draw_line(self, x1, y1, x2, y2):
        line = ((float(x1), float(y1)), (float(x2), float(y2)), self.color_index)
        self.lines.append(line)
        self.history.append(("draw_line", x1, y1, x2, y2))
        if self.verbose:
            print(f"{x1} {y1} - {x2} {y2} - {self.color_index}")

    def limpar_tela(self):
        self.lines = []
        self.history.append(("limpar_tela",))
        if self.verbose:
            print("limpar_tela")

    def wait(self, seconds):
        pass

    def wait_for_exit(self):
        pass

    def finalize(self):
        pass
