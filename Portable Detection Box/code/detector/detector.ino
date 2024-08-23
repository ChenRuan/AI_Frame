#include <ESP8266WiFi.h>
#include <ezTime.h>
#include <PubSubClient.h>
#include <Wire.h>

// wifi module
#include "arduino_secrets.h" 
#include <time.h>

// 定义工作和睡眠时间
const int startHour = 8;
const int endHour = 18;
const int workDuration = 2 * 60 * 1000;  // 2分钟
const int sleepDuration = 10 * 60 * 1000; // 10分钟
const int dailySleepDuration = 30 * 60 * 1000; // 15小时深度睡眠 (以微秒为单位)


const int GREENLED = 14;
const int YELLOWLED = 13;
const int PIRPIN = 12;

const char* ssid     = SECRET_SSID;
const char* password = SECRET_PASS;
const char* mqttuser = SECRET_MQTTUSER;
const char* mqttpass = SECRET_MQTTPASS;
char* topic_1 = "student/CASA0022/zczqrua/detector/no5";

const char* mqtt_server = "mqtt.cetools.org";
WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
float value = 0;

unsigned long lastTime = 0;
unsigned long pirHighTime = 0;
unsigned long totalTime = 0;

Timezone GB;

void setup() {
  Serial.begin(115200);
  delay(100);
  
  startWifi();
  
  // 同步时间
  configTime(0, 0, "pool.ntp.org", "time.nist.gov");
  delay(2000);  // 等待时间同步
  
  // 等待时间同步完成
  while (!time(nullptr)) {
    Serial.println("Waiting for NTP time sync...");
    delay(1000);
  }
  
  pinMode(PIRPIN, INPUT);
  pinMode(GREENLED, OUTPUT);
  pinMode(YELLOWLED, OUTPUT);

  client.setServer(mqtt_server, 1884);
  client.setCallback(callback);
  
  analogWrite(YELLOWLED, 20);
  
  lastTime = millis();
}

void loop() {
  // 获取当前时间
  time_t now = time(nullptr);
  struct tm* timeInfo = localtime(&now);
  
  int currentHour = timeInfo->tm_hour;

  Serial.print("Current hour: ");
  Serial.println(currentHour);

  if (currentHour >= startHour && currentHour < endHour) {
    analogWrite(YELLOWLED, 20); 
    unsigned long startWorkTime = millis();
    
    while (millis() - startWorkTime < workDuration) {
      unsigned long currentMillis = millis();
      int pirStatus = digitalRead(PIRPIN);

      totalTime += currentMillis - lastTime;

      if (pirStatus == HIGH) {
        analogWrite(GREENLED, 80);
        pirHighTime += currentMillis - lastTime; 
      } else {
        digitalWrite(GREENLED, LOW);
      }

      lastTime = currentMillis;
      delay(1000);
    }

    float percentage = (float)pirHighTime / totalTime * 100;
    snprintf(msg, 50, "%.0f", percentage);
    sendMQTT(topic_1, "", msg);
    Serial.println(percentage);

    totalTime = 0;
    pirHighTime = 0;
    delay(1000);
    enterLightSleep(sleepDuration); 
  } else {
    Serial.println("Non-working hours, entering light sleep until 9 AM...");
    enterLightSleep(dailySleepDuration); 
  }
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
      // Check the client state
      if (client.state() == MQTT_CONNECTED) {
        Serial.println("MQTT connection established successfully.");
      }
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void enterLightSleep(unsigned long sleepDurationMillis) {
  analogWrite(YELLOWLED, 0);
  digitalWrite(GREENLED, LOW);
  pinMode(14, INPUT);
  pinMode(13, INPUT);
  pinMode(12, INPUT);
  system_update_cpu_freq(SYS_CPU_80MHZ);
  WiFi.setSleepMode(WIFI_LIGHT_SLEEP);
  Serial.println("Entering light sleep mode...");
  WiFi.forceSleepBegin();
  delay(1);
  delay(sleepDurationMillis); 
  WiFi.forceSleepWake(); 
  delay(100);
  if (WiFi.status() != WL_CONNECTED) {
    startWifi();
  }
  Serial.println("Exited light sleep mode. WiFi reconnected.");
}



