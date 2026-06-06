# Backlog de Melhorias Sugeridas

Este documento lista possíveis evoluções para o projeto **DRAW Interpreter**, focando em arquitetura, funcionalidades e experiência do desenvolvedor.

---

## Funcionalidades e Renderização

### 1. Sistema de Persistência e Redesenho Dinâmico
Implementar um mecanismo centralizado na `DrawEngine` ou via histórico de comandos para permitir que o desenho seja reconstruído automaticamente em eventos de sistema.

#### 1.1 Redesenho no Modo Gráfico (Tkinter)
- **Objetivo:** Garantir que o conteúdo não seja perdido e se adapte a mudanças de janela.
- **Ações:** 
    - Vincular ao evento `<Configure>` do Tkinter.
    - Limpar o canvas e reiniciar a execução do histórico de comandos.
    - Implementar debounce ou cancelamento de tarefa para lidar com redimensionamentos contínuos (arrastar borda), interrompendo o redesenho em curso para iniciar o novo.

#### 1.2 Redesenho no Modo Console
- **Objetivo:** Adaptar o desenho ao novo tamanho do terminal (colunas/linhas).
- **Ações:**
    - Monitorar sinal `SIGWINCH` (Unix) ou mudanças no `os.get_terminal_size()`.
    - Recalcular `logical_height` e redesenhar do zero para manter a centralização e proporções.
    - Gerenciar a interrupção de fluxos lentos (com `--slow`) durante a atualização.

#### 1.3 Estratégias de Ajuste de Escala (Futuro)
- **Ideia:** Criar parâmetros via CLI para definir o comportamento do redesenho:
    - **Modo Estático:** Redesenha mantendo o tamanho original.
    - **Modo Proporcional:** Altera o `pixel-size` ou `scale` automaticamente para preencher a nova área disponível.

### 2. Exportação para Formatos Vetoriais (SVG)
Aproveitar a arquitetura de Bridge para criar um `SVGRenderer`.
- **Ideia:** Em vez de renderizar na tela, gerar um arquivo `.svg` ao final da execução. Isso permitiria usar os desenhos criados em alta qualidade em outros softwares.

### 3. Expansão do Sistema de Cores (RGB/Hex)
O protocolo atual é limitado às 16 cores clássicas do CGA/BASIC.
- **Ideia:** Adicionar um comando estendido (ex: `HC #RRGGBB`) que suporte cores 24-bit no modo gráfico e use algoritmos de proximidade (Euclidean distance) para mapear para a cor ANSI mais próxima no terminal.

### 4. Redimensionamento Dinâmico (Console)
Ajustar o renderizador de terminal para lidar com mudanças no tamanho da janela durante a execução.
- **Ideia:** Capturar o sinal `SIGWINCH` (no Linux) para atualizar `logical_height` e centralizar o desenho em tempo real.

---

## Qualidade de Código e Arquitetura

### 5. Sistema de Macros e Sub-Desenhos
Implementar suporte para definir blocos de comandos que podem ser reutilizados.
- **Ideia:** Adicionar um comando `D n` (Define) para salvar uma sequência e um comando `X n` (eXecute) para chamá-la, similar ao que alguns dialetos BASIC faziam.

---

## Experiência do Usuário (UX)

### 6. Interface CLI Interativa (REPL)
Permitir que o usuário digite comandos um a um e veja o resultado imediatamente.
- **Ideia:** Criar uma casca interativa onde cada linha de comando DRAW digitada é enviada para o Renderer aberto em tempo real.

### 7. Documentação Automática de Comandos
Gerar uma referência rápida formatada a partir das docstrings dos métodos da `DrawEngine`.
- **Ideia:** Facilitar para que o usuário saiba quais comandos estão disponíveis e qual a sintaxe exata de cada um sem precisar ler o código.

---

[Voltar ao README](../README.md)
