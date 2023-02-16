### Keypad layout ###
#                   #
#      1 2 3 +      #
#      4 5 6 -      #
#      7 8 9 *      #
#      C 0 = /      #
#                   #
### Keypad layout ###

import picosquared as ps
import utime

class MyApp(ps.Application):
    def Init(self):
        self.keypad = ps.Keypad4x4([7,6,5,4], [3,2,1,0])
        self.oled = ps.SSD1306_I2C(128, 64, 9, 8) # Init I2C using pins GP8 & GP9 (default I2C0 pins), Init oled display
        
        self.equation = ""
        
        self.PutOnScreen()

    def FormatEquation(self):
        lines = []
        line = ""
        
        for c in self.equation:
            line += c
            if len(line) == 15:
                lines.append(line)
                line = ""
        
        lines.append(line)
        return lines

    def PutOnScreen(self):
        self.oled.fill(0)
        self.oled.text("Equation:", 5, 8)
        
        lines = self.FormatEquation()
        for i in range(len(lines)):
            line = lines[i]
            self.oled.text(line, 5, 8 * i + 16)
        
        self.oled.show()

    def AddToEquation(self, string, integer):
        if integer == 12: # C
            self.equation = ""
        elif integer == 14: # =
            self.equation = str(eval(self.equation))
        elif integer == 3:
            self.equation += "+"
        elif integer == 7:
            self.equation += "-"
        elif integer == 11:
            self.equation += "*"
        elif integer == 15:
            self.equation += "/"
        else:
            self.equation += string

    def Update(self):
        value = self.keypad.Read()
        
        if value != None:
            self.AddToEquation(ps.Keypad4x4.Keys[value], value)
            self.PutOnScreen()
            utime.sleep(0.3)
        
MyApp().Run()
