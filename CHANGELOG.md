# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Adicionado
- 

### Corrigido
- 

## [0.1.1] - 2026-06-07

### Adicionado
- Guia de release (`docs/release_guide.md`) e documentação detalhada de testes (`docs/testing.md`).
- Configuração automática do `$PATH` no instalador Shell para melhor experiência do usuário final.

### Corrigido
- Ajuste nos padrões de arquivo do `bumpver` para suporte correto ao formato do Changelog.

## [0.1.0] - 2026-06-07

### Adicionado
- Estrutura inicial do projeto com motor `DrawEngine`.
- Renderizadores: `ConsoleRenderer` (ANSI), `TkinterRenderer` (GUI) e `MockRenderer`.
- Suporte a comandos clássicos do comando DRAW do BASIC (U, D, L, R, E, F, G, H, M, C, S, A, TA, B, N).
- Sistema de ajuda dinâmica com `--help-draw`.
- Padrão Context Manager para limpeza automática de recursos (janelas e terminal).
- Modo de instalação CLI via `pip` com comandos `draw` e `pydraw`.
- Redimensionamento dinâmico (redesenho) em tempo real.
- Suporte a keypad Enter para fechar no modo gráfico.
- Scripts de instalação automatizada (`install.sh` e `install.ps1`) com suporte a `draw-uninstall`.
- Guia de testes Cross-Distro para WSL em `docs/wsl_instructions.md`.
- Automação de versão configurada com `bumpver`.

### Alterado
- Output padrão alterado de gráfico (GUI) para texto (Console).
- Requisito mínimo do Python reduzido para 3.10 para maior compatibilidade.
- Comportamento de saída: o programa agora aguarda especificamente **ENTER** ou **ESPAÇO** para encerrar.
- Importação preguiçosa (`lazy import`) do Tkinter para permitir execução em servidores headless.

### Corrigido
- Interrupção por `Ctrl+C` agora exibe um aviso amigável em vez de traceback.
- Tratamento de erros aprimorado para dependências de sistema ausentes (`tkinter`, `venv`).
