### Keypad layout ###
#                   #
#      1 2 3 +      #
#      4 5 6 -      #
#      7 8 9 *      #
#      C 0 = /      #
#                   #
### Keypad layout ###

from utils import putTextOnOLED, ButtonPressListener
import picosquared as ps
import utime

class ErrorState(ps.State):
    def __init__(self, oled, myState):
        self.oled = oled
        self.myState = myState
        
        self.error = ""
    
    def setError(self, e):
        self.error = e
    
    def update(self):
        putTextOnOLED(self.oled, "Error:\n" + self.error)
        utime.sleep(2)
        ps.Application.getInstance().setState(self.myState)

class MyState(ps.State):
    def __init__(self, keypad, oled):
        self.keypad = keypad
        self.oled = oled
        
        self.equation = ""
        
        self.buttonPressListener = ButtonPressListener(
            initialValue = self.keypad.read()
        )
        
        self.errorState = ErrorState(oled, self)
    
    def solve(self):
        try:
            self.equation = str(eval(self.equation))
        except Exception as e:
            ps.Application.getInstance().setState(self.errorState)
            self.errorState.setError(str(e))
    
    def update(self):
        putTextOnOLED(self.oled, "Equation:\n" + self.equation)
        
        value = self.keypad.read()
        
        if self.buttonPressListener.update(value):
            if value == 0:
                self.equation += "1"
            elif value == 1:
                self.equation += "2"
            elif value == 2:
                self.equation += "3"
            elif value == 3:
                self.equation += "+"
            elif value == 4:
                self.equation += "4"
            elif value == 5:
                self.equation += "5"
            elif value == 6:
                self.equation += "6"
            elif value == 7:
                self.equation += "-"
            elif value == 8:
                self.equation += "7"
            elif value == 9:
                self.equation += "8"
            elif value == 10:
                self.equation += "9"
            elif value == 11:
                self.equation += "*"
            elif value == 12:
                self.equation = ""
            elif value == 13:
                self.equation += "0"
            elif value == 14:
                self.solve()
            elif value == 15:
                self.equation += "/"
