# Guia de Testes Automatizados

Este projeto utiliza o framework `pytest` para garantir a integridade da lógica de interpretação do motor DRAW, independentemente da interface visual utilizada.

## O MockRenderer

Para testar a lógica sem abrir janelas ou depender do terminal, foi criado o `MockRenderer` ([src/draw/renderers/mock_renderer.py](../src/draw/renderers/mock_renderer.py)). Ele simula um dispositivo de saída e armazena:
- Todas as linhas desenhadas (coordenadas e cores).
- Um histórico cronológico de todas as operações invocadas pela Engine.

## Como Rodar os Testes

Certifique-se de estar com o ambiente virtual ativado:

```bash
source .venv/bin/activate
```

Para executar todos os testes (graças à configuração no `pyproject.toml`):

```bash
python -m pytest
```

### Opções Úteis do Pytest

- **Ver mais detalhes**: `-v`
- **Exibir print() durante os testes**: `-s`
- **Parar no primeiro erro**: `-x`

## Estrutura de Testes

Os testes estão localizados na pasta `tests/` e cobrem:

1.  **Movimentos Básicos**: Verifica se `U`, `D`, `L`, `R` deslocam o cursor nas direções e distâncias corretas.
2.  **Prefixos Modificadores**: Garante que o prefixo `B` (Blind) não desenha linhas e que o prefixo `N` (No Update) mantém o cursor na posição original.
3.  **Transformações**:
    *   **Escala (`S`)**: Verifica se o tamanho do desenho é multiplicado corretamente.
    *   **Rotação (`A` / `TA`)**: Valida o cálculo trigonométrico das rotações no sentido anti-horário.
4.  **Cores**: Confirma se o índice de cor correto é enviado ao renderer.

## Adicionando Novos Testes

Sempre que adicionar uma nova funcionalidade à `DrawEngine`, crie um novo caso de teste em `tests/test_engine.py` utilizando o fixture `engine` para injetar o `MockRenderer`.

## Testes de Distribuição (WSL Cross-Distro)

Para testar o processo de instalação e desinstalação em ambientes Linux reais utilizando o WSL, consulte o [Guia de Testes WSL](wsl_instructions.md).

## Guia de Release

Para entender o fluxo completo de como gerar uma nova versão oficial do sistema, consulte o [Guia de Release](release_guide.md).

---

[Voltar ao README](../README.md)
