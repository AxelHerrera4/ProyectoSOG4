#!/usr/bin/env python3
"""
Administrador de Tareas - Interfaz Gráfica
Sistema de gestión de procesos con monitoreo en tiempo real
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import psutil
import threading
import time
from datetime import datetime
import json
import os

class TaskManagerGUI:
    """Administrador de Tareas con Interfaz Gráfica"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Administrador de Tareas")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Variables para gráficos dinámicos
        self.cpu_data = []
        self.memory_data = []
        self.time_data = []
        self.max_points = 50
        
        # Base de datos de procesos observados
        self.watched_processes = self.load_watched_processes()
        
        # Configurar estilos
        self.setup_styles()
        
        # Crear la interfaz
        self.create_widgets()
        
        # Iniciar actualización automática
        self.update_system_info()
        self.start_real_time_monitoring()
    
    def setup_styles(self):
        """Configura los estilos de la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores
        style.configure('Title.TLabel', 
                       background='#2c3e50', 
                       foreground='#ecf0f1', 
                       font=('Arial', 16, 'bold'))
        
        style.configure('Subtitle.TLabel', 
                       background='#34495e', 
                       foreground='#ecf0f1', 
                       font=('Arial', 12, 'bold'))
        
        style.configure('Custom.Treeview', 
                       background='#ecf0f1',
                       foreground='#2c3e50',
                       fieldbackground='#ecf0f1')
        
        style.configure('Action.TButton',
                       background='#3498db',
                       foreground='white',
                       font=('Arial', 10, 'bold'))
    
    def load_watched_processes(self):
        """Carga la lista de procesos observados"""
        try:
            if os.path.exists('watched_processes.json'):
                with open('watched_processes.json', 'r') as f:
                    return json.load(f)
            return {}
        except:
            return {}
    
    def save_watched_processes(self):
        """Guarda la lista de procesos observados"""
        try:
            with open('watched_processes.json', 'w') as f:
                json.dump(self.watched_processes, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {e}")
    
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        
        # Marco principal
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título principal
        title_label = ttk.Label(main_frame, 
                               text="ADMINISTRADOR DE TAREAS", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Crear notebook para pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Crear todas las pestañas
        self.create_system_info_tab()
        self.create_processes_tab()
        self.create_monitoring_tab()
        self.create_watched_processes_tab()
        self.create_actions_tab()
    
    def create_system_info_tab(self):
        """Crea la pestaña de información del sistema"""
        system_frame = ttk.Frame(self.notebook)
        self.notebook.add(system_frame, text="Sistema")
        
        # Marco superior para información básica
        info_frame = tk.Frame(system_frame, bg='#34495e', relief='ridge', bd=2)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(info_frame, text="INFORMACIÓN DEL SISTEMA", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Frame para información en columnas
        columns_frame = tk.Frame(info_frame, bg='#34495e')
        columns_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Columna CPU
        cpu_frame = tk.Frame(columns_frame, bg='#34495e')
        cpu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        tk.Label(cpu_frame, text="CPU", bg='#34495e', fg='#ecf0f1', 
                font=('Arial', 12, 'bold')).pack()
        self.cpu_usage_label = tk.Label(cpu_frame, text="Uso: ---%", 
                                       bg='#34495e', fg='#e74c3c', 
                                       font=('Arial', 11))
        self.cpu_usage_label.pack()
        self.cpu_cores_label = tk.Label(cpu_frame, text="Núcleos: ---", 
                                       bg='#34495e', fg='#ecf0f1')
        self.cpu_cores_label.pack()
        
        # Columna Memoria
        memory_frame = tk.Frame(columns_frame, bg='#34495e')
        memory_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        tk.Label(memory_frame, text="MEMORIA", bg='#34495e', fg='#ecf0f1', 
                font=('Arial', 12, 'bold')).pack()
        self.memory_usage_label = tk.Label(memory_frame, text="Uso: ---%", 
                                          bg='#34495e', fg='#e67e22', 
                                          font=('Arial', 11))
        self.memory_usage_label.pack()
        self.memory_total_label = tk.Label(memory_frame, text="Total: --- GB", 
                                          bg='#34495e', fg='#ecf0f1')
        self.memory_total_label.pack()
        
        # Columna Disco
        disk_frame = tk.Frame(columns_frame, bg='#34495e')
        disk_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        tk.Label(disk_frame, text="DISCO", bg='#34495e', fg='#ecf0f1', 
                font=('Arial', 12, 'bold')).pack()
        self.disk_usage_label = tk.Label(disk_frame, text="Uso: ---%", 
                                        bg='#34495e', fg='#9b59b6', 
                                        font=('Arial', 11))
        self.disk_usage_label.pack()
        self.disk_total_label = tk.Label(disk_frame, text="Total: --- GB", 
                                        bg='#34495e', fg='#ecf0f1')
        self.disk_total_label.pack()
        
        # Botón de actualización manual
        refresh_btn = ttk.Button(info_frame, text="Actualizar", 
                                style='Action.TButton',
                                command=self.update_system_info)
        refresh_btn.pack(pady=10)
    
    def create_processes_tab(self):
        """Crea la pestaña de procesos"""
        processes_frame = ttk.Frame(self.notebook)
        self.notebook.add(processes_frame, text="Procesos")
        
        # Marco de controles
        controls_frame = tk.Frame(processes_frame, bg='#34495e', relief='ridge', bd=2)
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(controls_frame, text="LISTA DE PROCESOS", 
                 style='Subtitle.TLabel').pack(pady=5)
        
        # Controles de búsqueda y filtrado
        search_frame = tk.Frame(controls_frame, bg='#34495e')
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Buscar:", bg='#34495e', fg='#ecf0f1').pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        search_btn = ttk.Button(search_frame, text="Buscar", 
                               command=self.search_processes)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_processes_btn = ttk.Button(search_frame, text="Actualizar", 
                                          command=self.update_processes_list)
        refresh_processes_btn.pack(side=tk.LEFT, padx=5)
        
        # Marco para filtros adicionales
        filter_frame = tk.Frame(controls_frame, bg='#34495e')
        filter_frame.pack(pady=5)
        
        self.show_accessible_only = tk.BooleanVar(value=False)
        accessible_check = tk.Checkbutton(filter_frame, 
                                         text="Solo procesos accesibles",
                                         variable=self.show_accessible_only,
                                         bg='#34495e', fg='#ecf0f1',
                                         selectcolor='#34495e',
                                         command=self.update_processes_list)
        accessible_check.pack(side=tk.LEFT, padx=10)
        
    # (Botón de ayuda de permisos eliminado por solicitud del usuario)
        
        # Lista de procesos con scroll
        list_frame = tk.Frame(processes_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear Treeview para procesos
        columns = ('PID', 'Nombre', 'CPU%', 'Memoria%', 'Memoria(MB)', 'Estado')
        self.processes_tree = ttk.Treeview(list_frame, columns=columns, show='headings',
                                          style='Custom.Treeview')
        
        # Configurar columnas
        for col in columns:
            self.processes_tree.heading(col, text=col)
            if col == 'PID':
                self.processes_tree.column(col, width=80)
            elif col == 'Nombre':
                self.processes_tree.column(col, width=250)
            elif col in ['CPU%', 'Memoria%']:
                self.processes_tree.column(col, width=80)
            elif col == 'Memoria(MB)':
                self.processes_tree.column(col, width=100)
            else:
                self.processes_tree.column(col, width=120)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.processes_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.processes_tree.xview)
        self.processes_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Empaquetar
        self.processes_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Cargar procesos inicialmente
        self.update_processes_list()
    
    def create_monitoring_tab(self):
        """Crea la pestaña de monitoreo con gráficos dinámicos"""
        monitor_frame = ttk.Frame(self.notebook)
        self.notebook.add(monitor_frame, text="Monitor")
        
        # Marco de título
        title_frame = tk.Frame(monitor_frame, bg='#34495e', relief='ridge', bd=2)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(title_frame, text="MONITOREO EN TIEMPO REAL", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Crear figura de matplotlib
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(10, 6))
        self.fig.patch.set_facecolor('#2c3e50')
        
        # Configurar gráfico de CPU
        self.ax1.set_title('Uso de CPU (%)', color='white', fontsize=12, fontweight='bold')
        self.ax1.set_ylabel('Porcentaje', color='white')
        self.ax1.set_facecolor('#34495e')
        self.ax1.tick_params(colors='white')
        self.ax1.grid(True, alpha=0.3)
        
        # Configurar gráfico de Memoria
        self.ax2.set_title('Uso de Memoria (%)', color='white', fontsize=12, fontweight='bold')
        self.ax2.set_ylabel('Porcentaje', color='white')
        self.ax2.set_xlabel('Tiempo', color='white')
        self.ax2.set_facecolor('#34495e')
        self.ax2.tick_params(colors='white')
        self.ax2.grid(True, alpha=0.3)
        
        # Integrar matplotlib en tkinter
        canvas_frame = tk.Frame(monitor_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = FigureCanvasTkAgg(self.fig, canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Controles de monitoreo
        controls_monitor_frame = tk.Frame(monitor_frame, bg='#34495e')
        controls_monitor_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.monitoring_active = tk.BooleanVar(value=True)
        monitor_check = tk.Checkbutton(controls_monitor_frame, 
                                      text="Monitoreo activo",
                                      variable=self.monitoring_active,
                                      bg='#34495e', fg='#ecf0f1',
                                      selectcolor='#34495e')
        monitor_check.pack(side=tk.LEFT, padx=10)
        
        clear_btn = ttk.Button(controls_monitor_frame, text="Limpiar graficos",
                              command=self.clear_graphs)
        clear_btn.pack(side=tk.RIGHT, padx=10)
    
    def create_watched_processes_tab(self):
        """Crea la pestaña para procesos observados"""
        watched_frame = ttk.Frame(self.notebook)
        self.notebook.add(watched_frame, text="Observados")
        
        # Marco de título
        title_frame = tk.Frame(watched_frame, bg='#34495e', relief='ridge', bd=2)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(title_frame, text="PROCESOS OBSERVADOS", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Controles CRUD
        crud_frame = tk.Frame(watched_frame, bg='#34495e')
        crud_frame.pack(fill=tk.X, padx=10, pady=5)
        
        add_btn = ttk.Button(crud_frame, text="Agregar", 
                            command=self.add_watched_process)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        edit_btn = ttk.Button(crud_frame, text="Editar", 
                             command=self.edit_watched_process)
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = ttk.Button(crud_frame, text="Eliminar", 
                               command=self.delete_watched_process)
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_watched_btn = ttk.Button(crud_frame, text="Actualizar", 
                                        command=self.update_watched_list)
        refresh_watched_btn.pack(side=tk.RIGHT, padx=5)
        
        # Lista de procesos observados
        watched_list_frame = tk.Frame(watched_frame)
        watched_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        watched_columns = ('PID', 'Nombre', 'Prioridad', 'Estado', 'Agregado')
        self.watched_tree = ttk.Treeview(watched_list_frame, columns=watched_columns, 
                                        show='headings', style='Custom.Treeview')
        
        for col in watched_columns:
            self.watched_tree.heading(col, text=col)
            if col == 'PID':
                self.watched_tree.column(col, width=80)
            elif col == 'Nombre':
                self.watched_tree.column(col, width=200)
            else:
                self.watched_tree.column(col, width=150)
        
        # Scrollbar para procesos observados
        watched_scroll = ttk.Scrollbar(watched_list_frame, orient=tk.VERTICAL, 
                                      command=self.watched_tree.yview)
        self.watched_tree.configure(yscrollcommand=watched_scroll.set)
        
        self.watched_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        watched_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Cargar lista inicial
        self.update_watched_list()
    
    def create_actions_tab(self):
        """Crea la pestaña de acciones sobre procesos"""
        actions_frame = ttk.Frame(self.notebook)
        self.notebook.add(actions_frame, text="Acciones")
        
        # Marco de título
        title_frame = tk.Frame(actions_frame, bg='#34495e', relief='ridge', bd=2)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(title_frame, text="ACCIONES SOBRE PROCESOS", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Marco principal de acciones
        main_actions_frame = tk.Frame(actions_frame, bg='#2c3e50')
        main_actions_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Terminar proceso
        terminate_frame = tk.LabelFrame(main_actions_frame, text="Terminar Proceso", 
                                       bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'))
        terminate_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(terminate_frame, text="PID del proceso:", bg='#e74c3c', fg='white').pack(anchor=tk.W, padx=10, pady=5)
        self.terminate_pid_var = tk.StringVar()
        tk.Entry(terminate_frame, textvariable=self.terminate_pid_var, width=20).pack(anchor=tk.W, padx=10)
        
        terminate_btn = tk.Button(terminate_frame, text="TERMINAR PROCESO", 
                                 bg='#c0392b', fg='white', font=('Arial', 10, 'bold'),
                                 command=self.terminate_process)
        terminate_btn.pack(pady=10)
        
        # Cambiar prioridad
        priority_frame = tk.LabelFrame(main_actions_frame, text="Cambiar Prioridad", 
                                      bg='#f39c12', fg='white', font=('Arial', 12, 'bold'))
        priority_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(priority_frame, text="PID del proceso:", bg='#f39c12', fg='white').pack(anchor=tk.W, padx=10, pady=5)
        self.priority_pid_var = tk.StringVar()
        tk.Entry(priority_frame, textvariable=self.priority_pid_var, width=20).pack(anchor=tk.W, padx=10)
        
        tk.Label(priority_frame, text="Nueva prioridad:", bg='#f39c12', fg='white').pack(anchor=tk.W, padx=10, pady=(10,5))
        self.priority_var = tk.StringVar(value="normal")
        priority_combo = ttk.Combobox(priority_frame, textvariable=self.priority_var,
                                     values=["realtime", "high", "normal", "below_normal", "idle"],
                                     width=17)
        priority_combo.pack(anchor=tk.W, padx=10)
        
        priority_btn = tk.Button(priority_frame, text="CAMBIAR PRIORIDAD", 
                                bg='#e67e22', fg='white', font=('Arial', 10, 'bold'),
                                command=self.change_priority)
        priority_btn.pack(pady=10)
        
        # Información detallada
        info_frame = tk.LabelFrame(main_actions_frame, text="Información Detallada", 
                                  bg='#3498db', fg='white', font=('Arial', 12, 'bold'))
        info_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(info_frame, text="PID del proceso:", bg='#3498db', fg='white').pack(anchor=tk.W, padx=10, pady=5)
        self.info_pid_var = tk.StringVar()
        tk.Entry(info_frame, textvariable=self.info_pid_var, width=20).pack(anchor=tk.W, padx=10)
        
        info_btn = tk.Button(info_frame, text="VER INFORMACIÓN", 
                            bg='#2980b9', fg='white', font=('Arial', 10, 'bold'),
                            command=self.show_process_info)
        info_btn.pack(pady=10)
    
    def update_system_info(self):
        """Actualiza la información del sistema"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_count = psutil.cpu_count()
            self.cpu_usage_label.config(text=f"Uso: {cpu_percent:.1f}%")
            self.cpu_cores_label.config(text=f"Núcleos: {cpu_count}")
            
            # Memoria
            memory = psutil.virtual_memory()
            self.memory_usage_label.config(text=f"Uso: {memory.percent:.1f}%")
            self.memory_total_label.config(text=f"Total: {memory.total / (1024**3):.1f} GB")
            
            # Disco
            try:
                disk = psutil.disk_usage('C:' if os.name == 'nt' else '/')
                disk_percent = (disk.used / disk.total) * 100
                self.disk_usage_label.config(text=f"Uso: {disk_percent:.1f}%")
                self.disk_total_label.config(text=f"Total: {disk.total / (1024**3):.1f} GB")
            except:
                self.disk_usage_label.config(text="Uso: N/A")
                self.disk_total_label.config(text="Total: N/A")
            
        except Exception:
            pass
        
        # Programar próxima actualización
        self.root.after(5000, self.update_system_info)
    
    # La función de ayuda de permisos fue eliminada por solicitud del usuario.
    
    def get_safe_process_info(self, proc):
        """Obtiene información de proceso de manera segura"""
        info = {
            'pid': proc.pid,
            'name': 'N/A',
            'cpu_percent': 0.0,
            'memory_percent': 0.0,
            'memory_mb': 0.0,
            'status': 'N/A',
            'accessible': True
        }
        
        try:
            info['name'] = proc.name()[:30]
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            info['name'] = '[Acceso denegado]'
            info['accessible'] = False
        except Exception:
            info['name'] = '[Error]'
            info['accessible'] = False
        
        try:
            cpu = proc.cpu_percent()
            info['cpu_percent'] = cpu if cpu is not None else 0.0
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            info['cpu_percent'] = 0.0
            info['accessible'] = False
        except Exception:
            info['cpu_percent'] = 0.0
        
        try:
            mem_percent = proc.memory_percent()
            info['memory_percent'] = mem_percent if mem_percent is not None else 0.0
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            info['memory_percent'] = 0.0
            info['accessible'] = False
        except Exception:
            info['memory_percent'] = 0.0
        
        try:
            memory_info = proc.memory_info()
            info['memory_mb'] = memory_info.rss / (1024*1024) if memory_info else 0.0
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            info['memory_mb'] = 0.0
            info['accessible'] = False
        except Exception:
            info['memory_mb'] = 0.0
        
        try:
            status = proc.status()
            info['status'] = status[:15] if status else 'N/A'
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            info['status'] = '[Protegido]'
            info['accessible'] = False
        except Exception:
            info['status'] = '[Error]'
            info['accessible'] = False
        
        return info
    
    def update_processes_list(self):
        """Actualiza la lista de procesos"""
        # Limpiar lista actual
        for item in self.processes_tree.get_children():
            self.processes_tree.delete(item)
        
        try:
            procesos = []
            accessible_count = 0
            total_count = 0
            
            for proc in psutil.process_iter():
                total_count += 1
                try:
                    info = self.get_safe_process_info(proc)
                    
                    # Aplicar filtro si está activado
                    if self.show_accessible_only.get() and not info['accessible']:
                        continue
                    
                    procesos.append(info)
                    if info['accessible']:
                        accessible_count += 1
                except Exception:
                    continue
            
            # Ordenar por CPU
            procesos.sort(key=lambda x: x['cpu_percent'], reverse=True)
            
            # Mostrar top 50 procesos
            displayed_count = min(50, len(procesos))
            for proc in procesos[:displayed_count]:
                pid = proc['pid']
                name = proc['name']
                cpu = f"{proc['cpu_percent']:.1f}"
                mem_percent = f"{proc['memory_percent']:.1f}"
                mem_mb = f"{proc['memory_mb']:.1f}"
                status = proc['status']
                
                self.processes_tree.insert('', 'end', values=(pid, name, cpu, mem_percent, mem_mb, status))
            
            # Actualizar título o mostrar información de estado
            if not self.show_accessible_only.get() and accessible_count < total_count:
                restricted_count = total_count - accessible_count
                print(f"Procesos: {displayed_count} mostrados, {accessible_count} accesibles de {total_count} totales")
            else:
                print(f"Procesos mostrados: {displayed_count} de {len(procesos)} totales")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar procesos: {e}")
    
    def search_processes(self):
        """Busca procesos por nombre"""
        search_term = self.search_var.get().strip().lower()
        if not search_term:
            self.update_processes_list()
            return
        
        # Limpiar lista
        for item in self.processes_tree.get_children():
            self.processes_tree.delete(item)
        
        try:
            found_count = 0
            for proc in psutil.process_iter():
                try:
                    info = self.get_safe_process_info(proc)
                    
                    # Aplicar filtro de accesibilidad si está activado
                    if self.show_accessible_only.get() and not info['accessible']:
                        continue
                    
                    # Buscar en el nombre del proceso
                    if search_term in info['name'].lower():
                        pid = info['pid']
                        name = info['name']
                        cpu = f"{info['cpu_percent']:.1f}"
                        mem_percent = f"{info['memory_percent']:.1f}"
                        mem_mb = f"{info['memory_mb']:.1f}"
                        status = info['status']
                        
                        self.processes_tree.insert('', 'end', values=(pid, name, cpu, mem_percent, mem_mb, status))
                        found_count += 1
                        
                except Exception:
                    continue
            
            if found_count == 0:
                messagebox.showinfo("Búsqueda", f"No se encontraron procesos con '{search_term}'")
                        
        except Exception as e:
            messagebox.showerror("Error", f"Error en búsqueda: {e}")
    
    def start_real_time_monitoring(self):
        """Inicia el monitoreo en tiempo real para gráficos"""
        def update_graphs():
            while True:
                if self.monitoring_active.get():
                    try:
                        # Obtener datos actuales
                        cpu_percent = psutil.cpu_percent(interval=1)
                        memory_percent = psutil.virtual_memory().percent
                        current_time = datetime.now().strftime("%H:%M:%S")
                        
                        # Agregar a listas
                        self.cpu_data.append(cpu_percent)
                        self.memory_data.append(memory_percent)
                        self.time_data.append(current_time)
                        
                        # Mantener solo los últimos puntos
                        if len(self.cpu_data) > self.max_points:
                            self.cpu_data.pop(0)
                            self.memory_data.pop(0)
                            self.time_data.pop(0)
                        
                        # Actualizar gráficos
                        self.root.after(0, self.update_graphs_display)
                        
                    except Exception:
                        pass
                
                time.sleep(2)
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=update_graphs, daemon=True)
        thread.start()
    
    def update_graphs_display(self):
        """Actualiza la visualización de los gráficos"""
        try:
            # Limpiar gráficos
            self.ax1.clear()
            self.ax2.clear()
            
            if self.cpu_data and self.memory_data:
                # Gráfico CPU
                self.ax1.plot(range(len(self.cpu_data)), self.cpu_data, 'r-', linewidth=2, label='CPU')
                self.ax1.fill_between(range(len(self.cpu_data)), self.cpu_data, alpha=0.3, color='red')
                self.ax1.set_title('Uso de CPU (%)', color='white', fontsize=12, fontweight='bold')
                self.ax1.set_ylabel('Porcentaje', color='white')
                self.ax1.set_ylim(0, 100)
                self.ax1.set_facecolor('#34495e')
                self.ax1.tick_params(colors='white')
                self.ax1.grid(True, alpha=0.3)
                
                # Gráfico Memoria
                self.ax2.plot(range(len(self.memory_data)), self.memory_data, 'b-', linewidth=2, label='Memoria')
                self.ax2.fill_between(range(len(self.memory_data)), self.memory_data, alpha=0.3, color='blue')
                self.ax2.set_title('Uso de Memoria (%)', color='white', fontsize=12, fontweight='bold')
                self.ax2.set_ylabel('Porcentaje', color='white')
                self.ax2.set_xlabel('Tiempo', color='white')
                self.ax2.set_ylim(0, 100)
                self.ax2.set_facecolor('#34495e')
                self.ax2.tick_params(colors='white')
                self.ax2.grid(True, alpha=0.3)
            
            # Actualizar canvas
            self.canvas.draw()
            
        except Exception:
            pass
    
    def clear_graphs(self):
        """Limpia los gráficos"""
        self.cpu_data.clear()
        self.memory_data.clear()
        self.time_data.clear()
        self.ax1.clear()
        self.ax2.clear()
        self.canvas.draw()

    def ask_priority_choice(self, title="Seleccionar Prioridad", initial="media"):
        """Muestra un diálogo modal con un Combobox para elegir prioridad.

        Devuelve la prioridad seleccionada ('alta'|'media'|'baja') o None si se cancela.
        """
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.transient(self.root)
        dialog.resizable(False, False)
        dialog.grab_set()

        frame = tk.Frame(dialog, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Prioridad:", bg='#f39c12', fg='white').pack(anchor=tk.W)
        var = tk.StringVar(value=initial)
        combo = ttk.Combobox(frame, textvariable=var, values=('alta', 'media', 'baja'), state='readonly', width=20)
        combo.pack(anchor=tk.W, pady=(5, 10))
        combo.focus_set()

        result = {'value': None}

        def on_ok():
            result['value'] = var.get()
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill=tk.X)
        tk.Button(btn_frame, text='OK', width=10, command=on_ok).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(btn_frame, text='Cancelar', width=10, command=on_cancel).pack(side=tk.LEFT)

        # Esperar a que se cierre
        self.root.wait_window(dialog)
        return result['value']
    
    def add_watched_process(self):
        """Agregar proceso a observados"""
        pid = simpledialog.askstring("Agregar Proceso", "Ingrese el PID del proceso:")
        if pid and pid.isdigit():
            pid = int(pid)
            try:
                if psutil.pid_exists(pid):
                    process = psutil.Process(pid)
                    name = process.name()
                    # Usar Combobox modal para evitar entrada libre
                    priority = self.ask_priority_choice("Prioridad de observación", initial="media")
                    if priority is None:
                        return
                    
                    self.watched_processes[str(pid)] = {
                        'name': name,
                        'priority': priority or 'media',
                        'status': 'activo',
                        'added': datetime.now().isoformat()
                    }
                    
                    self.save_watched_processes()
                    self.update_watched_list()
                    messagebox.showinfo("Éxito", f"Proceso {name} agregado a observación")
                else:
                    messagebox.showerror("Error", "El proceso no existe")
            except Exception as e:
                messagebox.showerror("Error", f"Error al agregar proceso: {e}")
    
    def edit_watched_process(self):
        """Editar proceso observado"""
        selection = self.watched_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione un proceso para editar")
            return
        
        item = self.watched_tree.item(selection[0])
        pid = item['values'][0]
        
        current_data = self.watched_processes.get(str(pid), {})

        # Usar Combobox modal para editar prioridad
        new_priority = self.ask_priority_choice("Editar Prioridad", initial=current_data.get('priority', 'media'))
        # Estado puede seguir siendo texto libre por ahora
        new_status = simpledialog.askstring("Editar Estado", 
                                           "Nuevo estado:", 
                                           initialvalue=current_data.get('status', 'activo'))

        if new_priority or new_status:
            if new_priority:
                self.watched_processes[str(pid)]['priority'] = new_priority
            if new_status:
                self.watched_processes[str(pid)]['status'] = new_status

            self.save_watched_processes()
            self.update_watched_list()
            messagebox.showinfo("Éxito", "Proceso actualizado")
    
    def delete_watched_process(self):
        """Eliminar proceso de observados"""
        selection = self.watched_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione un proceso para eliminar")
            return
        
        item = self.watched_tree.item(selection[0])
        pid = item['values'][0]
        name = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar {name} (PID: {pid}) de observación?"):
            if str(pid) in self.watched_processes:
                del self.watched_processes[str(pid)]
                self.save_watched_processes()
                self.update_watched_list()
                messagebox.showinfo("Éxito", "Proceso eliminado de observación")
    
    def update_watched_list(self):
        """Actualiza la lista de procesos observados"""
        for item in self.watched_tree.get_children():
            self.watched_tree.delete(item)
        
        for pid, data in self.watched_processes.items():
            added_date = data['added'][:19].replace('T', ' ')
            
            self.watched_tree.insert('', 'end', values=(
                pid, data['name'], data['priority'], 
                data['status'], added_date
            ))
    
    def terminate_process(self):
        """Termina un proceso"""
        pid_str = self.terminate_pid_var.get().strip()
        if not pid_str.isdigit():
            messagebox.showerror("Error", "El PID debe ser numérico")
            return
        
        pid = int(pid_str)
        try:
            if psutil.pid_exists(pid):
                process = psutil.Process(pid)
                
                # Intentar obtener el nombre del proceso
                try:
                    name = process.name()
                except psutil.AccessDenied:
                    name = f"PID {pid} (nombre no accesible)"
                
                # Advertencia especial para procesos del sistema
                try:
                    username = process.username()
                    if "SYSTEM" in username.upper() or "NT AUTHORITY" in username.upper():
                        warning_msg = f"""ADVERTENCIA: Proceso del sistema detectado

Proceso: {name}
Usuario: {username}
PID: {pid}

Terminar procesos del sistema puede causar inestabilidad.
¿Está seguro de continuar?"""
                        
                        if not messagebox.askyesno("Proceso del Sistema", warning_msg):
                            return
                except psutil.AccessDenied:
                    pass
                
                if messagebox.askyesno("Confirmar", f"¿Terminar proceso {name} (PID: {pid})?"):
                    try:
                        process.terminate()
                        messagebox.showinfo("Éxito", f"Proceso {name} terminado correctamente")
                        self.terminate_pid_var.set("")
                        self.update_processes_list()
                    except psutil.AccessDenied:
                        # Sugerir alternativas
                        error_msg = f"""Permisos insuficientes para terminar el proceso {name}

Soluciones posibles:
1. Ejecutar este programa como Administrador (Windows) o con sudo (Linux/Mac)
2. El proceso pertenece al sistema y requiere permisos especiales
3. Solo puedes terminar procesos de tu usuario

¿Desea intentar forzar la terminación? (solo procesos de usuario)"""
                        
                        if messagebox.askyesno("Permisos Insuficientes", error_msg):
                            try:
                                process.kill()
                                messagebox.showinfo("Éxito", f"Proceso {name} forzado a terminar")
                                self.terminate_pid_var.set("")
                                self.update_processes_list()
                            except Exception as e:
                                messagebox.showerror("Error", f"No se pudo forzar la terminación: {e}")
            else:
                messagebox.showerror("Error", "El proceso no existe")
        except psutil.NoSuchProcess:
            messagebox.showerror("Error", "El proceso ya no existe")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")
    
    def change_priority(self):
        """Cambia la prioridad de un proceso"""
        pid_str = self.priority_pid_var.get().strip()
        if not pid_str.isdigit():
            messagebox.showerror("Error", "El PID debe ser numérico")
            return
        
        pid = int(pid_str)
        priority = self.priority_var.get()
        
        try:
            if psutil.pid_exists(pid):
                process = psutil.Process(pid)
                
                # Intentar obtener información del proceso
                try:
                    name = process.name()
                except psutil.AccessDenied:
                    name = f"PID {pid} (nombre no accesible)"
                
                # Advertencia para prioridades altas
                if priority in ['realtime', 'high']:
                    warning_msg = f"""ADVERTENCIA: Prioridad Alta/Realtime

Proceso: {name}
Nueva prioridad: {priority.upper()}

Las prioridades altas pueden afectar el rendimiento del sistema.
¿Continuar con el cambio?"""
                    
                    if not messagebox.askyesno("Prioridad Alta", warning_msg):
                        return
                
                try:
                    # Mapear prioridades
                    if os.name == 'nt':  # Windows
                        priority_map = {
                            'realtime': psutil.REALTIME_PRIORITY_CLASS,
                            'high': psutil.HIGH_PRIORITY_CLASS,
                            'normal': psutil.NORMAL_PRIORITY_CLASS,
                            'below_normal': psutil.BELOW_NORMAL_PRIORITY_CLASS,
                            'idle': psutil.IDLE_PRIORITY_CLASS
                        }
                        process.nice(priority_map[priority])
                    else:  # Linux/Mac
                        nice_map = {'realtime': -20, 'high': -10, 'normal': 0, 'below_normal': 10, 'idle': 19}
                        process.nice(nice_map[priority])
                    
                    messagebox.showinfo("Éxito", f"Prioridad de {name} cambiada a {priority}")
                    self.priority_pid_var.set("")
                    
                except psutil.AccessDenied:
                    error_msg = f"""Permisos insuficientes para cambiar prioridad

Proceso: {name}
Prioridad deseada: {priority}

Soluciones:
1. Ejecutar como Administrador (Windows) o con sudo (Linux/Mac)
2. Solo puedes cambiar prioridad de procesos de tu usuario
3. Algunos procesos del sistema están protegidos

Nota: Las prioridades 'realtime' y 'high' siempre requieren permisos especiales."""
                    
                    messagebox.showerror("Permisos Insuficientes", error_msg)
                    
            else:
                messagebox.showerror("Error", "El proceso no existe")
        except psutil.NoSuchProcess:
            messagebox.showerror("Error", "El proceso ya no existe")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")
    
    def show_process_info(self):
        """Muestra información detallada de un proceso"""
        pid_str = self.info_pid_var.get().strip()
        if not pid_str.isdigit():
            messagebox.showerror("Error", "El PID debe ser numérico")
            return
        
        pid = int(pid_str)
        try:
            if psutil.pid_exists(pid):
                process = psutil.Process(pid)
                
                # Recopilar información disponible según permisos
                info_parts = ["INFORMACIÓN DETALLADA DEL PROCESO\n"]
                
                # Información básica (normalmente accesible)
                try:
                    info_parts.append("Básico:")
                    info_parts.append(f"• PID: {process.pid}")
                    
                    try:
                        name = process.name()
                        info_parts.append(f"• Nombre: {name}")
                    except psutil.AccessDenied:
                        info_parts.append("• Nombre: [Permisos insuficientes]")
                    
                    try:
                        status = process.status()
                        info_parts.append(f"• Estado: {status}")
                    except psutil.AccessDenied:
                        info_parts.append("• Estado: [Permisos insuficientes]")
                    
                    try:
                        create_time = datetime.fromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M:%S')
                        info_parts.append(f"• Creado: {create_time}")
                    except psutil.AccessDenied:
                        info_parts.append("• Creado: [Permisos insuficientes]")
                        
                    try:
                        username = process.username()
                        info_parts.append(f"• Usuario: {username}")
                    except psutil.AccessDenied:
                        info_parts.append("• Usuario: [Permisos insuficientes]")
                        
                except Exception:
                    info_parts.append("• Información básica: [Error de acceso]")
                
                # Información de rendimiento
                info_parts.append("\nRendimiento:")
                try:
                    cpu_percent = process.cpu_percent()
                    info_parts.append(f"• CPU: {cpu_percent:.1f}%")
                except psutil.AccessDenied:
                    info_parts.append("• CPU: [Permisos insuficientes]")
                except Exception:
                    info_parts.append("• CPU: [No disponible]")
                
                try:
                    memory_percent = process.memory_percent()
                    info_parts.append(f"• Memoria: {memory_percent:.1f}%")
                except psutil.AccessDenied:
                    info_parts.append("• Memoria: [Permisos insuficientes]")
                except Exception:
                    info_parts.append("• Memoria: [No disponible]")
                
                try:
                    memory_info = process.memory_info()
                    memory_mb = memory_info.rss / (1024*1024)
                    info_parts.append(f"• Memoria RSS: {memory_mb:.1f} MB")
                except psutil.AccessDenied:
                    info_parts.append("• Memoria RSS: [Permisos insuficientes]")
                except Exception:
                    info_parts.append("• Memoria RSS: [No disponible]")
                
                # Información de prioridad
                info_parts.append("\nPrioridad:")
                try:
                    nice_value = process.nice()
                    info_parts.append(f"• Nice: {nice_value}")
                except psutil.AccessDenied:
                    info_parts.append("• Nice: [Permisos insuficientes]")
                except Exception:
                    info_parts.append("• Nice: [No disponible]")
                
                # Información adicional si está disponible
                try:
                    cmdline = process.cmdline()
                    if cmdline:
                        cmd_str = ' '.join(cmdline)
                        if len(cmd_str) > 100:
                            cmd_str = cmd_str[:100] + "..."
                        info_parts.append(f"\nComando:\n• {cmd_str}")
                except psutil.AccessDenied:
                    info_parts.append("\nComando: [Permisos insuficientes]")
                except Exception:
                    pass
                
                # Añadir nota sobre permisos si es necesario
                if "[Permisos insuficientes]" in '\n'.join(info_parts):
                    info_parts.append("\n" + "="*50)
                    info_parts.append("NOTA: Algunos datos requieren permisos de administrador.")
                    info_parts.append("Para ver información completa:")
                    info_parts.append("• Windows: Ejecutar como Administrador")
                    info_parts.append("• Linux/Mac: Usar sudo")
                    info_parts.append("• O solo consultar procesos de tu usuario")
                
                final_info = '\n'.join(info_parts)
                messagebox.showinfo("Información del Proceso", final_info)
                self.info_pid_var.set("")
            else:
                messagebox.showerror("Error", "El proceso no existe")
        except psutil.NoSuchProcess:
            messagebox.showerror("Error", "El proceso ya no existe")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")
    
    def run(self):
        """Ejecuta la aplicación"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass
        except Exception:
            pass

def main():
    """Función principal"""
    try:
        app = TaskManagerGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Error Crítico", f"No se pudo iniciar la aplicación:\n{e}")

if __name__ == "__main__":
    main()
