
import datetime
from flask import Flask, render_template

app = Flask(__name__)

from credentials_bar import credentials

#########################################################################
# VARIABLES & CONSTANTS

MQTT_TOPIC_BATTERY = "mqtt_bat"
MQTT_TOPIC_ORDER = "mqtt_order"


##########################################
# FUNCTIONS




##########################################
# DATABASE STUFF

# import mysql.connector

# mydb = mysql.connector.connect(
#   host="localhost",
#   user=credentials["mysql_user"],
#   password=credentials['mysql_password']
# )

# mycursor = mydb.cursor()
# try:
#     mycursor.execute("CREATE DATABASE bar16") # Creates database named "bar16" if it doesn't already exist.
# except:
#     print("Database already exist. Continuing...")





# mydb = mysql.connector.connect(
#   host="localhost",
#   user=credentials["mysql_user"],
#   password=credentials['mysql_password']
#   database="bar16"
# )

# mycursor = mydb.cursor()

# mycursor.execute(f"CREATE TABLE completed_orders (drink_type VARCHAR(255), amount VARCHAR(255)), table VARCHAR(255))")


##########################################
# MQTT CLIENT


# https://pypi.org/project/paho-mqtt/
import paho.mqtt.client as mqtt

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
            byte_string = msg.payload
            decoded_string = byte_string.decode("utf-8")
            
            if len(decoded_string) > 50:
                # initializing string
                test_str = decoded_string
                
                # printing original string
                print("The original string is : " + str(test_str))
                
                # eval() used to convert 
                result = list(eval(test_str))
                order_data.append(result)
                print(f"{msg.topic} {result}")
            
            else:
                result = eval(decoded_string)
                order_data.append(result)
                print(f"{msg.topic} {result}")

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

@app.route('/statistics/')
def statistics():
    return render_template('statistics.html')

@app.route('/orders/')
def orders():
    # orders = ['This is the first order.',
    #             'This is the second order.',
    #             'This is the third order.',
    #             'This is the fourth order.'
    #             ]
    orders = order_data
    
    # print(len("{'name': 'Dark 'n Stormy', 'amount': 40}"))
    # print(len("{'name': '0', 'amount': 0},{'name': '0', 'amount': 0}"))
    # order_list = []
    # for obj in order_data:
    #     dict = eval(obj)
    #     order_list.append(dict)

    
    # orders = order_list
    
    print(order_data)
    #print(orders)
    # amount = 

    return render_template('orders.html', orders=orders)