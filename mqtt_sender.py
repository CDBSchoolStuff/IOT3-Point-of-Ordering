# Complete project details at https://randomnerdtutorials.com/micropython-mqtt-esp32-esp8266/

# https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/
# https://pimylifeup.com/raspberry-pi-mosquitto-mqtt-server/

# RaspberryPi Mosquitto Command:
# mosquitto_sub -d -h localhost -t mqtt_data

import ubinascii
import machine, time
from umqttsimple import MQTTClient
from credentials_table import credentials


# This library borrows code from a prior project: 
# https://github.com/CDBSchoolStuff/IOT2-Cleanflow/blob/main/mqtt_sender.py


mqtt_server = credentials['mqtt_server']
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'mqtt_data'
topic_pub = b'mqtt_data'

last_message = 0
message_interval = 5
counter = 0

client = MQTTClient(client_id, mqtt_server)

mqtt_connected = False

#########################################################################
# FUNCTIONS

def restart_and_reconnect():
    print('[MQTT] Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

from time import ticks_ms

def connect_to_broker():
    try:
        print("[MQTT] Connecting to %s MQTT broker..." % (mqtt_server))
        client = MQTTClient(client_id, mqtt_server)
        client.connect()
        print('[MQTT] Successfully connected to %s MQTT broker.' % (mqtt_server))
        return client
    except OSError as e:
        print("[MQTT] Failed to connect to %s MQTT broker." % (mqtt_server))
        client = MQTTClient(client_id, mqtt_server)
        return client

# def run_once():
#     try:
#         client = connect_and_subscribe()
#     except OSError as e:
#         restart_and_reconnect()
      
      
def send_message(msg, topic):
    try:
        #client = MQTTClient(client_id, mqtt_server)
        #client.connect()
        client.publish(topic, msg)
        print(f"[MQTT] Topic: {topic} | Message: {msg}")
    except OSError as e:
        # restart_and_reconnect()
        print(f"[MQTT] Message not sent. Topic: {topic} | Message: {msg}")