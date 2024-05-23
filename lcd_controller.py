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
# LCD OBJECT

lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
                d4_pin=Pin(33), d5_pin=Pin(32), d6_pin=Pin(21), d7_pin=Pin(22),
                num_lines=4, num_columns=20)


#########################################################################
# FUNCTIONS


def lcd_boot_message(string1, string2):
        lcd.clear()
        lcd.putstr(string1)
        lcd.move_to(0, 2)
        lcd.putstr(string2)
        lcd.move_to(len(string2), 2)
        lcd_dot_animation()

def lcd_dot_animation():
    dots = "....."
    for x in dots:
        sleep(0.2)
        lcd.putstr(x)