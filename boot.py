from machine import Pin, PWM
import _thread
import lcd_controller

from time import sleep



#########################################################################
# VARIABLES

starting = True
ready_to_continue = False
has_run = False

#########################################################################
# BOOT PROGRAM

def boot_sequence_thread():
    try:    
        string1 = "   -={ Bar 16 }=-"
        string2 = "System starting"

        while starting:
            lcd_controller.lcd.clear()
            lcd_controller.lcd.putstr(string1)
            lcd_controller.lcd.move_to(0, 2)
            lcd_controller.lcd.putstr(string2)
            lcd_controller.lcd.move_to(len(string2), 2)
            lcd_controller.lcd_dot_animation()
            
        lcd_controller.lcd.clear()
        global ready_to_continue
        ready_to_continue = True
        _thread.exit
        
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting thread')
        _thread.exit


_thread.start_new_thread(boot_sequence_thread, ())

# Ukommenter, hvis der arbejdes med MQTT
# --------------------------------------

# import sys # Ukommenter, hvis der arbejdes med MQTT

# sys.path.reverse()

print("\n\n\nESP32 starter op")

# --------------------------------------

sleep(5)
starting = False


# This while loop ensures that the code in main.py will not run before the boot sequence has stopped running.
while not ready_to_continue:
    if not has_run:
        has_run = True
        print("Holding program hostage until it starting sequence has ended.")
    
print("Continuing...")