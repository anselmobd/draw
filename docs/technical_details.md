# Detalhes Técnicos - DRAW Interpreter

Este documento detalha as decisões de arquitetura e implementações técnicas avançadas do projeto.

## Arquitetura do Sistema

O projeto utiliza o **Bridge Pattern** para desacoplar a lógica de movimentação da renderização visual.

### Componentes Core
- **`DrawEngine`**: Responsável pelo processamento de tokens, tratamento de recursividade (prefixos B/N), transformações (escala/rotação) e gerenciamento de estado (posicionamento).
- **`Renderer` (Classe Base Abstrata)**: Localizada em `src/draw/renderers/base.py`, define o contrato rigoroso que qualquer motor de saída deve implementar utilizando o módulo `abc`. Isso facilita a criação de novos renderizadores (ex: SVG, Imagem estática, etc).

---

## Estrutura do Projeto (Src Layout)

O projeto segue as recomendações modernas do ecossistema Python utilizando o diretório `src/`:

```text
draw/
├── assets/                  # Scripts DRAW (.txt) de exemplo
├── src/
│   └── draw/                # Pacote principal
│       ├── __init__.py
│       ├── __main__.py      # CLI e orquestração
│       ├── core/
│       │   └── engine.py    # Lógica do interpretador
│       └── renderers/
│           ├── console_renderer.py # Renderizador ANSI High-Res
│           └── tkinter_renderer.py # Renderizador Gráfico (GUI)
├── run.py                   # Entry point para o usuário
└── pyproject.toml           # Configurações de build e metadados
```

---

## Renderização em "Alta Resolução" no Terminal

O `ConsoleRenderer` implementa uma técnica de sub-pixel para dobrar a resolução vertical disponível no terminal.

### O Caractere de Meia-Célula
Em vez de usar o bloco inteiro (`█`), utilizamos os caracteres de meia célula:
- `▀` (Upper Half Block - Unicode U+2580)
- `▄` (Lower Half Block - Unicode U+2584)

Cada célula do terminal (caractere) é tratada como **dois pixels verticais**. 

### Lógica de Buffer e Transparência
Como uma única célula pode conter dois pixels de cores diferentes, implementamos um `screen_buffer`:
1. **Mapeamento**: O motor envia coordenadas para uma `logical_height` que é o dobro da altura real do terminal.
2. **Buffer de Cores**: Armazenamos as cores da metade superior e inferior de cada célula.
3. **Composição**: 
   - Se apenas o pixel do topo estiver pintado, usamos `▀` com cor de frente e fundo transparente (`\033[49m`).
   - Se apenas o da base estiver pintado, usamos `▄`.
   - Se ambos estiverem pintados, usamos `▀` onde a cor do topo é o *Foreground* e a cor da base é convertida para *Background*.

### Conversão de Cores ANSI
Para que o sistema de cores 0-15 funcione em ambos os modos:
- Cores de Frente (*Foreground*): Escopo `30-37` e `30;1-37;1`.
- Cores de Fundo (*Background*): Convertidas dinamicamente para `40-47` e `100-107` ao compor a célula.

---

## Gerenciamento de Ciclo de Vida e Terminal

Para garantir que o ambiente seja restaurado corretamente (como o cursor do terminal ou a limpeza de recursos gráficos), implementamos o padrão **Context Manager** na classe base `Renderer`.

### Uso do Context Manager (`with`)
O uso do bloco `with renderer:` garante que, independentemente de como o programa termine (sucesso, erro ou interrupção por Ctrl+C), o método `finalize()` será invocado:
- O cursor do terminal é restaurado.
- Janelas gráficas são fechadas.
- O terminal volta ao modo de operação normal do sistema operacional.

### Entrada e Sinais no Console
Adotamos o **modo cbreak** para o console, o que oferece um equilíbrio entre controle e funcionalidade:

- **Modo `cbreak`**:
    - Permite a leitura de teclas individuais sem esperar pela tecla *Enter* (vital para o `wait_for_exit`).
    - Diferente do modo *raw*, ele preserva a geração de sinais do sistema. Isso permite que o **Ctrl+C** continue funcionando normalmente para interromper o programa, disparando um `KeyboardInterrupt` que o sistema captura para uma saída amigável.
- **Restauração (`termios`)**:
    - No Linux/macOS, o estado original do terminal é capturado no início da execução e restaurado milimetricamente no final, evitando que o shell do usuário fique "quebrado" (sem eco ou com configurações de linha alteradas).
- **Windows**:
    - O suporte a ANSI é habilitado via `os.system('')`, permitindo que o Windows execute as mesmas sequências de cores e posicionamento de cursor que outros sistemas.

---

## Precisão e Simetria (Snap-to-Grid)

Diferente de sistemas vetoriais puros, renderizadores de pixel sofrem com a acumulação de erros decimais ao lidar com rotações (TA45) e escalas. Para resolver isso, implementamos o **Grid Discreto**:

1. **Interface `is_discrete`**: Renderizadores baseados em pixels indicam que trabalham em um grid fixo.
2. **Snap-to-Grid**: A `DrawEngine` arredonda as coordenadas para o inteiro mais próximo (usando `int(v + 0.5)`) após cada movimento.
3. **Ponto Cego**: O arredondamento ocorre **antes** do desenho. Isso garante que o ponto final de uma linha e o inicial da próxima coincidam exatamente no mesmo pixel físico, evitando "gaps" de 1 pixel em vértices e garantindo simetria perfeita em diamantes e triângulos.

## Escala Física vs Escala Lógica

O sistema distingue dois tipos de escala:
- **Escala Lógica (`S n`)**: Altera o comprimento matemático das linhas (vetorial).
- **Escala Física (`-p / pixel_size`)**: Altera o tamanho de cada "unidade de desenho" na saída. Ao usar `-p 2x2`, cada pixel lógico é desenhado como um bloco de 4 pixels físicos, gerando um efeito de *Pixel Art*. A Engine recalibra automaticamente a resolução disponível (`get_resolution`) para que o sistema de coordenadas reflita o novo tamanho do "canvas".

Essas abordagens garantem que o encerramento do programa seja intuitivo e "limpo", respeitando o visual gerado pelo desenho.

---

[Voltar ao README](../README.md)
