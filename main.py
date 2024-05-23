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


beers = ["Tuborg", "Carlsberg", "Slots", "Guld Damer", "Royal", "Albani", "Skovlyst"]
cocktails = ["Gin Hass", "Dark 'N Stormy", "Negroni", "Margarita", "Daiquiri"]


#########################################################################
# PROGRAM

left = False
right = False
counter = 0

while True:
    try:
        # Read the rotary encoder
        res = rotary_encoder.re_full_step()    
        
        if (res == 1):
            print("Right/CW")
        elif (res == -1):
            print("Left/CCW")
        
        
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        sys.exit()