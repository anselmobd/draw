# =================================================================
# DRAW Interpreter - Instalador para Windows (PowerShell)
# =================================================================

$InstallDir = "$HOME\AppData\Local\draw"
$BinDir = "$HOME\AppData\Local\Microsoft\WindowsApps"
$RepoUrl = "https://github.com/anselmobd/draw.git"

$ErrorActionPreference = "Stop"

Write-Host "----------------------------------------------------" -ForegroundColor Cyan
Write-Host "  Iniciando instalação do DRAW Interpreter" -ForegroundColor Cyan
Write-Host "----------------------------------------------------" -ForegroundColor Cyan

# 1. Verificar se o Python está instalado
try {
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if (!$pythonCmd) {
        throw "Python não encontrado"
    }
} catch {
    Write-Host "ERRO: Python não encontrado!" -ForegroundColor Red
    Write-Host "O DRAW Interpreter precisa do Python para rodar via script." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Sugestão de instalação:" -ForegroundColor Yellow
    Write-Host "  - Execute no terminal: winget install Python.Python.3.10" -ForegroundColor White
    Write-Host "  - Ou baixe em: https://python.org" -ForegroundColor White
    Write-Host ""
    Write-Host "DICA: No futuro, teremos uma versão .EXE que não exige Python." -ForegroundColor Cyan
    exit 1
}

# 2. Criar diretórios
Write-Host "[1/4] Criando pastas em $InstallDir..."
if (!(Test-Path $InstallDir)) { New-Item -ItemType Directory -Path $InstallDir | Out-Null }

# 3. Baixar código (Simplificado para o exemplo, assumindo que tem Git ou baixando via WebClient)
Write-Host "[2/4] Preparando código..."
if (Test-Path "$InstallDir\repo") {
    Set-Location "$InstallDir\repo"
    git pull
} else {
    git clone $RepoUrl "$InstallDir\repo"
}

# 4. Criar Venv e Instalar
Write-Host "[3/4] Configurando ambiente isolado (venv)..."
python -m venv "$InstallDir\venv"
& "$InstallDir\venv\Scripts\pip.exe" install --upgrade pip
& "$InstallDir\venv\Scripts\pip.exe" install -e "$InstallDir\repo"

# 5. Criar o comando global (Bat wrapper)
Write-Host "[4/4] Criando atalho draw.bat..."
$BatContent = @"
@echo off
"$InstallDir\venv\Scripts\draw.exe" %*
"@
$BatContent | Out-File -FilePath "$BinDir\draw.bat" -Encoding ASCII

# 5.1 Criar o desinstalador
Write-Host "[4.1/4] Criando desinstalador..."
$UninstallScript = @"
Write-Host "Removendo DRAW Interpreter..." -ForegroundColor Yellow
if (Test-Path "$BinDir\draw.bat") { Remove-Item -Force "$BinDir\draw.bat" }
if (Test-Path "$BinDir\draw-uninstall.bat") { Remove-Item -Force "$BinDir\draw-uninstall.bat" }
if (Test-Path "$InstallDir") { Remove-Item -Recurse -Force "$InstallDir" }
Write-Host "DRAW Interpreter removido com sucesso." -ForegroundColor Green
"@
$UninstallScript | Out-File -FilePath "$InstallDir\uninstall.ps1" -Encoding UTF8

$UninstallBatContent = @"
@echo off
powershell -ExecutionPolicy Bypass -File "$InstallDir\uninstall.ps1"
"@
$UninstallBatContent | Out-File -FilePath "$BinDir\draw-uninstall.bat" -Encoding ASCII

# 6. Finalização
Write-Host "----------------------------------------------------" -ForegroundColor Green
Write-Host "  Instalação Concluída com Sucesso!" -ForegroundColor Green
Write-Host "----------------------------------------------------" -ForegroundColor Green
Write-Host "Você já pode usar o comando: draw" -ForegroundColor White
Write-Host "Para desinstalar, use: draw-uninstall" -ForegroundColor White
Write-Host ""
Write-Host "Se o comando não for reconhecido, reinicie o terminal." -ForegroundColor Yellow
Write-Host "----------------------------------------------------" -ForegroundColor Green
