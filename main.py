########################################
# IMPORT
from adc_sub import ADC_substitute

from machine import ADC, Pin
from time import ticks_ms, sleep
import sys



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
# PROGRAM


while True:
    try:
        print("Running")
        sleep(1)
        
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        sys.exit()