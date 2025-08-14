#!/usr/bin/env python3
"""
Administrador de Tareas - Punto de entrada principal
Interfaz gráfica para gestión de procesos del sistema
"""

import os
import sys

def main():
    """Función principal"""
    try:
        # Verificar dependencias críticas
        missing_deps = []
        
        try:
            import psutil
        except ImportError:
            missing_deps.append("psutil")
        
        try:
            import matplotlib
        except ImportError:
            missing_deps.append("matplotlib")
        
        try:
            import tkinter
        except ImportError:
            missing_deps.append("tkinter")
        
        if missing_deps:
            print("Error: Faltan dependencias requeridas:")
            for dep in missing_deps:
                print(f"  - {dep}")
            print("\nSolución: pip install", " ".join(missing_deps))
            input("\nPresione Enter para salir...")
            return
        
        # Iniciar aplicación
        from task_manager_gui_clean import TaskManagerGUI
        app = TaskManagerGUI()
        app.run()
        
    except ImportError as e:
        print(f"Error de importación: {e}")
        print("Instale las dependencias: pip install psutil matplotlib pandas pillow")
        input("Presione Enter para salir...")
    except KeyboardInterrupt:
        print("Aplicación cerrada por el usuario")
    except Exception as e:
        print(f"Error al iniciar: {e}")
        input("Presione Enter para salir...")

if __name__ == "__main__":
    main()
