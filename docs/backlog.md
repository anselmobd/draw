# Backlog de Melhorias Sugeridas

Este documento lista possíveis evoluções para o projeto **DRAW Interpreter** e o status de melhorias já realizadas.

---

## Funcionalidades Implementadas (Recentemente)

### 1. Sistema de Redesenho Dinâmico
O sistema agora lida com redimensionamentos de forma robusta tanto no modo gráfico quanto no console.
- **Gráfico:** Integração com eventos do Tkinter para recompor o desenho.
- **Console:** Captura de `SIGWINCH` para redesenhar a arte adaptada ao novo tamanho do terminal.
- **Ciclo de Vida:** Uso de *Context Managers* para garantir a limpeza do ambiente (cursor, terminal `cbreak`) mesmo em interrupções.

---

## Próximos Passos

### 2. Exportação para Formatos Vetoriais (SVG)
Aproveitar a arquitetura de Bridge para criar um `SVGRenderer`.
- **Ideia:** Em vez de renderizar na tela, gerar um arquivo `.svg` ao final da execução. Isso permitiria usar os desenhos criados em alta qualidade em outros softwares.

### 3. Expansão do Sistema de Cores (RGB/Hex)
O protocolo atual é limitado às 16 cores clássicas do CGA/BASIC.
- **Ideia:** Adicionar um comando estendido (ex: `HC #RRGGBB`) que suporte cores 24-bit no modo gráfico e use algoritmos de proximidade (Euclidean distance) para mapear para a cor ANSI mais próxima no terminal.

### 4. Suporte a Macros e Sub-Desenhos
Implementar suporte para definir blocos de comandos que podem ser reutilizados.
- **Ideia:** Adicionar um comando `D n` (Define) para salvar uma sequência e um comando `X n` (eXecute) para chamá-la.

### 5. Estratégias de Ajuste de Escala
Criar parâmetros via CLI para definir o comportamento do redesenho:
- **Modo Estático:** Redesenha mantendo o tamanho original.
- **Modo Proporcional:** Altera o `pixel-size` ou `scale` automaticamente para preencher a nova área disponível.

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
