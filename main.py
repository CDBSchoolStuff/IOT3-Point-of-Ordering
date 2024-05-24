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

DRINKS_CATEGORIES = ["Beer", "Cocktails"]


ARROW_STRING = "<---"

TICK_PERIOD_BUTTON = 100





#########################################################################
# VARIABLES

menu_location = 0
pb1 = Pin(PIN_BUTTON_1, Pin.IN, Pin.PULL_UP)             # No external pull-up or debounce
pb2 = Pin(PIN_BUTTON_2, Pin.IN, Pin.PULL_UP)             # No external pull-up or debounce

current_menu = DRINKS_CATEGORIES # Sets the default menu


# drinks_beer = [tuborg, carlsberg]
categories = [DRINKS_BEER, DRINKS_COCKTAIL]
#########################################################################
# FUNCTIONS

def menu_controller():
    lcd_controller.lcd.clear()
    lcd_controller.lcd.move_to(0, 0)
    lcd_controller.lcd.putstr("   -={ Bar 16 }=-")
    lcd_controller.lcd.move_to(0, 1)
    if menu_location != 0:
        lcd_controller.lcd.putstr(f"{menu_location - 1}: {current_menu[menu_location - 1]}") # Previous menu location
    lcd_controller.lcd.move_to(0, 2)
    lcd_controller.lcd.putstr(f"{menu_location}: {current_menu[menu_location]}") # Curent menu location
    lcd_controller.lcd.move_to(20 - len(ARROW_STRING), 2) # len(ARROW_STRING) ensures that the arrow will always be in the correct place.
    lcd_controller.lcd.putstr(ARROW_STRING)
    lcd_controller.lcd.move_to(0, 3)
    if menu_location < len(current_menu) - 1:
        lcd_controller.lcd.putstr(f"{menu_location + 1}: {current_menu[menu_location + 1]}") # Next menu location
    print(f"Menu Location: {menu_location}")


     

#########################################################################
# RUN ONCE

menu_controller()


#########################################################################
# PROGRAM

while True:
    try:
        pb1_val = pb1.value()              # Read onboard push button 1, active low
        pb2_val = pb2.value()
        
    
        if pb1_val == 0:
            if current_menu == DRINKS_CATEGORIES:
                current_menu = categories[menu_location]
                menu_location = 0 # Resets menu location to avoid outside index error
                print(f"1Set current menu to: {current_menu}")
                menu_controller()
                sleep(0.5)
        
        if pb2_val == 0:
            if current_menu != DRINKS_CATEGORIES:
                current_menu = DRINKS_CATEGORIES
                menu_location = 0 # Resets menu location to avoid outside index error
                print(f"3Set current menu to: {current_menu}")
                menu_controller()
                sleep(0.5)
        
        # Read the rotary encoder
        res = rotary_encoder.re_full_step()    
        
        if (res == 1):
            print("Right/CW")
            if menu_location < len(current_menu) - 1: # Minus one here cuz lists start from 0
                menu_location += 1
                menu_controller()
        elif (res == -1):
            print("Left/CCW")
            if menu_location > 0: # Ensures that the value can't go below 0
                menu_location -= 1
                menu_controller()
        
    
        
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        sys.exit()
        