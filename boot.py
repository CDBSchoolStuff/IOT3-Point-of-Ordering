print("\n\n\nESP32 starter op")

#########################################################################
# IMPORT
from machine import Pin, PWM
import _thread
import sys
from time import ticks_ms, sleep
import network
import esp

import lcd_controller
from credentials_table import credentials

esp.osdebug(None)
import gc
gc.collect()


#########################################################################
# VARIABLES & CONSTANTS

starting = True
ready_to_continue = False
has_run = False
system_start_ticks = ticks_ms()

STRING_2 = "System starting"


#########################################################################
# STARTUP SCREEN

# Async thread that runs a message on the LCD while the system is starting.
def boot_sequence_thread():
    global STRING_2

    while starting:
        lcd_controller.lcd_boot_message(STRING_2)
        
    #lcd_controller.lcd.clear()
    global ready_to_continue
    ready_to_continue = True
    _thread.exit            
        
_thread.start_new_thread(boot_sequence_thread, ())


#########################################################################
# WIFI CONNECTIVITY

ssid = credentials['ssid']
password = credentials['password']

station = network.WLAN(network.STA_IF)

try:
    station.active(True)
    station.connect(ssid, password)

    while station.isconnected() == False:
        pass

    print('Connection successful')
    print(station.ifconfig())
    
except: # Except tilføjet for at lade koden køre uden forbindelse til netværk.
    print("Network connection failed.")


#########################################################################

starting = False # Stops the boot sequence thread.

# This while loop ensures that the code in main.py will not run before the boot sequence has stopped running.
while not ready_to_continue:
    if not has_run:
        has_run = True
        print("Holding program hostage until the starting sequence has ended.")
    sleep(1)
print(f"System took {ticks_ms() - system_start_ticks}ms to start. Continuing...")