@echo off
chcp 65001 >nul
echo ========================================
echo   🎓 IA Pedagógico - Instalador
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Erro: Python não encontrado!
    echo.
    echo Por favor, instale Python 3.8+ de:
    echo https://www.python.org/downloads/
    echo.
    echo ⚠️  Importante: Marque "Add Python to PATH" durante a instalação
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado!
python --version
echo.

REM Criar ambiente virtual
echo 📦 Criando ambiente virtual...
python -m venv venv
echo.

REM Ativar ambiente virtual
echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat
echo.

REM Atualizar pip
echo 📥 Atualizando pip...
python -m pip install --upgrade pip
echo.

REM Instalar dependências
echo 📚 Instalando dependências...
echo (Isso pode levar alguns minutos)
echo.
pip install -r requirements.txt
echo.

REM Criar diretórios
echo 📁 Criando diretórios necessários...
if not exist "uploads" mkdir uploads
if not exist "output" mkdir output
if not exist "temp" mkdir temp
echo.

REM Verificar arquivo .env
if not exist ".env" (
    echo ⚠️  Arquivo .env não encontrado!
    echo.
    echo Para usar funcionalidades de IA, crie um arquivo .env
    echo Use env_example.txt como referência
    echo.
)

echo ========================================
echo   ✅ Instalação concluída!
echo ========================================
echo.
echo 🚀 Para iniciar o servidor:
echo    1. Execute: start.bat
echo    2. Ou digite: python app.py
echo.
echo 📖 Leia README.md para mais informações
echo.
pause

