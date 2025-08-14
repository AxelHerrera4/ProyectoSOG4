@echo off
title Instalador de Dependencias - Administrador de Tareas
color 0B
echo.
echo ========================================
echo     INSTALADOR DE DEPENDENCIAS
echo ========================================
echo.
echo Instalando dependencias necesarias...
echo.

REM Cambiar al directorio del proyecto
cd /d "D:\ProyectoSOG4"

echo Verificando Python...
python --version
echo.

echo Instalando dependencias del sistema...
echo.

echo Instalando psutil...
pip install psutil
echo.

echo Instalando matplotlib...
pip install matplotlib
echo.

echo Instalando pandas...
pip install pandas
echo.

echo Instalando pillow...
pip install pillow
echo.

echo Instalacion completada!
echo.
echo Ahora puede ejecutar el administrador de tareas con:
echo    - Doble clic en ejecutar.bat
echo    - python main.py
echo.
pause
