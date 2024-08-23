#include <ESP8266WiFi.h>
#include <ezTime.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <DHT.h>

// WiFi and MQTT credentials
#include "arduino_secrets.h" 

const char* ssid     = SECRET_SSID;
const char* password = SECRET_PASS;
const char* mqttuser = SECRET_MQTTUSER;
const char* mqttpass = SECRET_MQTTPASS;
char* topic_1 = "student/CASA0022/zczqrua/airquality/";
const char* mqtt_server = "mqtt.cetools.org";

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long currentMillis = 0;
unsigned long lastSendTime = 0;
const unsigned long sendInterval = 10 * 60 * 1000; // 10 minutes

// MQ7 Sensor
#define MQ7Pin 5
int mq7Sum = 0;
int mq7Readings = 0;
char mq7Str[10];

// DHT22 Sensor
#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);
float tempSum = 0;
float humSum = 0;
int dhtReadings = 0;
char tempStr[10];
char humStr[10];

void setup() {
  Serial.begin(115200);
  delay(100);
  startWifi();
  dht.begin();

  // Start MQTT server
  client.setServer(mqtt_server, 1884);
  client.setCallback(callback);
}

void loop() {
  currentMillis = millis();

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Read MQ7 sensor
  int mq7Value = analogRead(MQ7Pin);
  Serial.print("MQ7 value: ");
  Serial.println(mq7Value);
  mq7Sum += mq7Value;
  mq7Readings++;

  // Read DHT22 sensor
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  Serial.print("temperature: ");
  Serial.println(temperature);
  Serial.print("humidity: ");
  Serial.println(humidity);
  tempSum += temperature;
  humSum += humidity;
  dhtReadings++;

  // Check if it's time to send the average values
  if (currentMillis - lastSendTime >= sendInterval) {
    // Calculate and send MQ7 average value
    int mq7Average = mq7Sum / mq7Readings;
    dtostrf(mq7Average, 0, 0, mq7Str);
    sendMQTT(topic_1, "value", mq7Str);
    Serial.print("MQ7 Average: ");
    Serial.println(mq7Average);

    // Calculate and send DHT22 average values
    float tempAverage = tempSum / dhtReadings;
    float humAverage = humSum / dhtReadings;
    dtostrf(tempAverage, 0, 1, tempStr);
    dtostrf(humAverage, 0, 1, humStr);
    sendMQTT(topic_1, "t3mp", tempStr);
    sendMQTT(topic_1, "6um", humStr);
    Serial.print("Temperature Average: ");
    Serial.println(tempAverage);
    Serial.print("Humidity Average: ");
    Serial.println(humAverage);

    // Reset sums and counters
    mq7Sum = 0;
    mq7Readings = 0;
    tempSum = 0;
    humSum = 0;
    dhtReadings = 0;
    lastSendTime = currentMillis;
  }
  delay(100);
}

void startWifi() {
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void sendMQTT(char* topic, char* name, char* msg) {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  char fullTopic[100];
  snprintf(fullTopic, sizeof(fullTopic), "%s%s", topic, name);
  client.publish(fullTopic, msg);
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
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP32Client-";
    clientId += String(random(0xffff), HEX);

    if (client.connect(clientId.c_str(), mqttuser, mqttpass)) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}
