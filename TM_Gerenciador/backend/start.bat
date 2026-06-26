@echo off
cd /d "%~dp0"
.venv\Scripts\uvicorn.exe main:app --reload --port 8000
