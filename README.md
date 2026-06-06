# DRAW Interpreter

Um interpretador unificado para o comando `DRAW` (inspirado no clássico BASIC), com suporte a renderização gráfica via Tkinter e renderização em texto via Terminal (ANSI).

O projeto utiliza uma arquitetura modular que separa a lógica de interpretação da trajetória (Engine) da implementação visual (Renderers), permitindo fácil expansão para novas interfaces.

## 🚀 Funcionalidades

- **Renderização Dupla:** Escolha entre uma janela gráfica (`Tkinter`) ou o terminal (`ANSI`).
- **Comandos Clássicos:** Suporte a `U`, `D`, `L`, `R`, `E`, `F`, `G`, `H`, `M`, `C`, `S`, `A`, `TA`.
- **Modos Avançados:** Suporte a comandos `B` (Blind - mover sem desenhar) e `N` (No Update - desenhar sem mover o cursor).
- **Controle de Velocidade:** Parâmetro `--slow` para visualizar o desenho passo a passo.

Para mais detalhes sobre como usar o programa, a arquitetura do projeto e o funcionamento interno, consulte os links abaixo:

- [📖 Manual do Usuário](docs/user_manual.md)
- [🛠️ Detalhes Técnicos](docs/technical_details.md)
- [🧪 Guia de Testes](docs/testing.md)
- [📋 Backlog de Melhorias](docs/backlog.md)

## 🛠️ Como Usar

### Pré-requisitos
- Python 3.10+
- Tkinter (geralmente incluso no Python)

### Execução

Use o script `run.py` na raiz do projeto:

```bash
# Executar o teste padrão (Gráfico)
python run.py -t

# Executar o teste padrão no Console
python run.py -a c -t

# Executar o mock das coordenadas (respeitando a resolução do modo gráfico)
python run.py -m "C4 U40 R40 D40"

# Executar o mock das coordenadas (respeitando a resolução do terminal/console)
python run.py -a c -m "C4 U10 R10 D10"
```

> **Nota:** Após a execução do desenho, o programa aguardará que você pressione **qualquer tecla** para encerrar (fechar a janela ou retornar ao prompt). No console, nenhuma mensagem é exibida para não interferir no visual do desenho. O modo **Mock** (`-m`) não requer espera e encerra imediatamente após listar as coordenadas.

### Argumentos Principais
- `command` (posicional): Sequência de comandos DRAW (ex: `"C4 U10 R10"`).
- `-a, --app {g,c}`: Seleciona o renderizador (g = gráfico, c = console).
- `-p, --pixel-size`: Define o tamanho físico do pixel (ex: `2` ou `2x3`).
- `-m, --mock`: Ativa o modo auditoria (lista coordenadas no console).
- `-t, --test`: Executa desenhos de demonstração.
- `-s, --slow [ms]`: Atraso entre comandos para visualização passo a passo.
- `-f, --file [PATH]`: Carrega comandos de um arquivo de texto.
- `-h, --help`: Lista todas as opções disponíveis.

Consulte o [Manual do Usuário](docs/user_manual.md) para a lista completa e detalhada de comandos e opções.

## 🎨 Tabela de Comandos DRAW

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
