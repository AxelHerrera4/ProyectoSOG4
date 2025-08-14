@echo off
title Administrador de Tareas
color 0A
echo.
echo ========================================
echo     ADMINISTRADOR DE TAREAS
echo ========================================
echo.
echo Iniciando interfaz grafica...
echo Verificando entorno...
echo.

REM Cambiar al directorio del proyecto
cd /d "D:\ProyectoSOG4"

REM Verificar si existe el entorno virtual
if exist ".venv\Scripts\python.exe" (
    echo Entorno virtual encontrado
    echo Usando Python del entorno virtual...
    echo.
    ".venv\Scripts\python.exe" main.py
) else (
    echo Entorno virtual no encontrado
    echo Intentando con Python del sistema...
    echo.
    python main.py
)

echo.
echo Aplicacion cerrada
echo.
pause
