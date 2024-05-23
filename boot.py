from machine import Pin, PWM
from gpio_lcd import GpioLcd

#########################################################################
# LCD KONTRAST CONFIGURATION

pin_lcd_contrast = 23
contrast_level = 250                        # Varies from LCD to LCD and wanted contrast level: 0-1023
lcd_contrast = PWM(Pin(pin_lcd_contrast))   # Create PWM object from a pin
lcd_contrast.freq(440)                      # Set PWM frequency
lcd_contrast.duty(contrast_level)

#########################################################################
# LCD KONTRAST CONFIGURATION SLUT

def Print_LCD():
    # Create the LCD object
    lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
                  d4_pin=Pin(33), d5_pin=Pin(32), d6_pin=Pin(21), d7_pin=Pin(22),
                  num_lines=4, num_columns=20)
    lcd.clear()
    lcd.putstr("Programmering -")
    lcd.move_to(0, 1)
    lcd.putstr("Lektion X:")    
    lcd.move_to(0, 2)
    lcd.putstr("Emne")
    #lcd.move_to(0, 3)
    #lcd.putstr("Something!")

Print_LCD()


# Ukommenter, hvis der arbejdes med MQTT
# --------------------------------------

# import sys # Ukommenter, hvis der arbejdes med MQTT

# sys.path.reverse()
# print("\n\n\nESP32 starter op")

# --------------------------------------