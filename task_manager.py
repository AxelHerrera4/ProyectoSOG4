#!/usr/bin/env python3
"""
Administrador de Tareas - Sistema Operativo
Un administrador de tareas simple para visualizar y administrar procesos del sistema
"""

import psutil
import os
import sys

class TaskManager:
    def __init__(self):
        """Inicializa el administrador de tareas"""
        print("=== Administrador de Tareas ===")
        print("Iniciando sistema...")
    
    def mostrar_menu(self):
        """Muestra el menú principal de opciones"""
        print("\n" + "="*50)
        print("       ADMINISTRADOR DE TAREAS")
        print("="*50)
        print("1. Mostrar información del sistema")
        print("2. Ver procesos")
        print("3. Matar proceso")
        print("4. Buscar procesos")
        print("0. Salir")
        print("="*50)

    def ejecutar(self):
        """Ejecuta el bucle principal del programa"""
        try:
            while True:
                self.mostrar_menu()
                try:
                    opcion = input("\nSeleccione una opción (0-4): ").strip()
                    
                    if opcion == '1':
                        self.mostrar_info_sistema()
                    elif opcion == '2':
                        self.ver_procesos()
                    elif opcion == '3':
                        self.matar_proceso()
                    elif opcion == '4':
                        self.buscar_procesos()
                    elif opcion == '0':
                        print("\n¡Gracias por usar el Administrador de Tareas!")
                        break
                    else:
                        print("Error: Opción no válida. Por favor, seleccione una opción del 0 al 4.")
                    
                    input("\nPresione Enter para continuar...")
                    
                except KeyboardInterrupt:
                    print("\n\n¡Gracias por usar el Administrador de Tareas!")
                    break
                except Exception as e:
                    print(f"Error inesperado: {e}")
                    input("Presione Enter para continuar...")
                    
        except Exception as e:
            print(f"Error crítico: {e}")
    
    def mostrar_info_sistema(self):
        """Muestra información básica del sistema"""
        print("\n--- INFORMACIÓN DEL SISTEMA ---")
        try:
            # Información de CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            print(f"CPU:")
            print(f"  - Uso actual: {cpu_percent}%")
            print(f"  - Núcleos: {cpu_count}")
            if cpu_freq:
                print(f"  - Frecuencia: {cpu_freq.current:.2f} MHz")
            
            # Información de memoria
            memory = psutil.virtual_memory()
            print(f"\nMemoria:")
            print(f"  - Total: {memory.total / (1024**3):.2f} GB")
            print(f"  - Usada: {memory.used / (1024**3):.2f} GB")
            print(f"  - Disponible: {memory.available / (1024**3):.2f} GB")
            print(f"  - Porcentaje usado: {memory.percent}%")
            
            # Información de disco
            disk = psutil.disk_usage('/')
            print(f"\nDisco:")
            print(f"  - Total: {disk.total / (1024**3):.2f} GB")
            print(f"  - Usado: {disk.used / (1024**3):.2f} GB")
            print(f"  - Libre: {disk.free / (1024**3):.2f} GB")
            
        except Exception as e:
            print(f"Error al obtener información del sistema: {e}")
    
    def ver_procesos(self):
        """Muestra una lista de procesos activos"""
        print("\n--- PROCESOS ACTIVOS ---")
        print(f"{'PID':<8} {'Nombre':<25} {'CPU%':<8} {'Memoria%':<10} {'Estado':<12}")
        print("-" * 70)
        
        try:
            # Obtener lista de procesos
            procesos = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    procesos.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Ordenar por uso de CPU (descendente)
            procesos.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            
            # Mostrar los primeros 20 procesos
            for i, proc in enumerate(procesos[:20]):
                pid = proc['pid']
                name = proc['name'][:24] if proc['name'] else 'N/A'
                cpu = f"{proc['cpu_percent']:.1f}" if proc['cpu_percent'] else '0.0'
                memory = f"{proc['memory_percent']:.1f}" if proc['memory_percent'] else '0.0'
                status = proc['status'][:11] if proc['status'] else 'N/A'
                
                print(f"{pid:<8} {name:<25} {cpu:<8} {memory:<10} {status:<12}")
                
        except Exception as e:
            print(f"Error al obtener procesos: {e}")
    
    def matar_proceso(self):
        """Permite terminar un proceso por PID"""
        print("\n--- TERMINAR PROCESO ---")
        try:
            pid = input("Ingrese el PID del proceso a terminar: ")
            if not pid.isdigit():
                print("Error: El PID debe ser un número.")
                return
            
            pid = int(pid)
            
            # Verificar si el proceso existe
            if not psutil.pid_exists(pid):
                print(f"Error: No existe un proceso con PID {pid}")
                return
            
            # Obtener información del proceso antes de terminarlo
            try:
                proceso = psutil.Process(pid)
                nombre = proceso.name()
                
                confirmacion = input(f"¿Está seguro de terminar '{nombre}' (PID: {pid})? (s/n): ")
                if confirmacion.lower() in ['s', 'si', 'yes', 'y']:
                    proceso.terminate()
                    print(f"Proceso '{nombre}' (PID: {pid}) terminado exitosamente.")
                else:
                    print("Operación cancelada.")
                    
            except psutil.AccessDenied:
                print(f"Error: No tiene permisos para terminar el proceso {pid}")
            except psutil.NoSuchProcess:
                print(f"Error: El proceso {pid} ya no existe")
                
        except KeyboardInterrupt:
            print("\nOperación cancelada.")
        except Exception as e:
            print(f"Error inesperado: {e}")
    
    def buscar_procesos(self):
        """Busca procesos por nombre"""
        print("\n--- BUSCAR PROCESOS ---")
        try:
            termino_busqueda = input("Ingrese el nombre del proceso a buscar: ").strip()
            if not termino_busqueda:
                print("Error: Debe ingresar un término de búsqueda.")
                return
            
            print(f"\nBuscando procesos que contengan: '{termino_busqueda}'")
            print(f"{'PID':<8} {'Nombre':<30} {'CPU%':<8} {'Memoria%':<10} {'Estado':<12}")
            print("-" * 75)
            
            encontrados = 0
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    if termino_busqueda.lower() in proc.info['name'].lower():
                        pid = proc.info['pid']
                        name = proc.info['name'][:29] if proc.info['name'] else 'N/A'
                        cpu = f"{proc.info['cpu_percent']:.1f}" if proc.info['cpu_percent'] else '0.0'
                        memory = f"{proc.info['memory_percent']:.1f}" if proc.info['memory_percent'] else '0.0'
                        status = proc.info['status'][:11] if proc.info['status'] else 'N/A'
                        
                        print(f"{pid:<8} {name:<30} {cpu:<8} {memory:<10} {status:<12}")
                        encontrados += 1
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
                    continue
            
            if encontrados == 0:
                print(f"No se encontraron procesos que contengan '{termino_busqueda}'")
            else:
                print(f"\n{encontrados} proceso(s) encontrado(s).")
                
        except KeyboardInterrupt:
            print("\nBúsqueda cancelada.")
        except Exception as e:
            print(f"Error durante la búsqueda: {e}")
    
    

def main():
    """Función principal"""
    try:
        # Limpiar pantalla al inicio
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Crear e iniciar el administrador de tareas
        task_manager = TaskManager()
        task_manager.ejecutar()
        
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
    except Exception as e:
        print(f"Error al iniciar el programa: {e}")
    finally:
        sys.exit(0)

if __name__ == "__main__":
    main()
