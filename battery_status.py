from machine import Pin
import time


# This class borrows code from a prior project: 
# https://github.com/CDBSchoolStuff/IOT2-Cleanflow/blob/main/battery_status.py

class Battery_Status:
    #########################################################################
    # INIT
    
    def __init__(self, battery):
        self.battery = battery
    
    
    ########################################
    # CONFIGURATION

    max_bat_voltage = 4.2
    min_bat_voltage = 3.0


    ########################################
    # OBJECTS
    
    #battery = self.bat_subadc  # The battery object


    ########################################
    # VARIABLES

    # Previous values
    bat_pct = None
    prev_bat_pct = -1                      # The previous battery percentage value
    buffer = []                            # Opret en tom buffer

    # Resistors
    resistor1 = 47
    resistor2 = 22
    max_spaendingsdeler_voltage_measurement = 2.07   # Ikke brugt, bare til egen info. Målt ved 4.2V input med 2x 4.7k modstande.


    ########################################
    # FUNCTIONS

    # Beregner den teoretiske maksimale spænding for spændingsdeleren.
    def calc_spaendingsdeler(U, R1, R2):
        U_out = (U * R2) / (R1 + R2)
        return U_out

    max_spaendingsdeler_voltage = calc_spaendingsdeler(max_bat_voltage, resistor1, resistor2)
    min_spaendingsdeler_voltage = calc_spaendingsdeler(min_bat_voltage, resistor1, resistor2)

    print(f"Spaendingsdeler Max Voltage: {max_spaendingsdeler_voltage}")
    print(f"Spaendingsdeler Min Voltage: {min_spaendingsdeler_voltage}")

    def get_battery_percentage(self):          # The battery voltage percentage
        
        # Beregn procentdelen af batteriets opladning
        percentage = ((self.battery.read_voltage() - self.min_spaendingsdeler_voltage) / (self.max_spaendingsdeler_voltage - self.min_spaendingsdeler_voltage)) * 100
        
        # Sørg for, at procentdelen er inden for intervallet 0% til 100%
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
        
        
    def get_battery_status(self):
        bat_pct = self.calculate_average_battery(20, self.get_battery_percentage())
        
        # Send data if there is a change (this principle saves power)
        if bat_pct != self.prev_bat_pct:

            data_string = str(time.ticks_ms()) + '|' + str(bat_pct) # The data to send. CHANGE IT! (Added the "sensor_id")
                
            #print("Battery Pct: " + data_string)
                
            # Update the previous values for use next time
            self.prev_bat_pct = bat_pct
            print(data_string)
            