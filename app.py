
import datetime
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

from credentials_bar import credentials

#########################################################################
# VARIABLES & CONSTANTS

MQTT_TOPIC_BATTERY = "mqtt_bat"
MQTT_TOPIC_ORDER = "mqtt_order"

MQTT_TOPIC_CONFIRM = "mqtt_confirm"

battery_status = None

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
            
            mqttc.publish(MQTT_TOPIC_CONFIRM, "ack")

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
        elif msg.topic == MQTT_TOPIC_BATTERY:
            global battery_status
            
            byte_string = msg.payload
            decoded_string = byte_string.decode("utf-8")
            
            battery_status = f"{decoded_string}% {datetime.datetime.utcnow()}"
            print(f"{msg.topic} {battery_status}")
            
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



def complete_order():
    if order_data:
        order_data.pop(0)
        print("Order completed")

def delete_order():
    if order_data:
        order_data.pop(0)
        print("Order deleted")



# Executes function and redirects to page.
@app.route('/complete', methods=['POST'])
def complete():
    complete_order()
    return redirect(url_for('orders'))

@app.route('/delete', methods=['POST'])
def delete():
    delete_order()
    return redirect(url_for('orders'))


# Redirects root page to orders.
@app.route('/')
def hello():
    return redirect(url_for('orders'))



@app.route('/status/')
def status():
    return render_template('status.html', battery_status=battery_status)



@app.route('/orders/')
def orders():
    orders = order_data
    
    print(order_data)

    return render_template('orders.html', orders=orders)


if __name__ == '__main__':
    app.run(debug=True)