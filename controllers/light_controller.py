import serial
import time

class LightController:
    def __init__(self):
        # Mapeamento dos setores e seus caracteres de controle
        self.setores = {
            'oficina': {'on': 'A', 'off': 'a', 'status': False},
            'galpao_bloco1': {'on': 'B', 'off': 'b', 'status': False},
            'galpao_bloco2': {'on': 'C', 'off': 'c', 'status': False},
            'galpao_bloco3': {'on': 'D', 'off': 'd', 'status': False},
            'escritorio': {'on': 'E', 'off': 'e', 'status': False},
            'corredor': {'on': 'F', 'off': 'f', 'status': False},
            'area_servico': {'on': 'G', 'off': 'g', 'status': False},
            'area_externa': {'on': 'H', 'off': 'h', 'status': False}
        }
        
        # Configurações da comunicação serial
        self.serial_port = None
        self.port_name = 'COM3'  # Porta padrão (pode ser alterada)
        self.baud_rate = 9600
        self.connected = False
        
    def connect_arduino(self, port_name=None):
        """Conecta com o Arduino via serial"""
        if port_name:
            self.port_name = port_name
            
        try:
            self.serial_port = serial.Serial(self.port_name, self.baud_rate, timeout=1)
            time.sleep(2)  # Aguardar inicialização do Arduino
            self.connected = True
            print(f"Conectado ao Arduino na porta {self.port_name}")
            return True
        except serial.SerialException as e:
            print(f"Erro ao conectar com Arduino: {e}")
            self.connected = False
            return False
        except Exception as e:
            print(f"Erro inesperado: {e}")
            self.connected = False
            return False
            
    def disconnect_arduino(self):
        """Desconecta do Arduino"""
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            self.connected = False
            print("Desconectado do Arduino")
            
    def send_command(self, command):
        """Envia comando para o Arduino"""
        if not self.connected or not self.serial_port:
            print(f"Simulando envio do comando: {command}")
            return True  # Simular sucesso quando não conectado
            
        try:
            self.serial_port.write(command.encode())
            time.sleep(0.1)  # Pequena pausa para processamento
            print(f"Comando enviado: {command}")
            return True
        except Exception as e:
            print(f"Erro ao enviar comando: {e}")
            return False
            
    def toggle_light(self, setor):
        """Liga ou desliga a luz de um setor específico"""
        if setor not in self.setores:
            print(f"Setor '{setor}' não encontrado")
            return False
            
        current_status = self.setores[setor]['status']
        
        if current_status:
            # Desligar luz
            command = self.setores[setor]['off']
            self.setores[setor]['status'] = False
            action = "desligada"
        else:
            # Ligar luz
            command = self.setores[setor]['on']
            self.setores[setor]['status'] = True
            action = "ligada"
            
        success = self.send_command(command)
        if success:
            print(f"Luz do setor '{setor}' {action}")
            
        return success
        
    def turn_on_light(self, setor):
        """Liga a luz de um setor específico"""
        if setor not in self.setores:
            print(f"Setor '{setor}' não encontrado")
            return False
            
        command = self.setores[setor]['on']
        success = self.send_command(command)
        
        if success:
            self.setores[setor]['status'] = True
            print(f"Luz do setor '{setor}' ligada")
            
        return success
        
    def turn_off_light(self, setor):
        """Desliga a luz de um setor específico"""
        if setor not in self.setores:
            print(f"Setor '{setor}' não encontrado")
            return False
            
        command = self.setores[setor]['off']
        success = self.send_command(command)
        
        if success:
            self.setores[setor]['status'] = False
            print(f"Luz do setor '{setor}' desligada")
            
        return success
        
    def turn_on_all_lights(self):
        """Liga todas as luzes"""
        success_count = 0
        for setor in self.setores:
            if self.turn_on_light(setor):
                success_count += 1
                
        print(f"Ligadas {success_count} de {len(self.setores)} luzes")
        return success_count == len(self.setores)
        
    def turn_off_all_lights(self):
        """Desliga todas as luzes"""
        success_count = 0
        for setor in self.setores:
            if self.turn_off_light(setor):
                success_count += 1
                
        print(f"Desligadas {success_count} de {len(self.setores)} luzes")
        return success_count == len(self.setores)
        
    def get_light_status(self, setor):
        """Retorna o status de uma luz específica"""
        if setor in self.setores:
            return self.setores[setor]['status']
        return None
        
    def get_all_status(self):
        """Retorna o status de todas as luzes"""
        status = {}
        for setor, config in self.setores.items():
            status[setor] = config['status']
        return status
        
    def get_available_ports(self):
        """Retorna lista de portas seriais disponíveis"""
        import serial.tools.list_ports
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]
        
    def test_connection(self):
        """Testa a conexão com o Arduino"""
        if not self.connected:
            return False
            
        try:
            # Enviar comando de teste (pode ser um comando específico do Arduino)
            test_command = 'T'  # Comando de teste
            return self.send_command(test_command)
        except Exception as e:
            print(f"Erro no teste de conexão: {e}")
            return False

# Exemplo de uso
if __name__ == "__main__":
    controller = LightController()
    
    print("=== LogiTrack - Controlador de Luzes ===")
    
    # Tentar conectar (vai falhar se não houver Arduino conectado)
    if controller.connect_arduino():
        print("Arduino conectado com sucesso!")
    else:
        print("Arduino não conectado - modo simulação ativado")
    
    # Demonstrar funcionalidades
    print("\nTestando controle de luzes...")
    
    # Ligar luz da oficina
    controller.turn_on_light('oficina')
    
    # Ligar luzes do galpão
    controller.turn_on_light('galpao_bloco1')
    controller.turn_on_light('galpao_bloco2')
    controller.turn_on_light('galpao_bloco3')
    
    # Mostrar status
    print("\nStatus atual das luzes:")
    status = controller.get_all_status()
    for setor, ligada in status.items():
        print(f"{setor}: {'LIGADA' if ligada else 'DESLIGADA'}")
    
    # Aguardar um pouco
    time.sleep(2)
    
    # Desligar todas as luzes
    print("\nDesligando todas as luzes...")
    controller.turn_off_all_lights()
    
    # Mostrar status final
    print("\nStatus final das luzes:")
    status = controller.get_all_status()
    for setor, ligada in status.items():
        print(f"{setor}: {'LIGADA' if ligada else 'DESLIGADA'}")
    
    # Desconectar
    controller.disconnect_arduino()
    print("\nTeste finalizado.")

