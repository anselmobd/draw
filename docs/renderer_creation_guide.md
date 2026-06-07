# Guia de Criação de Novos Renderers

Este documento descreve a arquitetura do sistema de renderização do **DRAW Interpreter** e fornece as diretrizes para a implementação de novos renderizadores, garantindo compatibilidade com todos os recursos modernos como redesenho dinâmico e tratamento de grids discretos.

---

## 1. A Classe Base `Renderer`

Todo novo renderizador deve herdar de `draw.renderers.base.Renderer` e implementar seus métodos abstratos. A classe base define o contrato que a `DrawEngine` utiliza para desenhar.

### Interface Obrigatória

| Método / Propriedade | Descrição |
| :--- | :--- |
| `get_resolution()` | Retorna `(width, height)` do espaço de desenho disponível. |
| `get_start_pos()` | Retorna `(x, y)` inicial, geralmente o centro da tela. |
| `set_color(index)` | Define a cor atual baseada na paleta de 16 cores (0-15). |
| `draw_line(x1, y1, x2, y2)` | Desenha uma linha entre dois pontos no sistema de coordenadas do renderer. |
| `limpar_tela()` | Limpa completamente a área de desenho. |
| `wait(seconds)` | Realiza uma pausa na execução (importante para o modo `--slow`). |
| `wait_for_exit()` | Bloqueia a execução ao final do desenho até que o usuário decida sair. |

---

## 2. Recursos Avançados e Ciclo de Vida

Para suportar redimensionamento e interatividade, o renderer deve gerenciar três estados principais:

### 2.1 Suporte a Grid Discreto (`is_discrete`)
Se o seu renderer trabalha com unidades inteiras (como pixels ou células de texto), sobrescreva esta propriedade:
```python
@property
def is_discrete(self) -> bool:
    return True
```
Isso sinaliza para a `DrawEngine` que ela deve arredondar as coordenadas antes de chamar `draw_line`, evitando gaps visuais e erros de assimetria.

### 2.2 Sistema de Redesenho Dinâmico
Essencial para lidar com mudanças de tamanho de janela ou terminal sem perder o desenho.

1.  **`should_redraw`**: Propriedade que a Engine consulta a cada comando. Se retornar `True`, a Engine interrompe a execução atual e inicia o `redraw`.
2.  **`prepare_for_redraw()`**: Chamado pela Engine logo antes de re-executar o histórico. Use para:
    - Atualizar variáveis internas de largura/altura.
    - Resetar flags de sinalização (ex: `self.needs_redraw = False`).
3.  **`set_on_resize(callback)`**: Armazene este callback. Ele deve ser invocado quando o sistema operacional notificar um redimensionamento (ex: evento `<Configure>` no Tkinter ou `SIGWINCH` no Console).

### 2.3 Gerenciamento de Vida Útil (Context Manager)
Cada renderer herda suporte automático para blocos `with`. É altamente recomendado que renderers complexos implementem seus próprios métodos de entrada e saída para gerenciar hardware ou estados de sistema:

- **`__enter__(self)`**: Prepare o ambiente (ex: esconder cursor, carregar assets). Deve retornar `self`.
- **`__exit__(self, exc_type, exc_val, exc_tb)`**: Chame obrigatoriamente `self.finalize()` e restaure estados alterados do sistema.

A `DrawEngine` e o `__main__.py` utilizam o renderer desta forma para garantir resiliência contra exceções e interrupções manuais.

---

## 3. Exemplo de Estrutura para Novo Renderer

```python
from draw.renderers.base import Renderer

class MeuNovoRenderer(Renderer):
    def __init__(self, **kwargs):
        super().__init__(pixel_size=kwargs.get("pixel_size", (1,1)))
        self.needs_redraw = False
        # Inicialize seu backend (ex: SDL, Cairo, etc)

    @property
    def should_redraw(self):
        return self.needs_redraw

    def prepare_for_redraw(self):
        self.needs_redraw = False
        self._update_dimensions()

    def draw_line(self, x1, y1, x2, y2):
        # Implementação do desenho
        pass

    def wait_for_exit(self):
        # Loop de eventos que verifica self.needs_redraw
        # e invoca self.on_resize_callback() se necessário
        pass
```

---

## 4. Boas Práticas de Implementação

- **Isolamento de Estado:** Sempre reset as cores do sistema gráfico ao finalizar um `draw_line` ou `limpar_tela` para evitar que estilos influenciem a interface externa do usuário (especialmente importante em consoles).
- **Tratamento de Sinais:** Se o seu backend usar chamadas bloqueantes (como `sleep`), certifique-se de tratar exceções de interrupção (`InterruptedError`) para que o sinal de redimensionamento seja processado imediatamente.
- **Headless Mode:** Se possível, suporte o parâmetro `headless` para permitir execuções em ambientes sem interface gráfica (CI/CD ou testes automatizados).

---

[Voltar ao README](../README.md)
