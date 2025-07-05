import random
import time
from datetime import datetime
import threading

# Atividade de:

# Antony Rafael - https://github.com/MyAntony
# Débora Magalhães - https://github.com/Debs2Dev
# Brunna Barreto - https://github.com/brunnabarreto
# Luís Felipe - https://github.com/IamLiper


class SensorSimulator:
    def __init__(self):
        # Dados fictícios dos sensores
        self.sensor_data = {
            'presenca': False,
            'luminosidade': 50,  # 0-100 (0 = escuro, 100 = muito claro)
            'temperatura': 25.0,  # Celsius
            'fumaça': False,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Estados dos atuadores
        self.atuadores = {
            'alarme': False,
            'luzes_automaticas': True,
            'sirene': False,
            'ventilacao': False
        }
        
        # Configurações dos sensores
        self.config = {
            'temp_max': 35.0,  # Temperatura máxima antes de ativar sirene
            'luminosidade_min': 30,  # Luminosidade mínima para apagar luzes
            'presenca_timeout': 10  # Segundos para resetar presença
        }
        
        self.running = False
        self.thread = None
        
    def start_simulation(self):
        """Inicia a simulação dos sensores"""
        self.running = True
        self.thread = threading.Thread(target=self._simulate_sensors)
        self.thread.daemon = True
        self.thread.start()
        
    def stop_simulation(self):
        """Para a simulação dos sensores"""
        self.running = False
        if self.thread:
            self.thread.join()
            
    def _simulate_sensors(self):
        """Simula a leitura dos sensores em tempo real"""
        while self.running:
            # Simular sensor de presença (probabilidade de detecção)
            if random.random() < 0.1:  # 10% de chance de detectar movimento
                self.sensor_data['presenca'] = True
                self._check_security()
            else:
                self.sensor_data['presenca'] = False
                
            # Simular sensor de luminosidade (variação gradual)
            variation = random.uniform(-5, 5)
            new_luminosity = self.sensor_data['luminosidade'] + variation
            self.sensor_data['luminosidade'] = max(0, min(100, new_luminosity))
            self._check_lighting()
            
            # Simular sensor de temperatura (variação gradual)
            temp_variation = random.uniform(-1, 1)
            new_temp = self.sensor_data['temperatura'] + temp_variation
            self.sensor_data['temperatura'] = max(15, min(45, new_temp))
            self._check_temperature()
            
            # Simular sensor de fumaça (probabilidade baixa)
            if random.random() < 0.02:  # 2% de chance de detectar fumaça
                self.sensor_data['fumaça'] = True
                self._check_fire_safety()
            else:
                self.sensor_data['fumaça'] = False
                
            # Atualizar timestamp
            self.sensor_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            time.sleep(2)  # Atualizar a cada 2 segundos
            
    def _check_security(self):
        """Verifica segurança e ativa alarme se necessário"""
        if self.sensor_data['presenca']:
            self.atuadores['alarme'] = True
            print(f"[ALERTA] Movimento detectado! Alarme ativado às {self.sensor_data['timestamp']}")
        else:
            self.atuadores['alarme'] = False
            
    def _check_lighting(self):
        """Controla as luzes baseado na luminosidade"""
        if self.atuadores['luzes_automaticas']:
            if self.sensor_data['luminosidade'] < self.config['luminosidade_min']:
                # Acender luzes quando escuro
                print(f"[INFO] Luzes automáticas ligadas - Luminosidade: {self.sensor_data['luminosidade']:.1f}%")
            else:
                # Apagar luzes quando claro
                print(f"[INFO] Luzes automáticas desligadas - Luminosidade: {self.sensor_data['luminosidade']:.1f}%")
                
    def _check_temperature(self):
        """Verifica temperatura e ativa ventilação/sirene se necessário"""
        if self.sensor_data['temperatura'] > self.config['temp_max']:
            self.atuadores['ventilacao'] = True
            self.atuadores['sirene'] = True
            print(f"[ALERTA] Temperatura alta detectada: {self.sensor_data['temperatura']:.1f}°C - Sirene ativada!")
        else:
            self.atuadores['ventilacao'] = False
            if not self.sensor_data['fumaça']:  # Só desliga sirene se não há fumaça
                self.atuadores['sirene'] = False
                
    def _check_fire_safety(self):
        """Verifica detecção de fumaça"""
        if self.sensor_data['fumaça']:
            self.atuadores['sirene'] = True
            print(f"[EMERGÊNCIA] Fumaça detectada! Sirene de emergência ativada às {self.sensor_data['timestamp']}")
        else:
            if self.sensor_data['temperatura'] <= self.config['temp_max']:
                self.atuadores['sirene'] = False
                
    def get_sensor_data(self):
        """Retorna os dados atuais dos sensores"""
        return self.sensor_data.copy()
        
    def get_atuadores_status(self):
        """Retorna o status atual dos atuadores"""
        return self.atuadores.copy()
        
    def set_config(self, key, value):
        """Configura parâmetros dos sensores"""
        if key in self.config:
            self.config[key] = value
            print(f"[CONFIG] {key} configurado para {value}")
            
    def toggle_luzes_automaticas(self):
        """Liga/desliga o controle automático de luzes"""
        self.atuadores['luzes_automaticas'] = not self.atuadores['luzes_automaticas']
        status = "ligado" if self.atuadores['luzes_automaticas'] else "desligado"
        print(f"[CONFIG] Controle automático de luzes {status}")
        
    def reset_alarme(self):
        """Reseta o alarme manualmente"""
        self.atuadores['alarme'] = False
        print("[INFO] Alarme resetado manualmente")
        
    def test_emergency(self):
        """Testa o sistema de emergência"""
        print("[TESTE] Iniciando teste de emergência...")
        self.sensor_data['fumaça'] = True
        self.sensor_data['temperatura'] = 40.0
        self._check_fire_safety()
        self._check_temperature()
        
        # Resetar após 5 segundos
        def reset_test():
            time.sleep(5)
            self.sensor_data['fumaça'] = False
            self.sensor_data['temperatura'] = 25.0
            self.atuadores['sirene'] = False
            self.atuadores['ventilacao'] = False
            print("[TESTE] Teste de emergência finalizado")
            
        reset_thread = threading.Thread(target=reset_test)
        reset_thread.daemon = True
        reset_thread.start()

# Exemplo de uso
if __name__ == "__main__":
    simulator = SensorSimulator()
    
    print("=== LogiTrack - Simulador de Sensores IoT ===")
    print("Iniciando simulação...")
    
    simulator.start_simulation()
    
    try:
        # Simular por 30 segundos
        for i in range(15):
            time.sleep(2)
            data = simulator.get_sensor_data()
            atuadores = simulator.get_atuadores_status()
            
            print(f"\n--- Leitura {i+1} ---")
            print(f"Timestamp: {data['timestamp']}")
            print(f"Presença: {'SIM' if data['presenca'] else 'NÃO'}")
            print(f"Luminosidade: {data['luminosidade']:.1f}%")
            print(f"Temperatura: {data['temperatura']:.1f}°C")
            print(f"Fumaça: {'SIM' if data['fumaça'] else 'NÃO'}")
            print(f"Alarme: {'ATIVO' if atuadores['alarme'] else 'INATIVO'}")
            print(f"Sirene: {'ATIVA' if atuadores['sirene'] else 'INATIVA'}")
            
            # Teste de emergência no meio da simulação
            if i == 7:
                simulator.test_emergency()
                
    except KeyboardInterrupt:
        print("\nParando simulação...")
    finally:
        simulator.stop_simulation()
        print("Simulação finalizada.")

