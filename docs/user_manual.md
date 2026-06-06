# Manual do Usuário - DRAW Interpreter

O **DRAW Interpreter** é uma ferramenta versátil para criar desenhos vetoriais e pixel art usando comandos simples inspirados no comando `DRAW` do BASIC clássico. Ele suporta renderização em tempo real tanto em janelas gráficas quanto no terminal.

---

## 🕹️ Como Executar

A execução é feita através do script principal `run.py`. Você pode passar uma string de comandos diretamente ou carregar um arquivo.

### Comandos Rápidos
```bash
# Desenhar um triângulo no modo gráfico
python run.py "TA45 U10 R10 D10"

# Desenhar o mesmo triângulo no console (terminal)
python run.py -a c "TA45 U10 R10 D10"

# Carregar comandos de um arquivo
python run.py -f meus_comandos.txt
```

---

## 🛠️ Opções de Linha de Comando (CLI)

| Argumento | Descrição |
| :--- | :--- |
| `command` | String de comandos DRAW para execução imediata (ex: `"C4 U10"`). |
| `-h, --help` | Exibe a mensagem de ajuda e sai. |
| `-f, --file PATH` | Carrega e executa comandos DRAW de um arquivo de texto. |
| `-t, --test` | Executa os desenhos de demonstração (`assets/teste_...`). |
| `-s, --slow ms` | Adiciona um atraso em milissegundos entre cada comando (ideal para ver animação). |
| `-a, --app {g,c}` | Escolha entre **g** (gráfico/Tkinter, padrão) ou **c** (console/terminal). |
| `-m, --mock` | Modo de auditoria: exibe as coordenadas calculadas no console sem desenhar. |
| `-F, --fullscreen` | Abre a janela gráfica em modo tela cheia (apenas modo gráfico). |
| `-M, --maximize` | Abre a janela gráfica maximizada (apenas modo gráfico). |
| `-p, --pixel-size n` | Define o tamanho físico do pixel (ex: `2` para 2x2, `2x4` para retangular). |

---

## 🎨 Guia de Comandos DRAW

O interpretador processa sequências de letras seguidas por números. Espaços e vírgulas são opcionais.

### Movimentação Básica
- **U n**: Move para Cima (*Up*) `n` unidades.
- **D n**: Move para Baixo (*Down*) `n` unidades.
- **L n**: Move para a Esquerda (*Left*) `n` unidades.
- **R n**: Move para a Direita (*Right*) `n` unidades.

### Diagonais
- **E n**: Nordeste (Cima + Direita).
- **F n**: Sudeste (Baixo + Direita).
- **G n**: Sudoeste (Baixo + Esquerda).
- **H n**: Noroeste (Cima + Esquerda).

### Posicionamento e Rotação
- **M x,y**: Move para a coordenada absoluta `(x,y)`.
- **M +x,+y**: Move para a coordenada relativa à posição atual.
- **A n**: Rotaciona o desenho em 90° (n = 0 a 3).
- **TA n**: Rotaciona em um ângulo arbitrário (0-359 graus).

### Estética e Estado
- **C n**: Muda a cor (0-15).
- **S n**: Muda a escala lógica do desenho (padrão é 4).
- **B**: Prefixo "Blind". Move sem desenhar a linha. (Ex: `BU10`)
- **N**: Prefixo "No Update". Desenha mas retorna o cursor ao ponto inicial. (Ex: `NU10`)

---

## 👾 Recurso Especial: Pixel Art e Proporção

Você pode gerar artes pixeladas ajustando o tamanho do "pixel físico" via CLI. Isso é diferente da escala `S`, pois altera a espessura da linha e a resolução disponível da tela.

**Exemplo:**
```bash
# Pixels gigantes quadrados de 10x10
python run.py -p 10 "TA45 C4 U8 R8 D8 L8"

# Pixels retangulares (estilo monitores antigos)
python run.py -p 2x4 "C14 U10 R10 D10 L10"
```

---

## ⌨️ Comandos do Teclado
Após o término de um desenho, a janela gráfica ou o terminal aguardará uma interação:
- **Qualquer Tecla**: Fecha o programa ou limpa o terminal.
- **ESC** (Modo Gráfico): Fecha a janela.
