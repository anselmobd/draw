# Detalhes Técnicos - DRAW Interpreter

Este documento detalha as decisões de arquitetura e implementações técnicas avançadas do projeto.

## 🏗️ Arquitetura do Sistema

O projeto utiliza o **Bridge Pattern** para desacoplar a lógica de movimentação da renderização visual.

### Componentes Core
- **`DrawEngine`**: Responsável pelo processamento de tokens, tratamento de recursividade (prefixos B/N), transformações (escala/rotação) e gerenciamento de estado (posicionamento).
- **`Renderer` (Interface)**: Define o contrato que qualquer motor de saída deve implementar (`draw_line`, `set_color`, `limpar_tela`, etc.).

---

## 📁 Estrutura do Projeto (Src Layout)

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

## 🖥️ Renderização em "Alta Resolução" no Terminal

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

## ⌨️ Entrada Não-Bloqueante
Para implementar a funcionalidade "pressione qualquer tecla para sair" sem poluir o desenho no console, utilizamos:
- **Linux/macOS**: Módulo `termios` para colocar o terminal em modo *raw* temporariamente.
- **Windows**: Fallback para `msvcrt` ou `pause`.
