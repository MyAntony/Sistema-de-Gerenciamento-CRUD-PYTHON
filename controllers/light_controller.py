import serial
import time

# Atividade de:

# Antony Rafael - https://github.com/MyAntony
# Débora Magalhães - https://github.com/Debs2Dev
# Brunna Barreto - https://github.com/brunnabarreto
# Luís Felipe - https://github.com/IamLiper


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
        
    def conectar_arduino(self, port_name=None):
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
            
    def desconectar_arduino(self):
        """Desconecta do Arduino"""
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            self.connected = False
            print("Desconectado do Arduino")
            
    def enviar_comando(self, command):
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
            
    def alternar_luz(self, setor):
        """Liga ou desliga a luz de um setor específico"""
        if setor not in self.setores:
            print(f"Setor '{setor}' não encontrado")
            return False
            
        status_atual = self.setores[setor]['status']
        
        if status_atual:
            # Desligar luz
            command = self.setores[setor]['off']
            self.setores[setor]['status'] = False
            action = "desligada"
        else:
            # Ligar luz
            command = self.setores[setor]['on']
            self.setores[setor]['status'] = True
            action = "ligada"
            
        sucesso = self.enviar_comando(command)
        if sucesso:
            print(f"Luz do setor '{setor}' {action}")
            
        return sucesso
        
    def acender_luz(self, setor):
        """Liga a luz de um setor específico"""
        if setor not in self.setores:
            print(f"Setor '{setor}' não encontrado")
            return False
            
        command = self.setores[setor]['on']
        sucesso = self.enviar_comando(command)
        
        if sucesso:
            self.setores[setor]['status'] = True
            print(f"Luz do setor '{setor}' ligada")
            
        return sucesso
        
    def desligar_luz(self, setor):
        """Desliga a luz de um setor específico"""
        if setor not in self.setores:
            print(f"Setor '{setor}' não encontrado")
            return False
            
        command = self.setores[setor]['off']
        sucesso = self.enviar_comando(command)
        
        if sucesso:
            self.setores[setor]['status'] = False
            print(f"Luz do setor '{setor}' desligada")
            
        return sucesso
        
    def ligar_tudo(self):
        """Liga todas as luzes"""
        sucesso_count = 0
        for setor in self.setores:
            if self.acender_luz(setor):
                sucesso_count += 1
                
        print(f"Ligadas {sucesso_count} de {len(self.setores)} luzes")
        return sucesso_count == len(self.setores)
        
    def desligar_tudo(self):
        """Desliga todas as luzes"""
        sucesso_count = 0
        for setor in self.setores:
            if self.desligar_luz(setor):
                sucesso_count += 1
                
        print(f"Desligadas {sucesso_count} de {len(self.setores)} luzes")
        return sucesso_count == len(self.setores)
        
    def verifica_status(self, setor):
        """Retorna o status de uma luz específica"""
        if setor in self.setores:
            return self.setores[setor]['status']
        return None
        
    def verifica_tudo(self):
        """Retorna o status de todas as luzes"""
        status = {}
        for setor, config in self.setores.items():
            status[setor] = config['status']
        return status
        
    def verifica_portas(self):
        """Retorna lista de portas seriais disponíveis"""
        import serial.tools.list_ports
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]
        
    def verifica_conexao(self):
        """Testa a conexão com o Arduino"""
        if not self.connected:
            return False
            
        try:
            # Enviar comando de teste (pode ser um comando específico do Arduino)
            test_command = 'T'  # Comando de teste
            return self.enviar_comando(test_command)
        except Exception as e:
            print(f"Erro no teste de conexão: {e}")
            return False

# Exemplo de uso
if __name__ == "__main__":
    controller = LightController()
    
    print("=== LogiTrack - Controlador de Luzes ===")
    
    # Tentar conectar (vai falhar se não houver Arduino conectado)
    if controller.conectar_arduino():
        print("Arduino conectado com sucesso!")
    else:
        print("Arduino não conectado - modo simulação ativado")
    
    # Demonstrar funcionalidades
    print("\nTestando controle de luzes...")
    
    # Ligar luz da oficina
    controller.acender_luz('oficina')
    
    # Ligar luzes do galpão
    controller.acender_luz('galpao_bloco1')
    controller.acender_luz('galpao_bloco2')
    controller.acender_luz('galpao_bloco3')
    
    # Mostrar status
    print("\nStatus atual das luzes:")
    status = controller.verifica_tudo()
    for setor, ligada in status.items():
        print(f"{setor}: {'LIGADA' if ligada else 'DESLIGADA'}")
    
    # Aguardar um pouco
    time.sleep(2)
    
    # Desligar todas as luzes
    print("\nDesligando todas as luzes...")
    controller.desligar_tudo()
    
    # Mostrar status final
    print("\nStatus final das luzes:")
    status = controller.verifica_tudo()
    for setor, ligada in status.items():
        print(f"{setor}: {'LIGADA' if ligada else 'DESLIGADA'}")
    
    # Desconectar
    controller.desconectar_arduino()
    print("\nTeste finalizado.")

