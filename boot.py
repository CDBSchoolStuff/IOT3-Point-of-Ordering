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

def boot_sequence_thread():
    global STRING_1, STRING_2

    while starting:
        lcd_controller.lcd.clear()
        lcd_controller.lcd.putstr(STRING_1)
        lcd_controller.lcd.move_to(0, 2)
        lcd_controller.lcd.putstr(STRING_2)
        lcd_controller.lcd.move_to(len(STRING_2), 2)
        lcd_controller.lcd_dot_animation()
        
    lcd_controller.lcd.clear()
    global ready_to_continue
    ready_to_continue = True
    _thread.exit            
        
        


_thread.start_new_thread(boot_sequence_thread, ())

# Ukommenter, hvis der arbejdes med MQTT
# --------------------------------------

# import sys # Ukommenter, hvis der arbejdes med MQTT

# sys.path.reverse()

print("\n\n\nESP32 starter op")

# --------------------------------------

# This sleep is used to simulate stuff that takes time to load. Like connecting to wifi or mqtt.
sleep(0)

starting = False


# This while loop ensures that the code in main.py will not run before the boot sequence has stopped running.
while not ready_to_continue:
    if not has_run:
        has_run = True
        print("Holding program hostage until it starting sequence has ended.")

print(f"System took {ticks_ms() - system_start_ticks}ms to start. Continuing...")