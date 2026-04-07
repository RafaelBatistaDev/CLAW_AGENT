@echo off
REM 🚀 SETUP RÁPIDO — CLAW VS Code Extension (Windows)
REM Instala e configura a extensão automaticamente
REM 
REM Uso:
REM   setup.bat                    - Setup completo
REM   setup.bat --dev              - Modo desenvolvimento (watch)
REM   setup.bat --package          - Empacotar .vsix para release

setlocal enabledelayedexpansion
cd /d "%~dp0"

if "%~1"=="" (
    set MODE=install
) else (
    set MODE=%~1
)

cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║  🚀 CLAW VS Code Extension - Setup Automático (Windows)
echo ║  Modo: %MODE%
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM ════════════════════════════════════════════════════════════════════════════════
REM 1. VALIDAR AMBIENTE
REM ════════════════════════════════════════════════════════════════════════════════

echo 📋 Validando ambiente...

where node >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js não encontrado. Instale em: https://nodejs.org
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node -v') do set NODE_VERSION=%%i
echo ✅ Node.js: %NODE_VERSION%

where npm >nul 2>&1
if errorlevel 1 (
    echo ❌ npm não encontrado
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('npm -v') do set NPM_VERSION=%%i
echo ✅ npm: %NPM_VERSION%

where code >nul 2>&1
if errorlevel 1 (
    echo ⚠️  VS Code não encontrado no PATH
    echo    (Pode instalar depois manualmente)
) else (
    for /f "tokens=1" %%i in ('code --version') do set VS_CODE_VERSION=%%i
    echo ✅ VS Code: %VS_CODE_VERSION%
)

if exist "%USERPROFILE%\OneDrive\ClawRafaelIA\automation\my_scripts\agent.py" (
    echo ✅ agent.py: encontrado
) else (
    echo ⚠️  agent.py não encontrado
    echo    (Extension funcionará com fallback local)
)

echo.

REM ════════════════════════════════════════════════════════════════════════════════
REM 2. INSTALAR DEPENDÊNCIAS
REM ════════════════════════════════════════════════════════════════════════════════

echo 📦 Instalando dependências...

if not exist ".npmrc" (
    echo audit=false > .npmrc
)

call npm install >nul 2>&1
if errorlevel 1 (
    echo ❌ Erro ao instalar dependências
    pause
    exit /b 1
)

echo ✅ Dependências instaladas
echo.

REM ════════════════════════════════════════════════════════════════════════════════
REM 3. COMPILAR
REM ════════════════════════════════════════════════════════════════════════════════

echo 🔨 Compilando TypeScript...

call npm run compile >nul 2>&1
if errorlevel 1 (
    echo ❌ Erro ao compilar
    pause
    exit /b 1
)

echo ✅ Compilação completa
echo.

REM ════════════════════════════════════════════════════════════════════════════════
REM 4. AÇÕES ESPECÍFICAS DO MODO
REM ════════════════════════════════════════════════════════════════════════════════

if "%MODE%"=="--dev" (
    echo ⌚ Modo DESENVOLVIMENTO (watch mode)
    echo Pressione Ctrl+C para parar
    call npm run dev
    exit /b 0
)

if "%MODE%"=="--package" (
    echo 📦 Empacotando para release...
    call npm run compile:prod >nul 2>&1
    call npm run package >nul 2>&1
    
    for /f "tokens=*" %%f in ('dir /b /od *.vsix 2^>nul ^| findstr /v ".*"') do (
        set VSIX_FILE=%%f
    )
    
    if defined VSIX_FILE (
        echo ✅ Pacote criado: %VSIX_FILE%
    ) else (
        echo ⚠️  .vsix não gerado
        echo    Execute: npm run package
    )
    exit /b 0
)

if "%MODE%"=="install" (
    echo 📥 Instalando extensão no VS Code...
    
    where code >nul 2>&1
    if errorlevel 1 (
        echo ⚠️  VS Code não encontrado
        echo    Após instalar VS Code, execute:
        echo    code --install-extension .clawrafaelia-suggestions.vsix
    ) else (
        call npm run package >nul 2>&1
        
        REM Procurar .vsix mais recente
        for /f "tokens=*" %%f in ('dir /b /od *.vsix 2^>nul') do (
            set VSIX_FILE=%%f
        )
        
        if defined VSIX_FILE (
            code --install-extension "%VSIX_FILE%" >nul 2>&1
            echo ✅ Extensão instalada
        ) else (
            echo ⚠️  .vsix não gerado
            echo    Execute: npm run package
        )
    )
    
    goto success
)

echo ❌ Modo desconhecido: %MODE%
echo.
echo Usos:
echo   setup.bat           - Install (padrão)
echo   setup.bat --dev     - Desenvolvimento (watch)
echo   setup.bat --package - Empacotar para release
pause
exit /b 1

:success
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║  ✅ Setup completado!
echo ║
echo ║  📖 Próximos passos:
echo ║     1. Abra VS Code
echo ║     2. Vá para Extensions (Ctrl+Shift+X)
echo ║     3. Procure por 'CLAW'
echo ║     4. Clique Install
echo ║
echo ║  ⚙️  Configurar em Settings:
echo ║     Ctrl+, → clawrafaelia
echo ║
echo ║  💻 Começar a digitar em qualquer arquivo!
echo ╚════════════════════════════════════════════════════════════════╝
echo.
pause
