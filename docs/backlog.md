# Backlog de Melhorias Sugeridas

Este documento lista possíveis evoluções para o projeto **DRAW Interpreter** e o status de melhorias já realizadas.

---

## Próximos Passos

### 1. Distribuição como Ferramenta CLI
Preparar o pacote para ser instalado via `pip` e utilizado diretamente no terminal.
- **Comando:** Utilizar `draw` ou `pydraw` (caso haja conflito) como ponto de entrada global no sistema.
- **Configuração:** Ajustar `pyproject.toml` para definir os `project.scripts`.

### 2. Estratégias de Ajuste de Escala
Criar parâmetros via CLI para definir o comportamento do redesenho:
- **Modo Estático:** Redesenha mantendo o tamanho original.
- **Modo Proporcional:** Altera o `pixel-size` ou `scale` automaticamente para preencher a nova área disponível.
    
### 3. Suporte a Macros e Sub-Desenhos
Implementar suporte para definir blocos de comandos que podem ser reutilizados.
- **Ideia:** Adicionar um comando `D n` (Define) para salvar uma sequência e um comando `X n` (eXecute) para chamá-la.

### 4. Exportação para Formatos Vetoriais (SVG)
Aproveitar a arquitetura de Bridge para criar um `SVGRenderer`.
- **Ideia:** Em vez de renderizar na tela, gerar um arquivo `.svg` ao final da execução. Isso permitiria usar os desenhos criados em alta qualidade em outros softwares.

### 5. Expansão do Sistema de Cores (RGB/Hex)
O protocolo atual é limitado às 16 cores clássicas do CGA/BASIC.
- **Ideia:** Adicionar um comando estendido (ex: `HC #RRGGBB`) que suporte cores 24-bit no modo gráfico e use algoritmos de proximidade (Euclidean distance) para mapear para a cor ANSI mais próxima no terminal.

---

## Experiência do Usuário (UX)

### 6. Interface CLI Interativa (REPL)
Permitir que o usuário digite comandos um a um e veja o resultado imediatamente.
- **Ideia:** Criar uma casca interativa onde cada linha de comando DRAW digitada é enviada para o Renderer aberto em tempo real.

### 7. Uso do Projeto como Biblioteca (Biblioteca de Desenho)
Permitir que outros programas Python importem e utilizem o motor e os renderizadores sem as restrições da CLI.
- **Funcionalidade:** Adicionar opção para desabilitar o bloqueio de "pressionar tecla para sair" (`wait_for_exit`), permitindo controle total pelo programa que chama a biblioteca.
- **Flexibilidade:** Facilitar a integração em outros aplicativos GUI ou scripts de automação.

---

[Voltar ao README](../README.md)
