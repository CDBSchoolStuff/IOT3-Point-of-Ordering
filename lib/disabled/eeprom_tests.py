from machine import I2C, Pin
import eeprom_24xx64
 
class eeprom_tester:  
    def __init__(self):
        self.i2c = I2C(0)
        self.eeprom = eeprom_24xx64.EEPROM_24xx64(self.i2c)
    
    def eeprom_student_navn(self): 
        navn_byte = self.eeprom.read_byte(8000)
        if navn_byte > 20 or navn_byte == 0:
            studerendes_navn = input("Skriv dit navn og efternavn og tryk enter - Max 20 tegn\n")
            while len(studerendes_navn) > 20:
                print("Navn for langt, prøv igen og skriv det kortere! (Max 20 tegn)")
                studerendes_navn = input("Skriv dit navn og efternavn og tryk enter - Max 20 tegn\n")                
            else:    
                self.eeprom.write_string(8000, studerendes_navn)
                print("Dit navn: ",self.eeprom.read_string(8000))
                
    def slet_navn(self):
        print("Sletter EEPROM navn")
        self.eeprom.write_byte(8000, 0) # sætter længden af navn til 0 i EEPROM     
           
    def i2c_ping_EEPROM(self):
        # husk at importere I2C fra machine modulet
        print("Tester EEPROM I2C")
        ping = self.i2c.scan()
        try:
            if ping[0] == 80:
                print("👍 EEPROM I2C virker")
                return "👍 EEPROM I2C virker"
        except:
            print("👎 EEPROM I2C virker ikke")
            return "👎 EEPROM I2C virker ikke"
