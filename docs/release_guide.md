# Procedimento de Release (Lançamento de Versão)

Este documento descreve os passos necessários para preparar e publicar uma nova versão do DRAW Interpreter.

## 1. Preparação na Branch de Feature

Antes de iniciar o lançamento, garanta que todas as funcionalidades e correções estão commits na sua branch de trabalho (ex: `feature/nova-funcionalidade`).

### Atualizar o Changelog
Garanta que o arquivo `CHANGELOG.md` contém todas as mudanças relevantes na seção `[Unreleased]`.

### Validar Localmente
Execute os testes automatizados:
```bash
python -m pytest
```

---

## 2. Incremento de Versão (Automatico)

Utilize o `bumpver` para atualizar a versão em todos os arquivos de configuração simultaneamente.

1. **Simular o incremento (Dry Run):**
   ```bash
   # Escolha entre --patch (0.0.x), --minor (0.x.0) ou --major (x.0.0)
   ./.venv/bin/python -m bumpver update --patch --dry
   ```

2. **Aplicar o incremento:**
   Este comando irá atualizar os arquivos, criar um commit de "bump" e gerar uma tag Git local.
   ```bash
   ./.venv/bin/python -m bumpver update --patch
   ```

---

## 3. Fluxo de Integração (Git Flow)

O processo de integração segue o modelo de Pull Requests para garantir a integridade da branch principal.

### Passo A: Feature -> Develop
1. Faça o push da sua branch e da tag para o GitHub:
   ```bash
   git push origin <nome-da-branch> --tags
   ```
2. No GitHub, abra um **Pull Request** da sua branch para a `develop`.
3. Após a revisão, realize o merge.

### Passo B: Teste Final (Ambiente Real)
Utilize o procedimento descrito em [Guia de Testes WSL](wsl_instructions.md) para validar a instalação a partir da branch `develop`.

### Passo C: Develop -> Main (Release Oficial)
1. No GitHub, abra um **Pull Request** de `develop` para `main`.
2. Este merge representa o lançamento oficial da versão estável.
3. Após o merge, atualize seu ambiente local:
   ```bash
   git checkout main
   git pull origin main
   ```

---

## 4. Publicação do Release no GitHub

Para que comandos como o `curl | bash` funcionem corretamente apontando para a `main`, o código precisa estar lá.

1. No GitHub, vá em **Releases** > **Draft a new release**.
2. Escolha a tag que você criou (ex: `v0.1.1`).
3. Utilize o conteúdo do `CHANGELOG.md` para a descrição.
4. Publique o Release.

---

## 5. Checklist de Reversão (Importante)

Se você alterou o `REPO_URL` no `scripts/install/install.sh` para testar localmente, **certifique-se de que ele aponta para o GitHub antes do merge na main**:
`REPO_URL="https://github.com/anselmobd/draw.git"`

---
**Nota:** Este processo garante consistência entre o código, a versão exibida pelo programa (`draw -v`) e os scripts de instalação.
