// Código Arduino para Controle de Luzes - LogiTrack
// Este código recebe comandos via Serial para controlar luzes de diferentes setores

// Definição dos pinos para cada setor
const int LED_OFICINA = 2;        // Pino para LED da oficina
const int LED_GALPAO_1 = 3;       // Pino para LED do galpão bloco 1
const int LED_GALPAO_2 = 4;       // Pino para LED do galpão bloco 2
const int LED_GALPAO_3 = 5;       // Pino para LED do galpão bloco 3
const int LED_ESCRITORIO = 6;     // Pino para LED do escritório
const int LED_CORREDOR = 7;       // Pino para LED do corredor
const int LED_AREA_SERVICO = 8;   // Pino para LED da área de serviço
const int LED_AREA_EXTERNA = 9;   // Pino para LED da área externa

// Variáveis para armazenar o estado das luzes
bool estadoOficina = false;
bool estadoGalpao1 = false;
bool estadoGalpao2 = false;
bool estadoGalpao3 = false;
bool estadoEscritorio = false;
bool estadoCorredor = false;
bool estadoAreaServico = false;
bool estadoAreaExterna = false;

void setup() {
  // Inicializar comunicação serial
  Serial.begin(9600);
  
  // Configurar todos os pinos como saída
  pinMode(LED_OFICINA, OUTPUT);
  pinMode(LED_GALPAO_1, OUTPUT);
  pinMode(LED_GALPAO_2, OUTPUT);
  pinMode(LED_GALPAO_3, OUTPUT);
  pinMode(LED_ESCRITORIO, OUTPUT);
  pinMode(LED_CORREDOR, OUTPUT);
  pinMode(LED_AREA_SERVICO, OUTPUT);
  pinMode(LED_AREA_EXTERNA, OUTPUT);
  
  // Inicializar todas as luzes desligadas
  apagarTodasLuzes();
  
  Serial.println("=== LogiTrack - Sistema de Controle de Luzes ===");
  Serial.println("Sistema inicializado!");
  Serial.println("Comandos disponíveis:");
  Serial.println("A/a - Oficina (Ligar/Desligar)");
  Serial.println("B/b - Galpão Bloco 1 (Ligar/Desligar)");
  Serial.println("C/c - Galpão Bloco 2 (Ligar/Desligar)");
  Serial.println("D/d - Galpão Bloco 3 (Ligar/Desligar)");
  Serial.println("E/e - Escritório (Ligar/Desligar)");
  Serial.println("F/f - Corredor (Ligar/Desligar)");
  Serial.println("G/g - Área de Serviço (Ligar/Desligar)");
  Serial.println("H/h - Área Externa (Ligar/Desligar)");
  Serial.println("T - Teste de conexão");
  Serial.println("S - Status de todas as luzes");
  Serial.println("Aguardando comandos...");
}

void loop() {
  // Verificar se há dados disponíveis na serial
  if (Serial.available() > 0) {
    char comando = Serial.read();
    processarComando(comando);
  }
  
  // Pequena pausa para evitar sobrecarga
  delay(50);
}

void processarComando(char comando) {
  switch (comando) {
    // Oficina
    case 'A':
      ligarLuz(LED_OFICINA, "Oficina");
      estadoOficina = true;
      break;
    case 'a':
      desligarLuz(LED_OFICINA, "Oficina");
      estadoOficina = false;
      break;
      
    // Galpão Bloco 1
    case 'B':
      ligarLuz(LED_GALPAO_1, "Galpão Bloco 1");
      estadoGalpao1 = true;
      break;
    case 'b':
      desligarLuz(LED_GALPAO_1, "Galpão Bloco 1");
      estadoGalpao1 = false;
      break;
      
    // Galpão Bloco 2
    case 'C':
      ligarLuz(LED_GALPAO_2, "Galpão Bloco 2");
      estadoGalpao2 = true;
      break;
    case 'c':
      desligarLuz(LED_GALPAO_2, "Galpão Bloco 2");
      estadoGalpao2 = false;
      break;
      
    // Galpão Bloco 3
    case 'D':
      ligarLuz(LED_GALPAO_3, "Galpão Bloco 3");
      estadoGalpao3 = true;
      break;
    case 'd':
      desligarLuz(LED_GALPAO_3, "Galpão Bloco 3");
      estadoGalpao3 = false;
      break;
      
    // Escritório
    case 'E':
      ligarLuz(LED_ESCRITORIO, "Escritório");
      estadoEscritorio = true;
      break;
    case 'e':
      desligarLuz(LED_ESCRITORIO, "Escritório");
      estadoEscritorio = false;
      break;
      
    // Corredor
    case 'F':
      ligarLuz(LED_CORREDOR, "Corredor");
      estadoCorredor = true;
      break;
    case 'f':
      desligarLuz(LED_CORREDOR, "Corredor");
      estadoCorredor = false;
      break;
      
    // Área de Serviço
    case 'G':
      ligarLuz(LED_AREA_SERVICO, "Área de Serviço");
      estadoAreaServico = true;
      break;
    case 'g':
      desligarLuz(LED_AREA_SERVICO, "Área de Serviço");
      estadoAreaServico = false;
      break;
      
    // Área Externa
    case 'H':
      ligarLuz(LED_AREA_EXTERNA, "Área Externa");
      estadoAreaExterna = true;
      break;
    case 'h':
      desligarLuz(LED_AREA_EXTERNA, "Área Externa");
      estadoAreaExterna = false;
      break;
      
    // Comando de teste
    case 'T':
    case 't':
      Serial.println("TESTE: Conexão OK - Sistema funcionando!");
      piscarTodasLuzes();
      break;
      
    // Status de todas as luzes
    case 'S':
    case 's':
      mostrarStatus();
      break;
      
    default:
      Serial.print("Comando não reconhecido: ");
      Serial.println(comando);
      break;
  }
}

void ligarLuz(int pino, String setor) {
  digitalWrite(pino, HIGH);
  Serial.print("LUZ LIGADA: ");
  Serial.println(setor);
}

void desligarLuz(int pino, String setor) {
  digitalWrite(pino, LOW);
  Serial.print("LUZ DESLIGADA: ");
  Serial.println(setor);
}

void apagarTodasLuzes() {
  digitalWrite(LED_OFICINA, LOW);
  digitalWrite(LED_GALPAO_1, LOW);
  digitalWrite(LED_GALPAO_2, LOW);
  digitalWrite(LED_GALPAO_3, LOW);
  digitalWrite(LED_ESCRITORIO, LOW);
  digitalWrite(LED_CORREDOR, LOW);
  digitalWrite(LED_AREA_SERVICO, LOW);
  digitalWrite(LED_AREA_EXTERNA, LOW);
  
  // Atualizar estados
  estadoOficina = false;
  estadoGalpao1 = false;
  estadoGalpao2 = false;
  estadoGalpao3 = false;
  estadoEscritorio = false;
  estadoCorredor = false;
  estadoAreaServico = false;
  estadoAreaExterna = false;
}

void piscarTodasLuzes() {
  Serial.println("Executando teste - piscando todas as luzes...");
  
  // Ligar todas
  digitalWrite(LED_OFICINA, HIGH);
  digitalWrite(LED_GALPAO_1, HIGH);
  digitalWrite(LED_GALPAO_2, HIGH);
  digitalWrite(LED_GALPAO_3, HIGH);
  digitalWrite(LED_ESCRITORIO, HIGH);
  digitalWrite(LED_CORREDOR, HIGH);
  digitalWrite(LED_AREA_SERVICO, HIGH);
  digitalWrite(LED_AREA_EXTERNA, HIGH);
  
  delay(500);
  
  // Desligar todas
  apagarTodasLuzes();
  delay(500);
  
  // Repetir mais uma vez
  digitalWrite(LED_OFICINA, HIGH);
  digitalWrite(LED_GALPAO_1, HIGH);
  digitalWrite(LED_GALPAO_2, HIGH);
  digitalWrite(LED_GALPAO_3, HIGH);
  digitalWrite(LED_ESCRITORIO, HIGH);
  digitalWrite(LED_CORREDOR, HIGH);
  digitalWrite(LED_AREA_SERVICO, HIGH);
  digitalWrite(LED_AREA_EXTERNA, HIGH);
  
  delay(500);
  apagarTodasLuzes();
  
  Serial.println("Teste concluído!");
}

void mostrarStatus() {
  Serial.println("=== STATUS DAS LUZES ===");
  Serial.print("Oficina: ");
  Serial.println(estadoOficina ? "LIGADA" : "DESLIGADA");
  Serial.print("Galpão Bloco 1: ");
  Serial.println(estadoGalpao1 ? "LIGADA" : "DESLIGADA");
  Serial.print("Galpão Bloco 2: ");
  Serial.println(estadoGalpao2 ? "LIGADA" : "DESLIGADA");
  Serial.print("Galpão Bloco 3: ");
  Serial.println(estadoGalpao3 ? "LIGADA" : "DESLIGADA");
  Serial.print("Escritório: ");
  Serial.println(estadoEscritorio ? "LIGADA" : "DESLIGADA");
  Serial.print("Corredor: ");
  Serial.println(estadoCorredor ? "LIGADA" : "DESLIGADA");
  Serial.print("Área de Serviço: ");
  Serial.println(estadoAreaServico ? "LIGADA" : "DESLIGADA");
  Serial.print("Área Externa: ");
  Serial.println(estadoAreaExterna ? "LIGADA" : "DESLIGADA");
  Serial.println("========================");
}

