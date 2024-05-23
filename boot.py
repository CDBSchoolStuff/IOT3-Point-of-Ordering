print("\n\n\nESP32 starter op")

from machine import Pin, PWM
import _thread
import lcd_controller
import sys

from time import ticks_ms, sleep


#########################################################################
# VARIABLES

starting = True
ready_to_continue = False
has_run = False
system_start_ticks = ticks_ms()


#########################################################################
# CONSTANTS

STRING_1 = "   -={ Bar 16 }=-"
STRING_2 = "System starting"


#########################################################################
# BOOT PROGRAM


# Async thread that runs a message on the LCD while the system is starting.
def boot_sequence_thread():
    global STRING_1, STRING_2

    while starting:
        lcd_controller.lcd_boot_message(STRING_1, STRING_2)
        
    #lcd_controller.lcd.clear()
    global ready_to_continue
    ready_to_continue = True
    _thread.exit            
        
        


_thread.start_new_thread(boot_sequence_thread, ())

# Ukommenter, hvis der arbejdes med MQTT
# --------------------------------------

# import sys # Ukommenter, hvis der arbejdes med MQTT

# sys.path.reverse()


# --------------------------------------

# This sleep is used to simulate stuff that takes time to load. Like connecting to wifi or mqtt.
sleep(0)

starting = False


# This while loop ensures that the code in main.py will not run before the boot sequence has stopped running.
while not ready_to_continue:
    if not has_run:
        has_run = True
        print("Holding program hostage until the starting sequence has ended.")
    sleep(1)
print(f"System took {ticks_ms() - system_start_ticks}ms to start. Continuing...")