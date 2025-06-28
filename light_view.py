import customtkinter as ctk
from tkinter import messagebox, ttk
import threading
import time
from controllers.light_controller import LightController

class LightView:
    def __init__(self, parent):
        self.parent = parent
        self.light_frame = None
        self.controller = LightController()
        
        # Widgets para controle
        self.light_buttons = {}
        self.status_labels = {}
        self.connection_status_label = None
        
        # Nomes amigáveis para os setores
        self.setor_names = {
            'oficina': 'Oficina',
            'galpao_bloco1': 'Galpão - Bloco 1',
            'galpao_bloco2': 'Galpão - Bloco 2',
            'galpao_bloco3': 'Galpão - Bloco 3',
            'escritorio': 'Escritório',
            'corredor': 'Corredor',
            'area_servico': 'Área de Serviço',
            'area_externa': 'Área Externa'
        }
        
    def create_light_frame(self):
        if self.light_frame:
            self.light_frame.destroy()
            
        self.light_frame = ctk.CTkFrame(self.parent)
        self.light_frame.grid(row=0, column=1, columnspan=3, rowspan=4, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        # Title
        title_label = ctk.CTkLabel(self.light_frame, text="Controle de Luzes - LogiTrack", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, columnspan=4, padx=20, pady=20)
        
        # Frame de conexão
        connection_frame = ctk.CTkFrame(self.light_frame)
        connection_frame.grid(row=1, column=0, columnspan=4, padx=20, pady=10, sticky="ew")
        
        ctk.CTkLabel(connection_frame, text="Conexão Arduino:", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=10, pady=10)
        
        # Campo para porta serial
        ctk.CTkLabel(connection_frame, text="Porta:").grid(row=0, column=1, padx=5, pady=10)
        self.port_entry = ctk.CTkEntry(connection_frame, width=100)
        self.port_entry.insert(0, "COM3")
        self.port_entry.grid(row=0, column=2, padx=5, pady=10)
        
        # Botões de conexão
        self.connect_button = ctk.CTkButton(connection_frame, text="Conectar", 
                                           command=self.connect_arduino, width=100)
        self.connect_button.grid(row=0, column=3, padx=5, pady=10)
        
        self.disconnect_button = ctk.CTkButton(connection_frame, text="Desconectar", 
                                              command=self.disconnect_arduino, width=100, state="disabled")
        self.disconnect_button.grid(row=0, column=4, padx=5, pady=10)
        
        # Status da conexão
        self.connection_status_label = ctk.CTkLabel(connection_frame, text="Desconectado", 
                                                   text_color="red", font=ctk.CTkFont(weight="bold"))
        self.connection_status_label.grid(row=0, column=5, padx=10, pady=10)
        
        # Frame de controles gerais
        general_frame = ctk.CTkFrame(self.light_frame)
        general_frame.grid(row=2, column=0, columnspan=4, padx=20, pady=10, sticky="ew")
        
        ctk.CTkLabel(general_frame, text="Controles Gerais:", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=10, pady=10)
        
        ctk.CTkButton(general_frame, text="Ligar Todas", command=self.turn_on_all, 
                     width=120, fg_color="green").grid(row=0, column=1, padx=10, pady=10)
        
        ctk.CTkButton(general_frame, text="Desligar Todas", command=self.turn_off_all, 
                     width=120, fg_color="red").grid(row=0, column=2, padx=10, pady=10)
        
        ctk.CTkButton(general_frame, text="Atualizar Status", command=self.atualizar_status, 
                     width=120).grid(row=0, column=3, padx=10, pady=10)
        
        # Frame para controles individuais
        individual_frame = ctk.CTkFrame(self.light_frame)
        individual_frame.grid(row=3, column=0, columnspan=4, padx=20, pady=10, sticky="nsew")
        
        ctk.CTkLabel(individual_frame, text="Controles Individuais:", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        
        # Criar controles para cada setor
        row = 1
        col = 0
        for setor_id, setor_name in self.setor_names.items():
            # Frame para cada setor
            setor_frame = ctk.CTkFrame(individual_frame)
            setor_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            
            # Nome do setor
            ctk.CTkLabel(setor_frame, text=setor_name, 
                        font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=3, padx=5, pady=5)
            
            # Botão Ligar
            on_button = ctk.CTkButton(setor_frame, text="Ligar", width=60, height=30,
                                     command=lambda s=setor_id: self.turn_on_light(s),
                                     fg_color="green")
            on_button.grid(row=1, column=0, padx=2, pady=5)
            
            # Botão Desligar
            off_button = ctk.CTkButton(setor_frame, text="Desligar", width=60, height=30,
                                      command=lambda s=setor_id: self.turn_off_light(s),
                                      fg_color="red")
            off_button.grid(row=1, column=1, padx=2, pady=5)
            
            # Status
            status_label = ctk.CTkLabel(setor_frame, text="DESLIGADA", 
                                       font=ctk.CTkFont(weight="bold"), text_color="red")
            status_label.grid(row=1, column=2, padx=5, pady=5)
            
            self.status_labels[setor_id] = status_label
            
            # Organizar em grid 2x4
            col += 1
            if col >= 2:
                col = 0
                row += 1
        
        # Frame para log de comandos
        log_frame = ctk.CTkFrame(self.light_frame)
        log_frame.grid(row=4, column=0, columnspan=4, padx=20, pady=10, sticky="nsew")
        
        ctk.CTkLabel(log_frame, text="Log de Comandos:", 
                    font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=10, pady=10)
        
        self.log_textbox = ctk.CTkTextbox(log_frame, height=100, width=800)
        self.log_textbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Configure grid weights
        self.light_frame.grid_rowconfigure(3, weight=1)
        self.light_frame.grid_rowconfigure(4, weight=1)
        self.light_frame.grid_columnconfigure(0, weight=1)
        self.light_frame.grid_columnconfigure(1, weight=1)
        self.light_frame.grid_columnconfigure(2, weight=1)
        self.light_frame.grid_columnconfigure(3, weight=1)
        
        individual_frame.grid_columnconfigure(0, weight=1)
        individual_frame.grid_columnconfigure(1, weight=1)
        
        log_frame.grid_rowconfigure(1, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)
        
        # Atualizar status inicial
        self.atualizar_status()
        
    def connect_arduino(self):
        """Conecta com o Arduino"""
        port = self.port_entry.get().strip()
        if not port:
            messagebox.showerror("Erro", "Digite a porta serial!")
            return
            
        self.log_message(f"Tentando conectar na porta {port}...")
        
        if self.controller.connect_arduino(port):
            self.connection_status_label.configure(text="Conectado", text_color="green")
            self.connect_button.configure(state="disabled")
            self.disconnect_button.configure(state="normal")
            self.log_message("Conectado com sucesso!")
            messagebox.showinfo("Sucesso", "Conectado ao Arduino!")
        else:
            self.connection_status_label.configure(text="Erro de Conexão", text_color="red")
            self.log_message("Falha na conexão - modo simulação ativo")
            messagebox.showwarning("Aviso", "Não foi possível conectar ao Arduino.\nModo simulação ativado.")
            
    def disconnect_arduino(self):
        """Desconecta do Arduino"""
        self.controller.disconnect_arduino()
        self.connection_status_label.configure(text="Desconectado", text_color="red")
        self.connect_button.configure(state="normal")
        self.disconnect_button.configure(state="disabled")
        self.log_message("Desconectado do Arduino")
        
    def turn_on_light(self, setor):
        """Liga uma luz específica"""
        success = self.controller.turn_on_light(setor)
        if success:
            self.status_labels[setor].configure(text="LIGADA", text_color="green")
            self.log_message(f"Luz {self.setor_names[setor]} ligada")
        else:
            self.log_message(f"Erro ao ligar luz {self.setor_names[setor]}")
            
    def turn_off_light(self, setor):
        """Desliga uma luz específica"""
        success = self.controller.turn_off_light(setor)
        if success:
            self.status_labels[setor].configure(text="DESLIGADA", text_color="red")
            self.log_message(f"Luz {self.setor_names[setor]} desligada")
        else:
            self.log_message(f"Erro ao desligar luz {self.setor_names[setor]}")
            
    def turn_on_all(self):
        """Liga todas as luzes"""
        success = self.controller.turn_on_all_lights()
        if success:
            for setor in self.status_labels:
                self.status_labels[setor].configure(text="LIGADA", text_color="green")
            self.log_message("Todas as luzes ligadas")
        else:
            self.log_message("Erro ao ligar todas as luzes")
            
    def turn_off_all(self):
        """Desliga todas as luzes"""
        success = self.controller.turn_off_all_lights()
        if success:
            for setor in self.status_labels:
                self.status_labels[setor].configure(text="DESLIGADA", text_color="red")
            self.log_message("Todas as luzes desligadas")
        else:
            self.log_message("Erro ao desligar todas as luzes")
            
    def atualizar_status(self):
        """Atualiza o status de todas as luzes"""
        status = self.controller.get_all_status()
        for setor, ligada in status.items():
            if setor in self.status_labels:
                if ligada:
                    self.status_labels[setor].configure(text="LIGADA", text_color="green")
                else:
                    self.status_labels[setor].configure(text="DESLIGADA", text_color="red")
        
        self.log_message("Status atualizado")
        
    def log_message(self, message):
        """Adiciona mensagem ao log"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_textbox.insert("end", log_entry)
        self.log_textbox.see("end")  # Scroll para o final

