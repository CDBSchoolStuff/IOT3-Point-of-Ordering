print("Running code in main.py")


########################################
# IMPORT
from adc_sub import ADC_substitute
import rotary_encoder

from machine import ADC, Pin
from time import ticks_ms, sleep
import sys


import drink
import lcd_controller


#########################################################################
# CONFIGURATION

PIN_BATTERY = 32
PIN_BUTTON_1 = 4
PIN_BUTTON_2 = 12

MQTT_TOPIC_BATTERY = "mqtt_bat"
MQTT_TOPIC_LITER = "mqtt_order"


#########################################################################
# CONSTANTS


DRINKS_BEER = ["Tuborg", "Carlsberg", "Slots", "Guld Damer", "Royal", "Albani", "Skovlyst"]
DRINKS_COCKTAIL = ["Gin Hass", "Dark 'N Stormy", "Negroni", "Margarita", "Daiquiri"]




#########################################################################
# VARIABLES

menu_location = 0
pb1 = Pin(PIN_BUTTON_1, Pin.IN, Pin.PULL_UP)             # No external pull-up or debounce
pb2 = Pin(PIN_BUTTON_2, Pin.IN, Pin.PULL_UP)             # No external pull-up or debounce

current_menu = []  # List that holds a copy of the currently displayed menu.


#########################################################################
# FUNCTIONS & CLASSES


class menu():
    def __init__(self, name, list):
        self.name = name
        self.list = list


class drink():
    amount = 0
    
    def __init__(self, name):
        self.name = name
        
    def add_amount(self, val):
        self.amount += val
        
    def remove_amount(self, val):
        self.amount += val


def menu_controller(menu_list):
    
    global current_menu 
    current_menu = menu_list
    
    entries = []
    for i in range(len(menu_list)):
        entries.append(menu_list[i].name)
    
    lcd_controller.lcd_print_menu(menu_location, entries)



#########################################################################
# RUN ONCE


# ----------------------------------------
# Beer menu

menu_beers = []

for i in range(len(DRINKS_BEER)):
    menu_beers.append(drink(DRINKS_BEER[i]))


# ----------------------------------------
# Cocktail menu

menu_cocktails = []

for i in range(len(DRINKS_COCKTAIL)):
    menu_cocktails.append(drink(DRINKS_COCKTAIL[i]))


# ----------------------------------------
# Categories menu

menu_categories = []

menu_categories.append(menu("Beer", menu_beers))
menu_categories.append(menu("Cocktail", menu_cocktails))


# ----------------------------------------

print(menu_beers[4].name)

print(menu_categories[0].list)


# menu_controller(menu_categories) # Sets the default menu
menu_controller(menu_categories) # Sets the default menu



# #########################################################################
# # PROGRAM

while True:
    try:
        pb1_val = pb1.value()              # Read onboard push button 1, active low
        pb2_val = pb2.value()
        
        if pb1_val == 0:
            if current_menu == menu_categories:
                print(f"Set menu to: {menu_categories[menu_location].name}")
                
                menu_controller(menu_categories[menu_location].list)
            sleep(0.5)
        
        # Allows for returning to the categories menu if not already in that menu.
        if pb2_val == 0:
            if current_menu != menu_categories:
                menu_location = 0 # Resets menu location to avoid outside index error
                print(f"3Set current menu to: {menu_categories[menu_location].name}")
                menu_controller(menu_categories) # Returns to the category menu
                sleep(0.5)
        
        # ----------------------------------------
        # Rotary Encoder stuff
        
        res = rotary_encoder.re_full_step()    # Reads the rotary encoder
        
        if (res == 1):
            print("Right/CW")
            if menu_location < len(current_menu) - 1: # Minus one here cuz lists start from 0
                menu_location += 1
                menu_controller(current_menu) # Prints to the lcd and carries with is the current_menu
        elif (res == -1):
            print("Left/CCW")
            if menu_location > 0: # Ensures that the value can't go below 0
                menu_location -= 1
                menu_controller(current_menu) # Prints to the lcd and carries with is the current_menu
        
        # ----------------------------------------
        
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        sys.exit()
        