from machine import Pin

class Enabler:
    def __init__(self, lastEnabled=False, enabled=True):
        self.lastEnabled = lastEnabled
        self.enabled = enabled

        self.Update()
    
    def OnEnable(self):
        pass
    
    def OnDisable(self):
        pass
    
    def Enable(self):
        self.enabled = True
    
    def Disable(self):
        self.enabled = False

    def IsEnabled(self):
        return self.enabled
    
    def Update(self):
        if self.enabled and not self.lastEnabled:
            self.OnEnable()
        elif self.lastEnabled and not self.enabled:
            self.OnDisable()
        
        self.lastEnabled = self.enabled

class Application:
    def __init__(self):
        self.SleepTime = 0

        self.enabled = True

        self.Init()
    
    def Init(self):
        pass
    
    def Update(self):
        pass
    
    def Stop(self):
        self.enabled = False
    
    def Run(self):
        while self.enabled:
            self.Update()

            if self.SleepTime > 0:
                time.sleep(self.SleepTime)

class Input:
    def __init__(self, pin):
        if pin != None:
            self.pin = Pin(pin, Pin.IN)

    def Read(self):
        return self.pin.value()
    
    def Print(self):
        print(self.pin.value())
    
class Output:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.OUT)

        self.WriteLow()
    
    def Read(self):
        return self.pin.value()
    
    def Print(self):
        print(self.pin.value())
    
    def Toggle(self):
        self.pin.toggle()

    def WriteHigh(self):
        self.pin.value(1)
    
    def WriteLow(self):
        self.pin.value(0)

class Button(Input):
    def __init__(self, pin):
        super().__init__(pin)

class LED(Output):
    def __init__(self, pin):
        super().__init__(pin)

class Keypad4x4(Input):
    Keys = ["1", "2", "3", "A",
            "4", "5", "6", "B",
            "7", "8", "9", "C",
            "*", "0", "#", "D"]
    
    def __init__(self, keypad_rows, keypad_columns):
        super().__init__(None)

        self.row_pins = []
        self.col_pins = []
        
        for x in range(4):
            self.row_pins.append(Pin(keypad_rows[x], Pin.OUT))
            self.row_pins[x].value(1)
            
            self.col_pins.append(Pin(keypad_columns[x], Pin.IN, Pin.PULL_DOWN))
            self.col_pins[x].value(0)
    
    def Read(self):
        for row in range(4):
            self.row_pins[row].high()
            
            for col in range(4):
                if self.col_pins[col].value() == 1:
                    self.row_pins[row].low()
                    return row * 4 + col
                
            self.row_pins[row].low()
