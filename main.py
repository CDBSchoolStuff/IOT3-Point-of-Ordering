print("Running code in main.py")


########################################
# IMPORT
from adc_sub import ADC_substitute

from machine import ADC, Pin
from time import ticks_ms, sleep
import sys


import rotary_encoder
import lcd_controller


#########################################################################
# CONFIGURATION

PIN_BAT = 32
MQTT_TOPIC_BATTERY = "mqtt_bat"
MQTT_TOPIC_LITER = "mqtt_order"


#########################################################################
# OBJECTS




#########################################################################
# VARIABLES


#########################################################################
# FUNCTIONS


DRINKS_BEER = ["Tuborg", "Carlsberg", "Slots", "Guld Damer", "Royal", "Albani", "Skovlyst"]
DRINKS_COCKTAIL = ["Gin Hass", "Dark 'N Stormy", "Negroni", "Margarita", "Daiquiri"]


#########################################################################
# PROGRAM

left = False
right = False
counter = 0


menu_location = 0


def menu_controller():
    lcd_controller.lcd.clear()
    lcd_controller.lcd.move_to(0, 0)
    if menu_location != 0:
        lcd_controller.lcd.putstr(f"{menu_location - 1}: {DRINKS_BEER[menu_location - 1]}") # Previous menu location
    lcd_controller.lcd.move_to(0, 1)
    lcd_controller.lcd.putstr(f"{menu_location}: {DRINKS_BEER[menu_location]}") # Curent menu location
    lcd_controller.lcd.move_to(0, 2)
    if menu_location < len(DRINKS_BEER) - 1:
        lcd_controller.lcd.putstr(f"{menu_location + 1}: {DRINKS_BEER[menu_location + 1]}") # Next menu location
    print(f"Menu Location: {menu_location}")

while True:
    try:
        # Read the rotary encoder
        res = rotary_encoder.re_full_step()    
        
        if (res == 1):
            print("Right/CW")
            if menu_location < len(DRINKS_BEER) - 1: # Minus one here cuz lists start from 0
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
        