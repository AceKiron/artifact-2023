from utils import Typewriter, putTextOnOLED
import picosquared as ps
import apps.AxoTrivia, apps.Calc

class AppSelectionState(ps.State):
    def __init__(self):
        self.keypad = ps.Keypad4x4([7, 6, 5, 4], [3, 2, 1, 0]) # keypad_rows, keypad_columns
        self.oled = ps.SSD1306_I2C(128, 64, 9, 8) # width, height, scl, sda
        
        self.typewriter = Typewriter(
            step=1.5
        )
        self.typewriter.setTargetText(
            "Select app:\n" +
            "1:AxoTrivia\n" +
            "2:Calc"
        )
    
    def update(self):
        self.typewriter.increment()
        
        putTextOnOLED(self.oled, self.typewriter.getText())
        
        value = self.keypad.read()
            
        if value == 0: # 1
            print("App geselecteerd: AxoTrivia")
            ps.Application.getInstance().setState(apps.AxoTrivia.MyState(self.keypad, self.oled))
        elif value == 1: # 2
            print("App geselecteerd: Calc")
            ps.Application.getInstance().setState(apps.Calc.MyState(self.keypad, self.oled))

app = ps.Application.getInstance(
    defaultState = AppSelectionState()
)

app.run(tps=60)
