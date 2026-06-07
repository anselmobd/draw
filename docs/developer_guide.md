# Guia do Desenvolvedor - DRAW Interpreter

Este documento é destinado a desenvolvedores que desejam contribuir para o projeto, entender a arquitetura interna ou executar o código diretamente da fonte.

## Execução via Script (Fonte)

Para desenvolvedores, a execução pode ser feita através do script `run.py` na raiz do projeto ou via `python -m draw`.

### Comando run.py

```bash
# Executar o teste padrão no Console (Padrão)
python run.py -t

# Executar o teste padrão no modo Gráfico
python run.py -a g -t

# Executar o mock das coordenadas (respeitando a resolução do console)
python run.py -m "C4 U40 R40 D40"

# Executar o mock das coordenadas (respeitando a resolução do modo gráfico)
python run.py -a g -m "C4 U10 R10 D10"
```

### Argumentos Principais (Desenvolvimento)
- `command` (posicional): Sequência de comandos DRAW (ex: `"C4 U10 R10"`).
- `-a, --app {g,c}`: Seleciona o renderizador (g = gráfico, c = console). Padrão: c.
- `-p, --pixel-size`: Define o tamanho físico do pixel (ex: `2` ou `2x3`).
- `-m, --mock`: Ativa o modo auditoria (lista coordenadas no console).
- `-t, --test`: Executa desenhos de demonstração.
- `-s, --slow [ms]`: Atraso entre comandos para visualização passo a passo.
- `-f, --file [PATH]`: Carrega comandos de um arquivo de texto.

---

## Documentação Técnica Relacionada

- [Detalhes Técnicos](technical_details.md): Decisões de arquitetura e lógica interna.
- [Guia de Testes](testing.md): Como executar e criar novos testes.
- [Backlog de Melhorias](backlog.md): Caminho planejado para o projeto.
- [Criar Novo Renderer](renderer_creation_guide.md): Instruções para expandir as saídas do sistema.

---

[Voltar ao README](../README.md)
