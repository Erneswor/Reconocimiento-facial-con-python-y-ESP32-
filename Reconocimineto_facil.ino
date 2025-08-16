// ======== CONFIGURACIÓN DE BLYNK ========
#define BLYNK_TEMPLATE_ID "TMPL2md7hYcR4"
#define BLYNK_TEMPLATE_NAME "FocoCopy"
#define BLYNK_AUTH_TOKEN "nZagGJPH_bGR0mSx72giyQx4DO80iVVr"

// ======== LIBRERÍAS ========
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <BlynkSimpleEsp32.h>
#include <DHT.h>
#include <ESP32Servo.h>
#include <UniversalTelegramBot.h>

// ======== CONFIGURACIÓN WiFi ========
char ssid[] = "UD4-Administrativo";
char pass[] = "AdmonUPT";

//char ssid[] = "INFINITUM52F8";
//char pass[] = "nP2XU7uk7c";

// ======== CONFIGURACIÓN TELEGRAM ========
#define BOTtoken "8066175899:AAGLbSi6z1QkbzB9t79w4WSLUux-qb2t2tY" // Cambia por tu token
#define CHAT_ID "6204349968"             // Cambia por tu chat ID
WiFiClientSecure client;
UniversalTelegramBot bot(BOTtoken, client);

// ======== PINES ========
#define pinServo 4
#define pinLED 13
#define pinBuzzer 12
#define pinVentilador 5
#define DHTPIN 15        // Pin DHT11
#define DHTTYPE DHT11    // Tipo de sensor

// ======== VARIABLES ========
Servo servo;
bool sistemaActivo = false;
unsigned long tiempoDesactivacion = 0;
float temperatura = 0;
BlynkTimer timer;

DHT dht(DHTPIN, DHTTYPE);

// ======== SETUP ========
void setup() {
  Serial.begin(115200);
  
  // Conexión WiFi y Blynk
  WiFi.begin(ssid, pass);
  client.setInsecure(); // Necesario para Telegram
  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);

  // Inicializar pines
  servo.attach(pinServo);
  pinMode(pinLED, OUTPUT);
  pinMode(pinBuzzer, OUTPUT);
  pinMode(pinVentilador, OUTPUT);
  servo.write(0);  

  dht.begin();

  // Temporizador para leer temperatura
  timer.setInterval(2000L, leerTemperatura);

  Serial.println("✅ Sistema listo, esperando señal de Python...");
}

// ======== LOOP PRINCIPAL ========
void loop() {
  Blynk.run();
  timer.run();

  // Esperar señal de Python por Serial
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();
    if (comando == "ACTIVAR" && !sistemaActivo) {
      activarSistema();
    }
  }

  // Apagar sistema tras 5 segundos
  if (sistemaActivo && millis() - tiempoDesactivacion >= 5000) {
    desactivarSistema();
  }
}

// ======== LECTURA DE TEMPERATURA ========
void leerTemperatura() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    Serial.println("❌ Error al leer DHT11");
    return;
  }

  temperatura = t;

  Blynk.virtualWrite(V2, temperatura);
  Blynk.virtualWrite(V1, h);
  

  Serial.print("🌡 Temperatura: ");
  Serial.print(t);
  Serial.print(" °C | 💧 Humedad: ");
  Serial.print(h);
  Serial.println(" %");

  // Control automático del ventilador
  if (temperatura > 25.0) {
    digitalWrite(pinVentilador, HIGH);
    Blynk.virtualWrite(V0, 1);
  } else {
    digitalWrite(pinVentilador, LOW);
    Blynk.virtualWrite(V0, 0);
  }

  
}

// ======== ACTIVAR SISTEMA ========
void activarSistema() {
  sistemaActivo = true;
  tiempoDesactivacion = millis();

  digitalWrite(pinLED, HIGH);
  tone(pinBuzzer, 1000, 2000);
  
  servo.write(90);  

  Blynk.logEvent("sistema_activado", "Sistema activado por gesto de 4 dedos");

  bot.sendMessage(CHAT_ID, "🚨 Sistema activado: Usuario reconocido", "");

  Serial.println("✅ Sistema activado por Python");
  delay(2000);
}

// ======== DESACTIVAR SISTEMA ========
void desactivarSistema() {
  sistemaActivo = false;
  digitalWrite(pinLED, LOW);
  noTone(pinBuzzer);
  servo.write(0);
 
  bot.sendMessage(CHAT_ID, "✅ Sistema desactivado", "");

  Serial.println("🔕 Sistema desactivado");
  delay(2000);
}

// Esta función de ventilador
BLYNK_WRITE(V0) {  // V0 es el pin virtual del botón
  int valor = param.asInt();  // 1 si está encendido, 0 si está apagado
  if (valor == 1) {
    digitalWrite(pinVentilador, HIGH);
    Serial.println("Ventilador ENCENDIDO desde Blynk");
    bot.sendMessage(CHAT_ID, "✅ Ventilador ENCENDIDO desde Blynk", "");
  } else {
    digitalWrite(pinVentilador, LOW);
    Serial.println("Ventilador APAGADO desde Blynk");
    bot.sendMessage(CHAT_ID, "🚨 Ventilador DESACTIVADO desde Blynk", "");
  }
}



