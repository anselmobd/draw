# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Adicionado
- 

### Corrigido
- 

## [0.1.0] - 2026-06-07

### Adicionado
- Estrutura inicial do projeto com motor `DrawEngine`.
*   Renderizadores: `ConsoleRenderer` (ANSI), `TkinterRenderer` (GUI) e `MockRenderer`.
- Suporte a comandos clássicos do comando DRAW do BASIC (U, D, L, R, E, F, G, H, M, C, S, A, TA, B, N).
- Sistema de ajuda dinâmica com `--help-draw`.
- Padrão Context Manager para limpeza automática de recursos (janelas e terminal).
- Modo de instalação CLI via `pip` com comandos `draw` e `pydraw`.
- Redimensionamento dinâmico (redesenho) em tempo real.
- Suporte a keypad Enter para fechar no modo gráfico.
- Scripts de instalação automatizada (`install.sh` e `install.ps1`) em `scripts/install/`.
