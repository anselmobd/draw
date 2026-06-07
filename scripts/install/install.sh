#!/bin/bash

# =================================================================
# DRAW Interpreter - Instalador para Linux e macOS
# =================================================================

INSTALL_DIR="$HOME/.local/share/draw"
BIN_DIR="$HOME/.local/bin"
REPO_URL="https://github.com/anselmobd/draw.git"

set -e

echo "----------------------------------------------------"
echo "  Iniciando instalação do DRAW Interpreter"
echo "----------------------------------------------------"

# 1. Verificar se o Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python 3 não encontrado!"
    echo "O DRAW Interpreter precisa do Python 3 para rodar via script."
    echo ""
    echo "Sugestões de instalação:"
    echo "  - Linux (Ubuntu/Debian): sudo apt update && sudo apt install python3 python3-venv"
    echo "  - macOS: brew install python"
    echo "  - Ou visite: https://www.python.org/downloads/"
    echo ""
    echo "DICA: No futuro, teremos uma versão 'Standalone' que não exige Python."
    exit 1
fi

# 2. Criar diretórios de destino
echo "[1/4] Criando pastas em $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

# 3. Baixar ou atualizar o código
echo "[2/4] Baixando código do repositório..."
if [ -d "$INSTALL_DIR/repo" ]; then
    echo "Atualizando instalação existente..."
    cd "$INSTALL_DIR/repo" && git pull
else
    git clone "$REPO_URL" "$INSTALL_DIR/repo"
fi

# 4. Criar Ambiente Virtual e Instalar
echo "[3/4] Configurando ambiente isolado (venv)..."
python3 -m venv "$INSTALL_DIR/venv"
"$INSTALL_DIR/venv/bin/pip" install --upgrade pip
"$INSTALL_DIR/venv/bin/pip" install -e "$INSTALL_DIR/repo"

# 5. Criar o comando global (Wrapper)
echo "[4/4] Criando atalho em $BIN_DIR/draw..."
cat <<EOF > "$BIN_DIR/draw"
#!/bin/bash
# Wrapper gerado automaticamente pelo instalador do DRAW
"$INSTALL_DIR/venv/bin/draw" "\$@"
EOF

chmod +x "$BIN_DIR/draw"

# 6. Finalização
echo "----------------------------------------------------"
echo "  Instalação Concluída com Sucesso!"
echo "----------------------------------------------------"
echo "Você já pode usar o comando: draw"
echo ""
echo "Nota: Certifique-se de que '$BIN_DIR' está no seu PATH."
echo "Se 'draw' não funcionar, adicione esta linha ao seu .bashrc ou .zshrc:"
echo "export PATH=\"\$PATH:$BIN_DIR\""
echo "----------------------------------------------------"
