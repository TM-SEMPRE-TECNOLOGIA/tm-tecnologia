@echo off
title TM Gerenciador

echo ============================================================
echo   TM Gerenciador - TM Sempre Tecnologia
echo   Frontend: http://localhost:3000
echo   Backend API: http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo ============================================================
echo.

:: Inicia Backend FastAPI
echo [1/2] Iniciando Backend FastAPI...
start "TM Gerenciador - API" cmd /k "cd /d "%~dp0backend" && .venv\Scripts\uvicorn.exe main:app --reload --port 8000"

:: Aguarda 2 segundos para o backend inicializar
timeout /t 2 /nobreak >nul

:: Inicia Frontend Next.js
echo [2/2] Iniciando Frontend Next.js...
start "TM Gerenciador - Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo Ambos os servicos foram iniciados em janelas separadas.
echo Aguarde alguns segundos e acesse http://localhost:3000
pause
