### Keypad layout ###
#                   #
#      1 2 3 +      #
#      4 5 6 -      #
#      7 8 9 *      #
#      C 0 = /      #
#                   #
### Keypad layout ###

# PicoSquared is een python library die ik geschreven heb om programmeren met de Raspberry Pi Pico makkelijker te maken
# Voor het artifact heb ik een groot deel van de code (het niet gebruikte deel) weggelaten
import picosquared as ps

# Hetzelfde als time
import utime

# De Application class
class MyApp(ps.Application):
    def __init__(self):
        # 7, 6, 5, 4, 3, 2, 1 en 0 zijn de pins die gebruikt worden door de 4x4 matrix keypad
        # Init I2C met pins GP8 & GP9 (default I2C0 pins), init oled display, SCL=9, SDA=8, Power=36
        self.keypad = ps.Keypad4x4([7,6,5,4], [3,2,1,0])
        self.oled = ps.SSD1306_I2C(128, 64, 9, 8)
        
        # Formule gelijk stellen aan niks
        self.formula = ""
        
        # Zet de tekst "Formula:" op het scherm
        self.PutOnScreen()

    # Deze functie zorgt ervoor dat je een langere formule nog volledig kan zien
    def FormatFormula(self):
        lines = []
        line = ""
        
        for c in self.formula:
            line += c
            if len(line) == 15:
                lines.append(line)
                line = ""
        
        lines.append(line)
        return lines

    def PutOnScreen(self):
        # Maak het scherm helemaal leeg
        self.oled.fill(0)
        
        # Zet de tekst "Formula:" op de eerste rij
        self.oled.text("Formula:", 5, 8)
        
        # De volgende rijen worden gebruikt voor de formule
        lines = self.FormatFormula()
        for i in range(len(lines)):
            line = lines[i]
            self.oled.text(line, 5, 8 * i + 16)
        
        # Update het scherm
        self.oled.show()

    def AddToFormula(self, string, integer):
        if integer == 12: # C
            self.formula = ""
        elif integer == 14: # =
            try:
                # Probeer de formule op te lossen
                self.formula = str(eval(self.formula))
            except:
                # Als dat niet lukt, zet "ERROR" op het scherm
                self.formula = "ERROR"
        elif integer == 3:
            self.formula += "+"
        elif integer == 7:
            self.formula += "-"
        elif integer == 11:
            self.formula += "*"
        elif integer == 15:
            self.formula += "/"
        else: # 0-9
            self.formula += string

    def Update(self):
        # Lees de waarde van de 4x4 matrix keypad
        value = self.keypad.Read()
        
        # Als de waarde niet gelijk is aan None, dus als een knop ingedrukt is
        if value != None:
            # Voeg het correcte symbool of cijfer aan de formule toe
            self.AddToFormula(ps.Keypad4x4.Keys[value], value)
            
            # Zet de tekst "Equation:" op het scherm, met daaronder de formule
            self.PutOnScreen()
            
            # Wacht 0.3 seconden zodat je het symbool of cijfer niet te vaak wordt toegevoegd
            utime.sleep(0.3)
        
        utime.sleep(0.05)

# De Run() functie is een functie van mijn PicoSquared library's Application class
# Deze functie is simpel gezegd een "while True: Update()" loop
MyApp().Run()
