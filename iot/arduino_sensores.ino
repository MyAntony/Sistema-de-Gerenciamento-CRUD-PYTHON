// Código Arduino para Sensores IoT - LogiTrack
// Este código lê sensores de presença/distância, luminosidade e temperatura
// e envia os dados via Monitor Serial

/*
Atividade de:

Antony Rafael - https://github.com/MyAntony
Débora Magalhães - https://github.com/Debs2Dev
Brunna Barreto - https://github.com/brunnabarreto
Luís Felipe - https://github.com/IamLiper
*/

// Definição dos pinos
const int SENSOR_DISTANCIA_TRIG = 2;
const int SENSOR_DISTANCIA_ECHO = 3;
const int SENSOR_LDR = A0;  // Sensor de luminosidade (LDR)
const int SENSOR_TEMP = A1; // Sensor de temperatura (TMP36)
const int LED_ALARME = 13;  // LED para simular alarme
const int BUZZER = 12;      // Buzzer para sirene

// Variáveis globais
long duracao;
int distancia;
int luminosidade;
float temperatura;
bool presencaDetectada = false;
bool fumacaDetectada = false;

// Configurações
const int DISTANCIA_LIMITE = 20; // cm - distância para detectar presença
const int LUMINOSIDADE_MIN = 30; // Valor mínimo para considerar escuro
const float TEMP_MAX = 35.0;     // Temperatura máxima antes de ativar sirene

void setup() {
  // Inicializar comunicação serial
  Serial.begin(9600);
  
  // Configurar pinos do sensor ultrassônico
  pinMode(SENSOR_DISTANCIA_TRIG, OUTPUT);
  pinMode(SENSOR_DISTANCIA_ECHO, INPUT);
  
  // Configurar pinos de saída
  pinMode(LED_ALARME, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  
  // Inicializar com LEDs desligados
  digitalWrite(LED_ALARME, LOW);
  digitalWrite(BUZZER, LOW);
  
  Serial.println("=== LogiTrack - Sistema de Sensores IoT ===");
  Serial.println("Sistema inicializado!");
  Serial.println("Formato: PRESENCA,LUMINOSIDADE,TEMPERATURA,FUMACA");
  delay(2000);
}

void loop() {
  // Ler sensor de distância (simula presença)
  lerSensorDistancia();
  
  // Ler sensor de luminosidade
  lerSensorLuminosidade();
  
  // Ler sensor de temperatura
  lerSensorTemperatura();
  
  // Simular detecção de fumaça (aleatório)
  simularDeteccaoFumaca();
  
  // Processar lógica de segurança
  processarSeguranca();
  
  // Enviar dados via serial
  enviarDadosSerial();
  
  // Aguardar antes da próxima leitura
  delay(2000);
}

void lerSensorDistancia() {
  // Limpar o pino trigger
  digitalWrite(SENSOR_DISTANCIA_TRIG, LOW);
  delayMicroseconds(2);
  
  // Enviar pulso de 10 microssegundos
  digitalWrite(SENSOR_DISTANCIA_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(SENSOR_DISTANCIA_TRIG, LOW);
  
  // Ler o tempo de retorno do echo
  duracao = pulseIn(SENSOR_DISTANCIA_ECHO, HIGH);
  
  // Calcular distância em cm
  distancia = duracao * 0.034 / 2;
  
  // Verificar se há presença
  if (distancia > 0 && distancia <= DISTANCIA_LIMITE) {
    presencaDetectada = true;
  } else {
    presencaDetectada = false;
  }
}

void lerSensorLuminosidade() {
  // Ler valor do LDR (0-1023)
  int valorLDR = analogRead(SENSOR_LDR);
  
  // Converter para porcentagem (0-100%)
  luminosidade = map(valorLDR, 0, 1023, 0, 100);
}

void lerSensorTemperatura() {
  // Ler valor do sensor TMP36
  int valorTemp = analogRead(SENSOR_TEMP);
  
  // Converter para voltagem
  float voltagem = valorTemp * (5.0 / 1023.0);
  
  // Converter para temperatura em Celsius
  temperatura = (voltagem - 0.5) * 100.0;
}

void simularDeteccaoFumaca() {
  // Simular detecção de fumaça com probabilidade baixa
  // Em um projeto real, seria conectado um sensor MQ-2 ou similar
  int random_val = random(0, 100);
  if (random_val < 2) { // 2% de chance
    fumacaDetectada = true;
  } else {
    fumacaDetectada = false;
  }
}

void processarSeguranca() {
  // Processar alarme de presença
  if (presencaDetectada) {
    digitalWrite(LED_ALARME, HIGH);
  } else {
    digitalWrite(LED_ALARME, LOW);
  }
  
  // Processar sirene por temperatura alta ou fumaça
  if (temperatura > TEMP_MAX || fumacaDetectada) {
    // Ativar sirene (buzzer intermitente)
    digitalWrite(BUZZER, HIGH);
    delay(100);
    digitalWrite(BUZZER, LOW);
    delay(100);
    digitalWrite(BUZZER, HIGH);
    delay(100);
    digitalWrite(BUZZER, LOW);
  } else {
    digitalWrite(BUZZER, LOW);
  }
}

void enviarDadosSerial() {
  // Enviar dados no formato CSV
  Serial.print(presencaDetectada ? "1" : "0");
  Serial.print(",");
  Serial.print(luminosidade);
  Serial.print(",");
  Serial.print(temperatura, 1);
  Serial.print(",");
  Serial.print(fumacaDetectada ? "1" : "0");
  Serial.println();
  
  // Enviar dados formatados para debug (opcional)
  /*
  Serial.println("--- Leitura dos Sensores ---");
  Serial.print("Presença: ");
  Serial.println(presencaDetectada ? "DETECTADA" : "NÃO DETECTADA");
  Serial.print("Distância: ");
  Serial.print(distancia);
  Serial.println(" cm");
  Serial.print("Luminosidade: ");
  Serial.print(luminosidade);
  Serial.println("%");
  Serial.print("Temperatura: ");
  Serial.print(temperatura);
  Serial.println("°C");
  Serial.print("Fumaça: ");
  Serial.println(fumacaDetectada ? "DETECTADA" : "NÃO DETECTADA");
  Serial.println("---------------------------");
  */
}

