#include <WiFi.h>
#include <ezTime.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <DHT.h>
#include <esp_sleep.h>
#include "esp_system.h"
#include "driver/usb_serial_jtag.h"

// wifi module
#include "arduino_secrets.h" 

const char* ssid     = SECRET_SSID;
const char* password = SECRET_PASS;
const char* mqttuser = SECRET_MQTTUSER;
const char* mqttpass = SECRET_MQTTPASS;
char* topic_1 = "student/CASA0022/zczqrua/weather/";

const char* mqtt_server = "mqtt.cetools.org";
WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
float value = 0;

int v=0;
unsigned long currentMillis = 0;

// Wind Speed Module
unsigned long windSpeedDetectLastTime = 0;
int windSpeedPluse = 0;
float windSpeed = 0;  
const long windSpeedInterval = 14000;
char windSpeedStr[10];
#define WindSpeedPin D2

// Lux Module 
uint16_t lux = 0;
char luxStr[10];
#define SDAPin A4
#define SCLPin A5

// DHT Module
#define DHTPIN D3
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);
float temperature = 0;
float humidity = 0;
char tempStr[10];
char humStr[10];

// RainDetectModule
#define RAINDETECTPIN A6
int rainDetectValue = 0;
char rainStr[10];

// Date and time
Timezone GB;

// Sleep Module
int wakeTime = 15;
int sleepTime = 285;

void setup() {
  Wire.begin(SDAPin,SCLPin);
  Serial.begin(115200);
  delay(100);
  startWifi();
  //syncDate();
  dht.begin();
  pinMode(RAINDETECTPIN, INPUT);
  //start MQTT server
  client.setServer(mqtt_server, 1884);
  client.setCallback(callback);
  pinMode(WindSpeedPin,INPUT_PULLUP);
  // Enable timer wakeup
  uint64_t sleepDuration = (uint64_t)sleepTime * 1000000ULL;
  Serial.print("Setting sleep duration (microseconds): ");
  Serial.println(sleepDuration);
  esp_sleep_enable_timer_wakeup(sleepDuration);

  // Detect wind speed sensor pulses
  attachInterrupt(digitalPinToInterrupt(WindSpeedPin), blink, CHANGE);
}

void loop() {
  // put your main code here, to run repeatedly:
  //sendMQTT(topic_1,"test","20");
  //Serial.println(speed);
  delay(10);
  //v=analogRead(0);
  //Serial.println(v);
  currentMillis = millis();
  if(currentMillis - windSpeedDetectLastTime >= windSpeedInterval){
    readWindSpeed();
    dtostrf(windSpeed, 0, 2, windSpeedStr);
    sendMQTT(topic_1,"windSpeed",windSpeedStr);

    readLux();
    dtostrf(lux, 0, 0, luxStr);
    sendMQTT(topic_1,"lux",luxStr);

    readDHT22();
    dtostrf(temperature, 0, 1, tempStr);
    sendMQTT(topic_1,"temp",tempStr);
    dtostrf(humidity, 0, 1, humStr);
    sendMQTT(topic_1,"hum",humStr);

    readRainDetector();
    dtostrf(rainDetectValue, 0, 0, rainStr);
    sendMQTT(topic_1,"rain",rainStr);
  }

  if (currentMillis >= 1000 * wakeTime){
    Serial.println("Go sleep ");
    Serial.println(currentMillis);
    delay(1000);
    WiFi.disconnect(true);  
    WiFi.mode(WIFI_OFF);    
    configureAllPinsAsInput();
    Serial.end(); 
    disableUnusedPowerDomains();
    esp_deep_sleep_start();
  }
}


void disableUnusedPowerDomains() {
  // 关闭未使用的外设电源域
  esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_PERIPH, ESP_PD_OPTION_OFF);
  esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_SLOW_MEM, ESP_PD_OPTION_OFF);
  esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_FAST_MEM, ESP_PD_OPTION_OFF);
}

void blink(){
  windSpeedPluse++;
}

void readDHT22(){
  temperature = dht.readTemperature();
  humidity = dht.readHumidity();
  Serial.print("Temp:");
  Serial.println(temperature,2);
  Serial.print("Humidity:");
  Serial.println(humidity,2);
}

void readRainDetector(){
  rainDetectValue = analogRead(RAINDETECTPIN);
  Serial.print("rain value:");
  Serial.println(rainDetectValue);
}


void readWindSpeed(){
  unsigned long detectInterval = currentMillis - windSpeedDetectLastTime;
  windSpeed =  windSpeedPluse *1000.0 * 1.75 / detectInterval / 40 ;
  Serial.print("Wind speed:");
  Serial.println(windSpeed,2);
  windSpeedDetectLastTime = millis();
  windSpeedPluse = 0;
}

void readLux(){
  Wire.beginTransmission(0x23);
  Wire.write(0x23);
  Wire.endTransmission();

  delay(24); 
  
  Wire.requestFrom(0x23, 2); 

  if (Wire.available() == 2) {
    uint8_t highByte = Wire.read(); 
    uint8_t lowByte = Wire.read(); 
    lux = (highByte << 8) | lowByte; 
    lux = lux / 1.2; 
  }
  Serial.print("lux:");
  Serial.println(lux);
}


void startWifi() {
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  // check to see if connected and wait until you are
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  String macAddress = WiFi.macAddress();
  Serial.print("ESP32 MAC Address: ");
  Serial.println(macAddress);
}

void sendMQTT(char* topic, char* name, char* msg){
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  char fullTopic[100]; // Ensure this buffer is large enough to hold the concatenated string
  snprintf(fullTopic, sizeof(fullTopic), "%s%s", topic, name);
  client.publish(fullTopic, msg);
}

void syncDate() {
  // get real date and time
  waitForSync();
  Serial.println("UTC: " + UTC.dateTime());
  GB.setLocation("Europe/London");
  Serial.println("London time: " + GB.dateTime());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Switch on the LED if an 1 was received as first character
  if ((char)payload[0] == '1') {
    digitalWrite(14, LOW);   // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because it is active low on the ESP-01)
  } else {
    digitalWrite(14, HIGH);  // Turn the LED off by making the voltage HIGH
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    
    // Attempt to connect with clientID, username and password
    if (client.connect(clientId.c_str(), mqttuser, mqttpass)) {
      Serial.println("connected");
      // ... and resubscribe
      client.subscribe("student/CASA0014/plant/zczqrua/inTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void configureAllPinsAsInput() {
  for (int pin = 0; pin < GPIO_NUM_MAX; pin++) {
    pinMode(pin, INPUT);
  }
}