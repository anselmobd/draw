# DRAW Interpreter

Um interpretador unificado para o comando `DRAW` (inspirado no clássico BASIC), com suporte a renderização gráfica via Tkinter e renderização em texto via Terminal (ANSI).

O projeto utiliza uma arquitetura modular que separa a lógica de interpretação da trajetória (Engine) da implementação visual (Renderers), permitindo fácil expansão para novas interfaces.

## Funcionalidades

- **Renderização Dupla:** Escolha entre uma janela gráfica (`Tkinter`) ou o terminal (`ANSI`).
- **Comandos Clássicos:** Suporte a `U`, `D`, `L`, `R`, `E`, `F`, `G`, `H`, `M`, `C`, `S`, `A`, `TA`.
- **Modos Avançados:** Suporte a comandos `B` (Blind - mover sem desenhar) e `N` (No Update - desenhar sem mover o cursor).
- **Controle de Velocidade:** Parâmetro `--slow` para visualizar o desenho passo a passo.

Para mais detalhes sobre como usar o programa e os comandos disponíveis, consulte:

- [Manual do Usuário](docs/user_manual.md)

Para desenvolvedores e contribuidores:
- [Guia do Desenvolvedor](docs/developer_guide.md)

## Instalação Rápida (Para Usuários)

Se você deseja apenas utilizar o comando `draw` no seu sistema sem configurar ambientes de desenvolvimento:

### Linux / macOS (Bash)
```bash
# Baixa e executa o instalador automático
curl -sSL https://raw.githubusercontent.com/anselmobd/draw/main/scripts/install/install.sh | bash
```

### Windows (PowerShell)
```powershell
# Baixa e executa o instalador automático
iwr -useb https://raw.githubusercontent.com/anselmobd/draw/main/scripts/install/install.ps1 | iex -Encoding UTF8
```

*Nota: Os scripts acima configuram um ambiente isolado e criam o comando global `draw`. Requer Python 3 instalado. Para remover o programa, você pode usar o comando `draw-uninstall` que será criado durante a instalação.*

## Como Usar

Após a instalação, você pode usar o comando `draw` diretamente no seu terminal:

```bash
# Desenhar um triângulo no terminal (Console - Padrão)
draw "TA45 U10 R10 D10"

# Desenhar em uma janela gráfica (Tkinter)
draw -a g "C12 U10 R10 D10 L10"

# Ver a ajuda de comandos
draw --help-draw
```

> **Nota:** Após o desenho, o programa aguardará você pressionar **Enter** ou **Espaço** para encerrar. No modo console, nenhuma mensagem é exibida para não interferir no visual. Você pode interromper a qualquer momento com **Ctrl+C**.

## Tabela de Comandos DRAW

| Comando | Descrição |
| :--- | :--- |
| **U, D, L, R** | Move e desenha para Cima, Baixo, Esquerda e Direita. |
| **E, F, G, H** | Move e desenha nas diagonais (NE, SE, SW, NW). |
| **M x,y** | Move para coordenada absoluta ou relativa (+x,+y). |
| **C n** | Define a cor (0-15). |
| **S n** | Define a escala (padrão 4). |
| **A n** | Rotaciona em múltiplos de 90° (0-3). |
| **TA n** | Rotaciona em um ângulo específico (0-359). |
| **B** | Prefixo para mover sem desenhar. |
| **N** | Prefixo para desenhar sem atualizar a posição final. |

## Licença

Este projeto está licenciado sob a licença **BSD 3-Clause** - veja o arquivo [LICENSE](LICENSE) para detalhes.

