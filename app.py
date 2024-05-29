
import paho.mqtt.client as mqtt


import datetime
from flask import Flask, render_template

app = Flask(__name__)


#########################################################################
# CONFIGURATION

MQTT_TOPIC_BATTERY = "mqtt_bat"
MQTT_TOPIC_ORDER = "mqtt_order"



##########################################
# MQTT CLIENT


# https://pypi.org/project/paho-mqtt/
import paho.mqtt.client as mqtt

from credentials import credentials

mqtt_server = credentials['mqtt_server']

import paho.mqtt.client as mqtt

order_data = []

try:
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(MQTT_TOPIC_ORDER)
        client.subscribe(MQTT_TOPIC_BATTERY)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        
        # Appends the inbound order to the orders list if message is received on order topic.
        if msg.topic == MQTT_TOPIC_ORDER:
            order_data.append(msg.payload)
            print(f"{msg.topic} {msg.payload}")

    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    mqttc.connect(mqtt_server)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    # mqttc.loop_forever()
    mqttc.loop_start()

except:
    print("Failed to connect to MQTT broker. Continuing...")

##########################################




@app.route('/')
def hello():
    return render_template('index.html', utc_dt=datetime.datetime.utcnow())

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/orders/')
def orders():
    # orders = ['This is the first order.',
    #             'This is the second order.',
    #             'This is the third order.',
    #             'This is the fourth order.'
    #             ]
    orders = order_data

    return render_template('orders.html', orders=orders)