# DRAW Interpreter

Um interpretador unificado para o comando `DRAW` (inspirado no clássico BASIC), com suporte a renderização gráfica via Tkinter e renderização em texto via Terminal (ANSI).

O projeto utiliza uma arquitetura modular que separa a lógica de interpretação da trajetória (Engine) da implementação visual (Renderers), permitindo fácil expansão para novas interfaces.

## 🚀 Funcionalidades

- **Renderização Dupla:** Escolha entre uma janela gráfica (`Tkinter`) ou o terminal (`ANSI`).
- **Comandos Clássicos:** Suporte a `U`, `D`, `L`, `R`, `E`, `F`, `G`, `H`, `M`, `C`, `S`, `A`, `TA`.
- **Modos Avançados:** Suporte a comandos `B` (Blind - mover sem desenhar) e `N` (No Update - desenhar sem mover o cursor).
- **Controle de Velocidade:** Parâmetro `--slow` para visualizar o desenho passo a passo.

Para mais detalhes sobre a arquitetura do projeto e o funcionamento do motor de alta resolução para terminal, consulte os [Detalhes Técnicos](docs/technical_details.md).

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

# Executar uma string de comandos específica
python run.py "C4 U40 R40 D40 L40"

# Executar a partir de um arquivo
python run.py -f assets/desenho.txt
```

> **Nota:** Após a execução do desenho, o programa aguardará que você pressione **qualquer tecla** para encerrar (fechar a janela ou retornar ao prompt). No console, nenhuma mensagem é exibida para não interferir no visual do desenho.

### Argumentos
- `command` (posicional): Uma string contendo comandos DRAW para execução direta.
- `-a, --app {g,c}`: Seleciona o renderizador (g = gráfico, c = console).
- `-t, --test`: Executa os desenhos de demonstração.
- `-s, --slow [ms]`: Define um atraso em milissegundos entre cada comando.
- `-f, --file [PATH]`: Carrega comandos de um arquivo de texto.

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
