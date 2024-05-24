from machine import Pin, PWM
from gpio_lcd import GpioLcd
from time import sleep


#########################################################################
# LCD CONTRAST CONFIGURATION

pin_lcd_contrast = 23
contrast_level = 250                        # Varies from LCD to LCD and wanted contrast level: 0-1023
lcd_contrast = PWM(Pin(pin_lcd_contrast))   # Create PWM object from a pin
lcd_contrast.freq(440)                      # Set PWM frequency
lcd_contrast.duty(contrast_level)


#########################################################################
# CONTANTS

ARROW_STRING = "<---"
BRANDING_STRING = "-={ Bar 16 }=-"


#########################################################################
# LCD OBJECT

lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
                d4_pin=Pin(33), d5_pin=Pin(32), d6_pin=Pin(21), d7_pin=Pin(22),
                num_lines=4, num_columns=20)




#########################################################################
# FUNCTIONS


def lcd_boot_message(string2):
        lcd.clear()
        lcd_print_branding()
        lcd.move_to(0, 2)
        lcd.putstr(string2)
        lcd.move_to(len(string2), 2)
        lcd_dot_animation()

def lcd_dot_animation():
    dots = "....."
    for x in dots:
        sleep(0.2)
        lcd.putstr(x)
        
def lcd_print_menu(menu_location, menu_list):
    lcd.clear()
    lcd_print_branding()
    lcd.move_to(0, 1)
    if menu_location != 0:
        lcd.putstr(f"{menu_location - 1}: {menu_list[menu_location - 1]}") # Previous menu location
    lcd.move_to(0, 2)
    
    lcd.putstr(f"{menu_location}: {menu_list[menu_location]}") # Curent menu location
    lcd.move_to(20 - len(ARROW_STRING), 2) # len(ARROW_STRING) ensures that the arrow will always be in the correct place.
    lcd.putstr(ARROW_STRING)
    lcd.move_to(0, 3)
    if menu_location < len(menu_list) - 1:
        lcd.putstr(f"{menu_location + 1}: {menu_list[menu_location + 1]}") # Next menu location
    print(f"Menu Location: {menu_location}")
    
    
def lcd_print_branding():
    lcd.move_to(0, 0)
    lcd.putstr(center_text(BRANDING_STRING))
    
    
def center_text(string):
    spacing_amount = (20-len(string))/2

    spaces = ""
    for i in range(spacing_amount):
        spaces += " "
    
    return spaces + string


def align_text_right(string):
    return (20-len(string))