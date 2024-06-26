from machine import Pin
import time


# This class borrows code from a previously judged project: 
# https://github.com/CDBSchoolStuff/IOT2-Cleanflow/blob/main/battery_status.py

class Battery_Status:
    ########################################
    # INIT
    
    def __init__(self, battery):
        self.battery = battery
    
    
    ########################################
    # CONFIGURATION

    MAX_BAT_VOLTAGE = 4.2
    MIN_BAT_VOLTAGE = 3.0
    
    # Resistors
    RESISTOR_1 = 6800
    RESISTOR_2 = 6800


    ########################################
    # VARIABLES

    # Previous values
    bat_pct = None
    prev_bat_pct = -1                      # The previous battery percentage value
    buffer = []                            # Opret en tom buffer


    ########################################
    # FUNCTIONS

    # Beregner den teoretiske maksimale spænding for spændingsdeleren og returnerer resultatet.
    def calc_spaendingsdeler(U, R1, R2):
        U_out = (U * R2) / (R1 + R2)
        return U_out


    max_spaendingsdeler_voltage = calc_spaendingsdeler(MAX_BAT_VOLTAGE, RESISTOR_1, RESISTOR_2)
    min_spaendingsdeler_voltage = calc_spaendingsdeler(MIN_BAT_VOLTAGE, RESISTOR_1, RESISTOR_2)

    print(f"Spaendingsdeler Max Voltage: {max_spaendingsdeler_voltage}")
    print(f"Spaendingsdeler Min Voltage: {min_spaendingsdeler_voltage}")


    def get_battery_percentage(self):          # The battery voltage percentage
        # Beregn procentdelen af batteriets opladning
        percentage = ((self.battery.read_voltage() - self.min_spaendingsdeler_voltage) / (self.max_spaendingsdeler_voltage - self.min_spaendingsdeler_voltage)) * 100
        
        # Sørger for, at procentdelen er inden for intervallet 0% til 100%
        percentage = max(0, min(100, percentage))

        return percentage
    

    def calculate_average_battery(self, window_size, bat_percentage):
        self.buffer.append(bat_percentage)

        if len(self.buffer) > window_size:
            self.buffer.pop(0)  # Fjern ældste værdi, hvis bufferen er fyldt

        if not self.buffer:
            return 0  # Returner 0, hvis bufferen er tom
        return int(sum(self.buffer) / len(self.buffer))


    def get_battery_pct(self):
        bat_pct = self.calculate_average_battery(20, self.get_battery_percentage())
        return bat_pct