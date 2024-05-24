print("Running code in main.py")


########################################
# IMPORT
from adc_sub import ADC_substitute
import rotary_encoder

from machine import ADC, Pin
from time import ticks_ms, sleep
import sys


import lcd_controller


#########################################################################
# CONFIGURATION

PIN_BATTERY = 32
PIN_BUTTON_1 = 4
PIN_BUTTON_2 = 12
PIN_BUTTON_3 = 14

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
pb3 = Pin(PIN_BUTTON_3, Pin.IN, Pin.PULL_UP)             # No external pull-up or debounce

current_menu = []  # List that holds a copy of the currently displayed menu.

counter = 0

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


# ----------------------------------------

print(menu_beers[4].name)

print(menu_categories[0].list)


menu_controller(menu_categories) # Sets the default menu

# current_menu = menu_beers  # Used for testing, remove after


#while True:
    
selecting = False

def selecting_menu(count):
    lcd_controller.lcd.clear()
    lcd_controller.lcd_print_branding()
    lcd_controller.lcd.move_to(0, 2)

    name = current_menu[menu_location].name
    lcd_controller.lcd.putstr(f"{name}")
    
    lcd_controller.lcd.move_to(lcd_controller.align_text_right(f"{count}"), 2)
    lcd_controller.lcd.putstr(f"{count}")


# selecting_menu(0)





# #########################################################################
# # PROGRAM

while True:
    try:
        # ----------------------------------------
        # Pusb button stuff
        
        pb1_val = pb1.value()              # Read onboard push button 1, active low
        pb2_val = pb2.value()
        # pb3_val = pb3.value()
        
        if pb1_val == 0:
            if current_menu == menu_categories and not selecting:
                print(f"Set menu to: {menu_categories[menu_location].name}")
                
                menu_controller(menu_categories[menu_location].list)
                sleep(0.5)
                
            
            # This handles the actions of the select button when inside either the Beer or Cocktail categories.
            elif current_menu != menu_categories and not selecting:
                print(f"Selected: {current_menu[menu_location].name}")
                
                # test_amount = 1
                # current_menu[menu_location].add_amount(test_amount) # Runs the add_amount method for the selected drink to add an amount to the order.
                # print(f"Added {test_amount} to amount for: {current_menu[menu_location].name}")
                
                #print(f"{current_menu[menu_location].name} amount = {current_menu[menu_location].amount}")
                
                selecting_menu(0)
                selecting = True  
                sleep(0.5)
            
            # Adds the counter variable to the amount of the current item
            elif selecting:
                current_menu[menu_location].add_amount(counter)
                print(f"{current_menu[menu_location].name} amount = {current_menu[menu_location].amount}")
                selecting = False
                menu_controller(current_menu) # Ensures that the selection screen closes
                counter = 0 # Resets counter variable
                sleep(0.5)
                
            
        
        # Allows for returning to the categories menu if not already in that menu.
        if pb2_val == 0:
            if current_menu != menu_categories:
                menu_location = 0 # Resets menu location to avoid outside index error
                
                if selecting:
                    selecting = False
                    
                print(f"Set current menu to: {menu_categories[menu_location].name}")
                menu_controller(menu_categories) # Returns to the category menu
                sleep(0.5)
        
        # ----------------------------------------
        # Rotary Encoder stuff
        
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
        