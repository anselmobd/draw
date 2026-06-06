# Backlog de Melhorias Sugeridas

Este documento lista possíveis evoluções para o projeto **DRAW Interpreter**, focando em arquitetura, funcionalidades e experiência do desenvolvedor.

---

## 🚀 Funcionalidades e Renderização

### 1. Persistência de Desenho no Modo Gráfico (Tkinter)
Atualmente, as linhas são desenhadas diretamente no Canvas. Se a janela for minimizada ou sobreposta por outra, o conteúdo pode ser perdido em alguns sistemas.
- **Ideia:** Armazenar um histórico de comandos de desenho (vetorial) e implementar o redesenho automático em eventos de exposição da janela.

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

## 🛠️ Qualidade de Código e Arquitetura

### 5. Sistema de Macros e Sub-Desenhos
Implementar suporte para definir blocos de comandos que podem ser reutilizados.
- **Ideia:** Adicionar um comando `D n` (Define) para salvar uma sequência e um comando `X n` (eXecute) para chamá-la, similar ao que alguns dialetos BASIC faziam.

---

## ✅ Melhorias Implementadas

### 1. Suíte de Testes Automatizados (Pytest)
Implementada a base para testes de regressão da lógica do interpretador.
- **Resultado:** Criado o `MockRenderer` e conjunto inicial de testes em `tests/test_engine.py` cobrindo movimentos, transformações e estados da Engine.
- **Documentação:** [Guia de Testes](testing.md).

### 2. Modos de Janela (Tkinter)
Adicionado suporte para diferentes estados de exibição da janela gráfica via CLI.
- **Resultado:** Implementadas as flags `--fullscreen` (-F) e `--maximize` (-M). O canvas agora se ajusta automaticamente à resolução do monitor ou área maximizada, garantindo desenhos centralizados em qualquer escala.

---

## 🎨 Experiência do Usuário (UX)

### 6. Interface CLI Interativa (REPL)
Permitir que o usuário digite comandos um a um e veja o resultado imediatamente.
- **Ideia:** Criar uma casca interativa onde cada linha de comando DRAW digitada é enviada para o Renderer aberto em tempo real.

### 7. Documentação Automática de Comandos
Gerar uma referência rápida formatada a partir das docstrings dos métodos da `DrawEngine`.
- **Ideia:** Facilitar para que o usuário saiba quais comandos estão disponíveis e qual a sintaxe exata de cada um sem precisar ler o código.
