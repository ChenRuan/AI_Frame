import paho.mqtt.client as mqtt
import csv
import time
import threading
from collections import defaultdict
import os

MQTT_BROKER = "mqtt.cetools.org"
MQTT_PORT = 1883
MQTT_TOPICS = ["student/CASA0022/zczqrua/weather/lux", "student/CASA0022/zczqrua/weather/windSpeed", "student/CASA0022/zczqrua/weather/rain","student/CASA0022/zczqrua/weather/temp","student/CASA0022/zczqrua/weather/hum","student/CASA0022/zczqrua/weather/hum","student/CASA0022/zczqrua/detector/no1","student/CASA0022/zczqrua/detector/no2","student/CASA0022/zczqrua/detector/no3","student/CASA0022/zczqrua/detector/no4","student/CASA0022/zczqrua/detector/no5","student/CASA0022/zczqrua/airquality/value","student/CASA0022/zczqrua/airquality/t3mp","student/CASA0022/zczqrua/airquality/6um"]

data_storage = defaultdict(list)
lock = threading.Lock()
csv_file_path = 'mqtt_data.csv'

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    for topic in MQTT_TOPICS:
        client.subscribe(topic)
   
def on_message(client, userdata, msg):
    with lock:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        data_storage[msg.topic].append((timestamp, msg.payload.decode()))

def write_to_csv():
    while True:
        time.sleep(300)  
        with lock:
            if any(data_storage.values()):
                file_exists = os.path.isfile(csv_file_path)
                with open(csv_file_path, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    if not file_exists:
                        writer.writerow(["Timestamp", "Topic", "Message"])
                    for topic, messages in data_storage.items():
                        for message in messages:
                            writer.writerow([message[0], topic, message[1]])
                print("Data appended to mqtt_data.csv")
                data_storage.clear()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)

csv_writer_thread = threading.Thread(target=write_to_csv)
csv_writer_thread.daemon = True
csv_writer_thread.start()

client.loop_forever()
