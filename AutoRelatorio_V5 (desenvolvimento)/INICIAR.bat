@echo off
title AutoRelatorio V5 — Iniciando...
echo.
echo  ╔══════════════════════════════════════════════╗
echo  ║         AutoRelatório V5 — Iniciar           ║
echo  ║  Backend (porta 5000) + Frontend (porta 3000) ║
echo  ╚══════════════════════════════════════════════╝
echo.

:: Backend Python
echo [1/2] Iniciando backend Python (FastAPI)...
start "AutoRelatório V5 — Backend" cmd /k "cd /d %~dp0backend && python -m uvicorn core.server:app --host 0.0.0.0 --port 5000 --reload"

:: Aguarda 2 segundos para o backend iniciar
timeout /t 2 /nobreak > nul

:: Frontend Next.js
echo [2/2] Iniciando frontend Next.js...
start "AutoRelatório V5 — Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo  Backend:  http://localhost:5000
echo  Frontend: http://localhost:3000
echo  Docs API: http://localhost:5000/docs
echo.
echo  Aguarde o frontend compilar e acesse http://localhost:3000
echo.
pause
