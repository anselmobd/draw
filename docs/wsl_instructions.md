# Guia de Testes Cross-Distro no WSL

Este guia descreve o procedimento para testar o instalador e a execução do DRAW Interpreter em uma distribuição Linux "limpa" (ex: Ubuntu) utilizando o sistema de arquivos de outra distribuição (ex: Debian) no mesmo ambiente WSL.

Este cenário é ideal para validar o processo de instalação e desinstalação antes de publicar uma nova versão no GitHub.

## 1. Preparação do Ambiente

Suponha que você desenvolve no **Debian** e quer testar no **Ubuntu**.

### No Windows (PowerShell)
Temos que garantir que o disco da distribuição de desenvolvimento esteja montado. O WSL faz isso automaticamente, mas você pode acessar via:
`\\wsl.localhost\debian\home\anselmo\dev\draw`

### No Linux de Teste (Ubuntu)
Se a pasta da outra distro não estiver aparecendo automaticamente em `/mnt/`, você pode montá-la manualmente usando o protocolo `drvfs`:

```bash
# Cria o ponto de montagem
sudo mkdir -p /mnt/debian

# Monta a distribuição Debian (ajuste o nome se necessário)
sudo mount -t drvfs '//wsl.localhost/Debian' /mnt/debian
```

## 2. Configuração da Distribuição de Teste (Ubuntu)

No terminal da distribuição de teste, acesse a pasta do projeto via mount do WSL:

```bash
# O Windows monta as distros em /mnt/wsl ou /mnt/wsl/<nome_distro>
# Verifique o caminho exato na sua máquina
cd /mnt/debian/home/anselmo/dev/draw
```

### 2.1 Permissões do Git (Crucial)
O Git bloqueia acesso a pastas que pertencem a outros usuários por segurança. Como o Ubuntu "vê" os arquivos do Debian como de outro dono, você deve habilitar a confiança na pasta:

```bash
git config --global --add safe.directory /mnt/debian/home/anselmo/dev/draw
git config --global --add safe.directory /mnt/debian/home/anselmo/dev/draw/.git
```

## 3. Execução do Teste de Instalação

O instalador por padrão baixa o código do GitHub. Para testar suas **mudanças locais** (como correções no `pyproject.toml` ou no próprio código) sem dar `push`:

1. No diretório de desenvolvimento (Debian), edite o arquivo `scripts/install/install.sh`.
2. Altere temporariamente a variável `REPO_URL` para o caminho local:
   ```bash
   REPO_URL="/mnt/debian/home/anselmo/dev/draw"
   ```
3. No terminal de teste (Ubuntu), execute o instalador:
   ```bash
   bash /mnt/debian/home/anselmo/dev/draw/scripts/install/install.sh
   ```

## 4. Validação dos Comandos

Após a instalação, verifique se o comando global foi criado com sucesso:

1. **Atualize o PATH**:
   ```bash
   source ~/.bashrc
   ```
2. **Teste o comando**:
   ```bash
   draw "U10 R10 D10 L10"
   ```
3. **Verifique a versão**:
   ```bash
   draw --version
   ```

## 5. Teste de Desinstalação

Verifique se a limpeza do sistema está funcionando conforme esperado:

```bash
draw-uninstall
```
Certifique-se de que o comando `draw` não seja mais encontrado e que a pasta `~/.local/share/draw` foi removida.

## 6. Solução de Problemas Comuns

### Erro de Versão do Python
Se o instalador reclamar da versão do Python:
- Verifique o `requires-python` no `pyproject.toml`.
- Instale a versão necessária: `sudo apt update && sudo apt install python3.10-venv` (ou versão superior).

### Comando 'draw' não encontrado
- Certifique-se de que `~/.local/bin` está no seu `$PATH`.
- Se estiver usando um ambiente virtual (`venv`) ativado manualmente, o `draw` do venv terá prioridade sobre o `draw` instalado globalmente pelo script. Use `which draw` para confirmar qual binário está sendo usado.

---
**Nota:** Lembre-se de reverter a `REPO_URL` no `install.sh` para o endereço do GitHub antes de enviar as alterações para o repositório oficial.
