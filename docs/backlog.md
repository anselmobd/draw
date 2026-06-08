# Backlog de Melhorias Sugeridas

Este documento lista possíveis evoluções para o projeto **DRAW Interpreter** e o status de melhorias já realizadas.

---

## Próximos Passos

### 1. Distribuição Global e Acessibilidade (Portable CLI)
Expandir o projeto para que pessoas que não são desenvolvedoras Python consigam utilizar o comando `draw` sem configurar ambientes virtuais ou gerenciar dependências.

#### 1.0 Ciclo de Lançamento e Automação (Fase Atual)
Implementar ferramentas para facilitar o lançamento de novas versões.
- **Versão Única:** Centralizar a versão em um único lugar para evitar inconsistências.
- **CHANGELOG:** Manter um registro humano das mudanças para usuários finais.
- **Automação de Release:** Estudar ferramentas como `bumpver` ou `commitizen` para automatizar o incremento de versão e tags.

#### 1.1 Scripts de Instalação "One-Liner" (Concluído)
Criar scripts automatizados que detectam o ambiente e instalam o `draw` pronto para uso.
- **Linux/macOS (Bash):** Script que verifica o Python, cria um ambiente isolado em `~/.local/share/draw` e cria um link simbólico para o executável em `~/.local/bin`.
- **Windows (PowerShell):** Script equivalente que instala em `%APPDATA%\draw` e ajusta o `PATH` do usuário.
- **Desinstalador:** Ambos os scripts agora criam um comando `draw-uninstall` para remoção limpa do sistema.

#### 1.2 Executáveis Estáticos (Binários)
Gerar binários autônomos que não dependem de uma instalação prévia do Python no sistema do usuário.
- **Tecnologias:** Usar PyInstaller ou Nuitka para empacotar tudo em um único arquivo (.exe no Windows, binário no Linux/macOS).

#### 1.3 Gerenciadores de Pacotes Nativos
Integrar o projeto nos fluxos de instalação padrão de cada sistema operacional.
- **macOS/Linux:** Fórmulas para Homebrew.
- **Windows:** Manifesto para WinGet ou Chocolatey.
- **Linux:** Pacotes nativos (.deb, .rpm) ou AppImage.
    
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

### 6. Novos Renderizadores de Alta Resolução (Pixel-Perfect)
Explorar tecnologias para desenhar pixels reais em ambientes sem interface gráfica (X11/Wayland).

- **SixelRenderer**:
    - **Características**: Utiliza o protocolo Sixel para enviar bitmaps codificados como sequências de escape ANSI através do terminal.
    - **Aplicações**: Ideal para acessos remotos via **SSH**, WSL e terminais modernos (Kitty, iTerm2, VS Code). Permite ver desenhos em alta resolução dentro da própria janela do terminal.
- **FramebufferRenderer**:
    - **Características**: Escreve diretamente no dispositivo de memória de vídeo do kernel do Linux (`/dev/fb0`).
    - **Aplicações**: Uso em **TTY puro** (consoles de sistema sem interface gráfica instalada), sistemas embarcados (como Raspberry Pi "headless") ou em situações de recuperação de sistema onde não há emulador de terminal disponível. Requer acesso físico ou via console serial.

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
