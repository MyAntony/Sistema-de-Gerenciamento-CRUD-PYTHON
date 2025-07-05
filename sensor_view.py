import customtkinter as ctk
from tkinter import messagebox
import threading
import time
from sensor_simulator import SensorSimulator

# Atividade de:

# Antony Rafael - https://github.com/MyAntony
# Débora Magalhães - https://github.com/Debs2Dev
# Brunna Barreto - https://github.com/brunnabarreto
# Luís Felipe - https://github.com/IamLiper


class SensorView:
    def __init__(self, parent):
        self.parent = parent
        self.sensor_frame = None
        self.simulator = SensorSimulator()
        self.atualizar_thread = None
        self.running = False
        
        # Widgets para exibir dados
        self.data_labels = {}
        self.status_labels = {}
        
    def criar_sensor_frame(self):
        if self.sensor_frame:
            self.sensor_frame.destroy()
            
        self.sensor_frame = ctk.CTkFrame(self.parent)
        self.sensor_frame.grid(row=0, column=1, columnspan=3, rowspan=4, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        # Title
        title_label = ctk.CTkLabel(self.sensor_frame, text="Sistema de Sensores IoT - LogiTrack", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, columnspan=3, padx=20, pady=20)
        
        # Controles principais
        control_frame = ctk.CTkFrame(self.sensor_frame)
        control_frame.grid(row=1, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        
        self.start_button = ctk.CTkButton(control_frame, text="Iniciar Simulação", 
                                         command=self.start_simulation, width=150)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.stop_button = ctk.CTkButton(control_frame, text="Parar Simulação", 
                                        command=self.stop_simulation, width=150, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.test_button = ctk.CTkButton(control_frame, text="Teste de Emergência", 
                                        command=self.test_emergency, width=150)
        self.test_button.grid(row=0, column=2, padx=10, pady=10)
        
        # Frame para dados dos sensores
        sensors_frame = ctk.CTkFrame(self.sensor_frame)
        sensors_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        
        ctk.CTkLabel(sensors_frame, text="Dados dos Sensores", 
                    font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        # Labels para dados dos sensores
        sensor_labels = [
            ("Timestamp:", "timestamp"),
            ("Presença:", "presenca"),
            ("Luminosidade:", "luminosidade"),
            ("Temperatura:", "temperatura"),
            ("Fumaça:", "fumaca")
        ]
        
        for i, (label_text, key) in enumerate(sensor_labels):
            ctk.CTkLabel(sensors_frame, text=label_text).grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
            self.data_labels[key] = ctk.CTkLabel(sensors_frame, text="--", 
                                               font=ctk.CTkFont(weight="bold"))
            self.data_labels[key].grid(row=i+1, column=1, padx=10, pady=5, sticky="w")
        
        # Frame para status dos atuadores
        actuators_frame = ctk.CTkFrame(self.sensor_frame)
        actuators_frame.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")
        
        ctk.CTkLabel(actuators_frame, text="Status dos Atuadores", 
                    font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        # Labels para status dos atuadores
        actuator_labels = [
            ("Alarme:", "alarme"),
            ("Luzes Automáticas:", "luzes_automaticas"),
            ("Sirene:", "sirene"),
            ("Ventilação:", "ventilacao")
        ]
        
        for i, (label_text, key) in enumerate(actuator_labels):
            ctk.CTkLabel(actuators_frame, text=label_text).grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
            self.status_labels[key] = ctk.CTkLabel(actuators_frame, text="--", 
                                                 font=ctk.CTkFont(weight="bold"))
            self.status_labels[key].grid(row=i+1, column=1, padx=10, pady=5, sticky="w")
        
        # Frame para configurações
        config_frame = ctk.CTkFrame(self.sensor_frame)
        config_frame.grid(row=2, column=2, padx=20, pady=10, sticky="nsew")
        
        ctk.CTkLabel(config_frame, text="Configurações", 
                    font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        # Configuração de temperatura máxima
        ctk.CTkLabel(config_frame, text="Temp. Máxima (°C):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.temp_entry = ctk.CTkEntry(config_frame, width=80)
        self.temp_entry.insert(0, "35.0")
        self.temp_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Configuração de luminosidade mínima
        ctk.CTkLabel(config_frame, text="Lumin. Mínima (%):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.lumin_entry = ctk.CTkEntry(config_frame, width=80)
        self.lumin_entry.insert(0, "30")
        self.lumin_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Botões de configuração
        ctk.CTkButton(config_frame, text="Aplicar Config", 
                     command=self.apply_config, width=120).grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        
        ctk.CTkButton(config_frame, text="Toggle Luzes Auto", 
                     command=self.toggle_auto_lights, width=120).grid(row=4, column=0, columnspan=2, padx=10, pady=5)
        
        ctk.CTkButton(config_frame, text="Reset Alarme", 
                     command=self.reset_alarm, width=120).grid(row=5, column=0, columnspan=2, padx=10, pady=5)
        
        # Frame para log de eventos
        log_frame = ctk.CTkFrame(self.sensor_frame)
        log_frame.grid(row=3, column=0, columnspan=3, padx=20, pady=10, sticky="nsew")
        
        ctk.CTkLabel(log_frame, text="Log de Eventos", 
                    font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, padx=10, pady=10)
        
        self.log_textbox = ctk.CTkTextbox(log_frame, height=150, width=800)
        self.log_textbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Configure grid weights
        self.sensor_frame.grid_rowconfigure(2, weight=1)
        self.sensor_frame.grid_rowconfigure(3, weight=1)
        self.sensor_frame.grid_columnconfigure(0, weight=1)
        self.sensor_frame.grid_columnconfigure(1, weight=1)
        self.sensor_frame.grid_columnconfigure(2, weight=1)
        
        log_frame.grid_rowconfigure(1, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)
        
        # Inicializar display
        self.atualizar_display()
        
    def start_simulation(self):
        """Inicia a simulação dos sensores"""
        self.simulator.start_simulation()
        self.running = True
        
        # Iniciar thread para atualizar a interface
        self.atualizar_thread = threading.Thread(target=self.atualizar_loop)
        self.atualizar_thread.daemon = True
        self.atualizar_thread.start()
        
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        
        self.log_message("Simulação de sensores iniciada")
        
    def stop_simulation(self):
        """Para a simulação dos sensores"""
        self.running = False
        self.simulator.stop_simulation()
        
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        
        self.log_message("Simulação de sensores parada")
        
    def atualizar_loop(self):
        """Loop para atualizar a interface em tempo real"""
        while self.running:
            self.atualizar_display()
            time.sleep(1)
            
    def atualizar_display(self):
        """Atualiza os dados exibidos na interface"""
        try:
            # Obter dados dos sensores
            sensor_data = self.simulator.get_sensor_data()
            actuator_status = self.simulator.get_atuadores_status()
            
            # Atualizar labels dos sensores
            self.data_labels['timestamp'].configure(text=sensor_data['timestamp'])
            self.data_labels['presenca'].configure(
                text="SIM" if sensor_data['presenca'] else "NÃO",
                text_color="red" if sensor_data['presenca'] else "green"
            )
            self.data_labels['luminosidade'].configure(text=f"{sensor_data['luminosidade']:.1f}%")
            self.data_labels['temperatura'].configure(
                text=f"{sensor_data['temperatura']:.1f}°C",
                text_color="red" if sensor_data['temperatura'] > 35 else "white"
            )
            self.data_labels['fumaca'].configure(
                text="SIM" if sensor_data['fumaça'] else "NÃO",
                text_color="red" if sensor_data['fumaça'] else "green"
            )
            
            # Atualizar labels dos atuadores
            self.status_labels['alarme'].configure(
                text="ATIVO" if actuator_status['alarme'] else "INATIVO",
                text_color="red" if actuator_status['alarme'] else "green"
            )
            self.status_labels['luzes_automaticas'].configure(
                text="LIGADO" if actuator_status['luzes_automaticas'] else "DESLIGADO",
                text_color="green" if actuator_status['luzes_automaticas'] else "gray"
            )
            self.status_labels['sirene'].configure(
                text="ATIVA" if actuator_status['sirene'] else "INATIVA",
                text_color="red" if actuator_status['sirene'] else "green"
            )
            self.status_labels['ventilacao'].configure(
                text="ATIVA" if actuator_status['ventilacao'] else "INATIVA",
                text_color="blue" if actuator_status['ventilacao'] else "gray"
            )
            
        except Exception as e:
            print(f"Erro ao atualizar display: {e}")
            
    def apply_config(self):
        """Aplica as configurações inseridas pelo usuário"""
        try:
            temp_max = float(self.temp_entry.get())
            lumin_min = int(self.lumin_entry.get())
            
            self.simulator.set_config('temp_max', temp_max)
            self.simulator.set_config('luminosidade_min', lumin_min)
            
            self.log_message(f"Configurações aplicadas: Temp. Max = {temp_max}°C, Lumin. Min = {lumin_min}%")
            messagebox.showinfo("Sucesso", "Configurações aplicadas com sucesso!")
            
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos nas configurações!")
            
    def toggle_auto_lights(self):
        """Liga/desliga o controle automático de luzes"""
        self.simulator.toggle_luzes_automaticas()
        status = self.simulator.get_atuadores_status()
        status_text = "ligado" if status['luzes_automaticas'] else "desligado"
        self.log_message(f"Controle automático de luzes {status_text}")
        
    def reset_alarm(self):
        """Reseta o alarme"""
        self.simulator.reset_alarme()
        self.log_message("Alarme resetado manualmente")
        
    def test_emergency(self):
        """Executa teste de emergência"""
        self.simulator.test_emergency()
        self.log_message("Teste de emergência executado")
        
    def log_message(self, message):
        """Adiciona mensagem ao log"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_textbox.insert("end", log_entry)
        self.log_textbox.see("end")  # Scroll para o final

