#include <OneWire.h>
#include <DallasTemperature.h>

// --- Pines ---
#define PH_PIN A0
#define TDS_PIN A1
#define ORP_PIN A2
#define TEMP_PIN 2

#define RELAY_BUENA 13
#define RELAY_MALA 12

OneWire oneWire(TEMP_PIN);
DallasTemperature sensors(&oneWire);

// --- Variables globales ---
float temperaturaC;
float voltajePH, voltajeTDS, voltajeORP;
float pH_raw, pH_corr;
float K, CE_corr, TDS_corr, ORP;

const float tempCoef = 0.02;
const float pH_cal = 6.92;

// --- Control de litros ---
unsigned long tiempoInicio = 0;
unsigned long tiempoBombeo = 10000; // 10 segundos = 5 litros
bool bombeando = false;
bool bombaBuenaActiva = false;
bool bombaMalaActiva = false;

void setup() {
  Serial.begin(9600);
  sensors.begin();

  pinMode(RELAY_BUENA, OUTPUT);
  pinMode(RELAY_MALA, OUTPUT);

  // Apagar al inicio
  digitalWrite(RELAY_BUENA, LOW);
  digitalWrite(RELAY_MALA, LOW);

}

void loop() {

  // Lectura temperatura
  sensors.requestTemperatures();
  temperaturaC = sensors.getTempCByIndex(0);

  // Sensores
  voltajePH = analogRead(PH_PIN)*(-0.0341)+38.1;
  voltajeTDS = analogRead(TDS_PIN)*(4.8711)-248.25;

  pH_raw = voltajePH;
  pH_corr = pH_cal - (298.15 / (temperaturaC + 273.15)) * (pH_cal - pH_raw);

  K = (voltajeTDS)*(-0.0005)+1.3704;
  CE_corr = (voltajeTDS / K);
  TDS_corr = voltajeTDS;

  
  ORP = voltajeORP;

  // --- Impresión por Serial (una línea por parámetro, con '=') ---
  
  /*
  Serial.print("Temperatura="); Serial.println(temperaturaC);
  Serial.print("pH_sin_correccion="); Serial.println(pH_raw, 3);
  Serial.print("pH_corregido="); Serial.println(pH_corr, 3);
  Serial.print("Constante_K="); Serial.println(K, 0);

  Serial.print("CE_ajustado="); Serial.println(CE_corr, 0);
  Serial.print("TDS_ppm="); Serial.println(TDS_corr, 0);
  */



  Serial.print(temperaturaC); Serial.print(",");  
  Serial.print(pH_corr, 3); Serial.print(","); 
  Serial.print(CE_corr, 0); Serial.print(",");
  Serial.println(TDS_corr, 0);

  bool agua_en_rango = (pH_corr >= 6.5 && pH_corr <= 8.5) && (TDS_corr < 1000);
  bool agua_fuera_rango = !agua_en_rango;

  // ----------------------
  //   SISTEMA DE 5 LITROS
  // ----------------------

  // Si se está bombeando, revisa si ya pasaron los 10 segundos
  if (bombeando) {
    if (millis() - tiempoInicio >= tiempoBombeo) {
      digitalWrite(RELAY_BUENA, LOW);
      digitalWrite(RELAY_MALA, LOW);
      bombeando = false;
      bombaBuenaActiva = false;
      bombaMalaActiva = false;
    }
    return; // No volver a activar bombas
  }

  // ----------------------
  //   LÓGICA DE ACTIVACIÓN
  // ----------------------

  if (agua_en_rango) {

    digitalWrite(RELAY_MALA, LOW);
    digitalWrite(RELAY_BUENA, HIGH);

    tiempoInicio = millis();
    bombeando = true;
    bombaBuenaActiva = true;
  }
  else if (agua_fuera_rango) {

    digitalWrite(RELAY_BUENA, LOW);
    digitalWrite(RELAY_MALA, HIGH);

    tiempoInicio = millis();
    bombeando = true;
    bombaMalaActiva = true;
  }

  delay(5000);
}
