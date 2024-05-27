# Complete project details at https://randomnerdtutorials.com/micropython-mqtt-esp32-esp8266/

# https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/
# https://pimylifeup.com/raspberry-pi-mosquitto-mqtt-server/

# RaspberryPi Mosquitto Command:
# mosquitto_sub -d -h localhost -t mqtt_data

import ubinascii
import machine, time
from umqttsimple import MQTTClient
from credentials import credentials

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

# def sub_cb(topic, msg):
#     print((topic, msg))
#     if topic == b'notification' and msg == b'received':
#         print('ESP received hello message')

# def connect_and_subscribe():
#     global mqtt_connected
#     try:
#         print("Connecting to %s MQTT broker..." % (mqtt_server))
#         #global client_id, mqtt_server, topic_sub
#         client = MQTTClient(client_id, mqtt_server)
#         client.set_callback(sub_cb)
#         client.connect()
#         client.subscribe(topic_sub)
#         print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
#         mqtt_connected = True
#         return client
#     except:
#         print("Failed to connect to MQTT broker. Continuing...")
#         mqtt_connected = False

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