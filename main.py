print("Running code in main.py")


########################################
# IMPORT
from adc_sub import ADC_substitute
import rotary_encoder

from machine import ADC, Pin
from time import ticks_ms, sleep
import sys
import _thread

from battery_status import Battery_Status
import lcd_controller
#import mqtt_client


#########################################################################
# CONFIGURATION

PIN_BUTTON_1 = 12
PIN_BUTTON_2 = 13
PIN_BUTTON_3 = 14
PIN_BUTTON_3 = 4 # Rotery Encoder button

PIN_BATTERY = 35
PIN_BUZZER = 26
PIN_NEOPIXEL = 15

MQTT_TOPIC_BATTERY = "mqtt_bat"
MQTT_TOPIC_ORDER = "mqtt_order"
MQTT_TOPIC_CONFIRM = "mqtt_confirm"

MQTT_CHECK_CONNECTION_DELAY = 60
ACK_TIMEOUT = 50000

MENU_INDEX_BEER = 0
MENU_INDEX_COCKTAIL = 1
MENU_INDEX_SELECTED = 2

DEVICE_ID = 1

#########################################################################
# CONSTANTS


DRINKS_BEER = ["Tuborg", "Carlsberg", "Slots", "Guld Damer", "Royal", "Albani", "Skovlyst"]
DRINKS_COCKTAIL = ["Gin Hass", "Dark N Stormy", "Negroni", "Margarita", "Daiquiri"]




#########################################################################
# VARIABLES

menu_location = 0

pb1 = Pin(PIN_BUTTON_1, Pin.IN, Pin.PULL_UP)             # No external pull-up or debounce
pb2 = Pin(PIN_BUTTON_2, Pin.IN, Pin.PULL_UP)             # No external pull-up or debounce
pb3 = Pin(PIN_BUTTON_3, Pin.IN, Pin.PULL_UP)             # No external pull-up or debounce

current_menu = []  # List that holds a copy of the currently displayed menu.

counter = 0


prev_bat_pct = 0

selecting = False
waiting_for_ack = False

#########################################################################
# OBJECTS

battery_subadc = ADC_substitute(PIN_BATTERY)  # The battery object
Battery = Battery_Status(battery_subadc)


#########################################################################
# FUNCTIONS & CLASSES


class Menu():
    def __init__(self, name, list):
        self.name = name
        self.list = list


class Drink():
    amount = 0
    
    def __init__(self, name):
        self.name = name
        
    def add_amount(self, val):
        self.amount += val
        
    def remove_amount(self, val):
        self.amount += val

# Takes a list and a boolean as arguments. The list is for constructing the menu. The boolean is for indicating that the menu location should be reset when printing.
def menu_controller(menu_list, reset_location):
    
    global current_menu, menu_location
    current_menu = menu_list
    
    entries = []
    for i in range(len(menu_list)):
        entries.append(menu_list[i].name)
    
    if reset_location == True: # Resets menu location to prevent crash if the menu location is outside of the current menu list
        menu_location = 0

    lcd_controller.lcd_print_menu(menu_location, entries)

        

#########################################################################
# RUN ONCE

# ----------------------------------------
# Beer menu

menu_beers = []

for i in range(len(DRINKS_BEER)):
    menu_beers.append(Drink(DRINKS_BEER[i]))


# ----------------------------------------
# Cocktail menu

menu_cocktails = []

# Iterates through the static DRINKS_COCKTAIL list to create objects objects based on the Drinks class
for i in range(len(DRINKS_COCKTAIL)):
    menu_cocktails.append(Drink(DRINKS_COCKTAIL[i]))


# ----------------------------------------
# Categories menu

menu_categories = []

menu_categories.append(Menu("Beer", menu_beers))
menu_categories.append(Menu("Cocktail", menu_cocktails))
menu_categories.append(Menu("Confirm order", []))

# ----------------------------------------

# print(menu_beers[4].name)
# print(menu_categories[0].list)


menu_controller(menu_categories, True) # Sets the default menu

# Responsible for overriding the current menu with a selection screen. Takes an integer as argument to display for the selection counter.
def selecting_menu(count):
    lcd_controller.lcd.clear()
    lcd_controller.lcd_print_branding()
    lcd_controller.lcd.move_to(0, 2)

    name = current_menu[menu_location].name
    lcd_controller.lcd.putstr(f"{name}")
    
    lcd_controller.lcd.move_to(lcd_controller.align_text_right(f"{count}"), 2)
    lcd_controller.lcd.putstr(f"{count}")

# Resets the amount variable stored in the drink objects.
# Takes list of drink objects as argument.
def reset_amount(obj_list):
    for obj in obj_list:
        obj.amount = 0
    return obj_list


# #########################################################################
# # PROGRAM


battery_status_start = ticks_ms()
battery_status_period_ms = 10000 # 1000ms = 1s

mqtt_connect_start = ticks_ms()
mqtt_connect_period_ms = 20000


#------------------------------------------------------
# MQTT Stuff
import ubinascii
import machine, time
from umqttsimple import MQTTClient
from credentials_table import credentials

mqtt_server = credentials['mqtt_server']
client_id = ubinascii.hexlify(machine.unique_id())

last_message = 0
message_interval = 5
counter = 0

def sub_cb(topic, msg):
  print((topic, msg))
  if topic == b'mqtt_confirm' and msg == b'ack':
    global waiting_for_ack
    waiting_for_ack = False
    print('ESP received ack message')

def connect_and_subscribe(topic_sub):
  global client_id, mqtt_server
  
  mqtt_client = MQTTClient(client_id, mqtt_server)
  mqtt_client.set_callback(sub_cb)
  mqtt_client.connect()
  mqtt_client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return mqtt_client


def send_message(msg, topic):
    try:        
        # client.connect()
        mqtt_client.publish(topic, msg)
        print(f"[MQTT] Topic: {topic} | Message: {msg}")
    except OSError as error:
        print(error)
        print(f"[MQTT] Message not sent. Topic: {topic} | Message: {msg}")


try:
    mqtt_client = connect_and_subscribe(MQTT_TOPIC_CONFIRM)
except:
    print("[MQTT] Connection failed.")


# Responsible for querying the MQTT-broker on set intervals, ensuring that the device is connected.
def mqtt_thread():
    #mqtt_sender.client = mqtt_sender.connect_to_broker() # Connect to MQTT
    while True:
        try:
            global mqtt_client
            
            mqtt_client.check_msg()
            
            # Check connection
            try:
                print("[MQTT] Checking connection.")
                mqtt_client.connect()
                print("[MQTT] Connection OK.")
            except:
                print("[MQTT] Connection failed. Reconnecting...")
                mqtt_client = connect_and_subscribe(MQTT_TOPIC_CONFIRM)
                # mqtt_client.connect_to_broker() # Connect to MQTT
                    
        except KeyboardInterrupt:
            print('Ctrl-C pressed...exiting')
            mqtt_client.disconnect()
            sys.exit()
        
        sleep(MQTT_CHECK_CONNECTION_DELAY)

#_thread.start_new_thread(mqtt_thread, ())              # Start MQTT thread.

#------------------------------------------------------

# Responsible for overriding the current menu screen with a confirmation screen and sending the order over MQTT.
def confirmation_menu():
    print(f"Opened confirmation screen")
    lcd_controller.lcd.clear()
    lcd_controller.lcd_print_branding()
    lcd_controller.lcd.move_to(0, 2)
    lcd_controller.lcd.putstr(f"Press again to send order.")

    waiting_for_confirm = True
    sleep(0.2)

    while waiting_for_confirm:
        if pb1.value() == 0:
            print(f"Sending order: {menu_categories[MENU_INDEX_SELECTED].list}")
            
            data = []
            for obj in menu_categories[MENU_INDEX_SELECTED].list:
                data.append({"name": obj.name, "amount": obj.amount}) # Puts the data of the drink entry into a dict
            
            data_string = f"{data}"
            
            send_message(data_string, MQTT_TOPIC_ORDER)
            wait_for_ack()

            reset_amount(menu_beers) # Reset the amount stored in the drink objects.
            reset_amount(menu_cocktails)
            update_selected_drinks()
            menu_controller(menu_categories, True) # Ensures that the selection screen closes

            waiting_for_confirm = False
            sleep(0.2)
            break
        elif pb2.value() == 0:
            print(f"Confirmation aborted")

            menu_controller(current_menu, False)
            waiting_for_confirm = False
            sleep(0.2)
            break

def wait_for_ack():
    global waiting_for_ack
    waiting_for_ack = True

    start_ticks = ticks_ms()
    print(f"Waiting for ack...")
    
    while waiting_for_ack:
        try:
        
            lcd_controller.print_simple_message("Your drink is being prepared")
            lcd_controller.lcd_dot_animation()
            
            if mqtt_client.check_msg():
                lcd_controller.print_simple_message("Your order is ready!")
                break
                
            if ticks_ms() > (start_ticks + ACK_TIMEOUT):
                lcd_controller.print_simple_message("Error! Too much time passed.")
                sleep(10)
                waiting_for_ack = False
                break
            sleep(1)
        except OSError as e:
            lcd_controller.print_simple_message("Error!")
            sleep(5)
            break
    
    sleep(10)
    waiting_for_ack = False


# Updates the list of selected drinks to include the drink objects that have an amount above 0.
def update_selected_drinks():
    print("Updating selected drinks list.")
    drinks = menu_beers + menu_cocktails
    drinks_with_amount = []

    for obj in drinks:
        if obj.amount > 0:
            drinks_with_amount.append(obj)
            print(f"Added {obj.name} to selected list")
    
    menu_categories[MENU_INDEX_SELECTED].list = drinks_with_amount
    print(f"Selected drinks: {menu_categories[MENU_INDEX_SELECTED].list}")


#------------------------------------------------------
# Main program

while True:
    try:
        mqtt_client.check_msg()
        
        # ----------------------------------------
        # Battery Status
        try:
            if ticks_ms() - battery_status_start > battery_status_period_ms: # Non breaking delay for the battery status.
                battery_status_start = ticks_ms()

                battery_pct = Battery.get_battery_pct()
                print(f"Battery Pct: {battery_pct}%")
                # Send data if there is a change (this principle saves power)
                if battery_pct != prev_bat_pct:
                    
                    send_message(f"{battery_pct}", MQTT_TOPIC_BATTERY)
                    # mqtt_client.send_message(battery_pct, MQTT_TOPIC_BATTERY)
                    # Update the previous values for use next time
                    prev_bat_pct = battery_pct
        except:
            print("[Error] An error occurred in battery status segment.")

        # ----------------------------------------
        # Push button stuff
        
        pb1_val = pb1.value()              # Read onboard push button 1, active low
        pb2_val = pb2.value()
        # pb3_val = pb3.value()
        
        if pb1_val == 0:
            if current_menu == menu_categories and not selecting and current_menu != menu_categories[MENU_INDEX_SELECTED].list:
                print(f"Set menu to: {menu_categories[menu_location].name}")
                print(f"Menu entries: {menu_categories[menu_location].list}")
                menu_controller(menu_categories[menu_location].list, True)
                sleep(0.2)
                
            
            # This handles the actions of the select button when inside either the Beer or Cocktail categories.
            elif current_menu != menu_categories and not selecting and current_menu != menu_categories[MENU_INDEX_SELECTED].list:
                print(f"Selected: {current_menu[menu_location].name}")
                
                # test_amount = 1
                # current_menu[menu_location].add_amount(test_amount) # Runs the add_amount method for the selected drink to add an amount to the order.
                # print(f"Added {test_amount} to amount for: {current_menu[menu_location].name}")
                
                #print(f"{current_menu[menu_location].name} amount = {current_menu[menu_location].amount}")
                
                selecting_menu(0)
                selecting = True  
                sleep(0.2)
            
            # Adds the counter variable to the amount of the current item & updates the list of selected drinks
            elif selecting:
                current_menu[menu_location].add_amount(counter)
                print(f"{current_menu[menu_location].name} amount = {current_menu[menu_location].amount}")
                selecting = False
                update_selected_drinks()
                # selected.append(current_menu[menu_location])
                menu_controller(current_menu, False) # Ensures that the selection screen closes
                counter = 0 # Resets counter variable
                sleep(0.2)
            
            # Adds clickable event to selected drinks menu.
            elif current_menu == menu_categories[MENU_INDEX_SELECTED].list and menu_categories[MENU_INDEX_SELECTED].list:
                confirmation_menu()
                sleep(0.2)

        
        # Allows for returning to the categories menu if not already in that menu.
        if pb2_val == 0:
            if current_menu != menu_categories:
                menu_location = 0 # Resets menu location to avoid outside index error
                
                if selecting:
                    selecting = False
                    
                print(f"Set current menu to: {menu_categories[menu_location].name}")
                menu_controller(menu_categories, False) # Returns to the category menu
                sleep(0.5)
        # ----------------------------------------
        # Rotary Encoder stuff
        try:
            res = rotary_encoder.re_full_step()    # Reads the rotary encoder
            
            
            # Responsible for selecting amount using Rotary Encoder
            if selecting == True:
                if (res == 1):
                    print("Right/CW")
                    counter += 1
                    selecting_menu(counter) # Prints to the lcd and carries with is the current_menu
                elif (res == -1):
                    print("Left/CCW")
                    if counter > 0: # Ensures that the value can't go below 0
                        counter -= 1
                        selecting_menu(counter) # Prints to the lcd
            
            
            # Responsible for navigating menus using Rotary Encoder
            else:
                if (res == 1):
                    print("Right/CW")
                    if menu_location < len(current_menu) - 1: # Minus one here cuz lists start from 0
                        menu_location += 1
                        menu_controller(current_menu, False) # Prints to the lcd and carries with is the current_menu
                elif (res == -1):
                    print("Left/CCW")
                    if menu_location > 0: # Ensures that the value can't go below 0
                        menu_location -= 1
                        menu_controller(current_menu, False) # Prints to the lcd and carries with is the current_menu
        except:
            print("[Error] An error occurred in rotary encoder segment.")
        
        # ----------------------------------------
        
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        sys.exit()
        