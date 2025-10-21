@echo off
chcp 65001 >nul
echo ========================================
echo   🎓 IA Pedagógico
echo   Iniciando servidor...
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
    pause
    exit /b 1
)

REM Criar diretórios necessários
if not exist "uploads" mkdir uploads
if not exist "output" mkdir output
if not exist "temp" mkdir temp

REM Ativar ambiente virtual se existir
if exist "venv\Scripts\activate.bat" (
    echo 📦 Ativando ambiente virtual...
    call venv\Scripts\activate.bat
)

REM Verificar se dependências estão instaladas
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo 📥 Instalando dependências...
    echo.
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    echo.
)

REM Iniciar servidor
echo.
echo ✅ Servidor iniciando em http://localhost:8000
echo.
echo 💡 Pressione Ctrl+C para parar o servidor
echo ========================================
echo.

python app.py

pause

