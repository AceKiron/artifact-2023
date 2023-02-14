### Keypad layout ###
#                   #
#      1 2 3 +      #
#      4 5 6 -      #
#      7 8 9 *      #
#      C 0 = /      #
#                   #
### Keypad layout ###

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

import picosquared as ps
import utime

equation = ""

oled = SSD1306_I2C(128, 64, I2C(0, scl=Pin(9), sda=Pin(8), freq=200000)) # Init I2C using pins GP8 & GP9 (default I2C0 pins), Init oled display

def FormatEquation():
    lines = []
    line = ""
    
    for c in equation:
        line += c
        if len(line) == 15:
            lines.append(line)
            line = ""
    
    lines.append(line)
    
    return lines

def PutOnScreen():
    oled.fill(0)
    oled.text("Equation:", 5, 8)
    
    lines = FormatEquation()
    for i in range(len(lines)):
        line = lines[i]
        oled.text(line, 5, 8 * i + 16)
    
    oled.show()

def AddToEquation(string, integer):
    global equation
    
    if integer == 12: # C
        equation = ""
    elif integer == 14: # =
        equation = str(eval(equation))
    elif integer == 3:
        equation += "+"
    elif integer == 7:
        equation += "-"
    elif integer == 11:
        equation += "*"
    elif integer == 15:
        equation += "/"
    else:
        equation += string
    
    PutOnScreen()

class MyApp(ps.Application):
    def Init(self):
        self.keypad = ps.Keypad4x4([7,6,5,4], [3,2,1,0])

    def Update(self):
        value = self.keypad.Read()
        
        if value != None:
            AddToEquation(ps.Keypad4x4.Keys[value], value)
            utime.sleep(0.3)
        
MyApp().Run()
