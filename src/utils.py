import random

class Typewriter:
    def __init__(self, step=1):
        self.i = 0
        self.s = ""
        self.step = step
        
    def setTargetText(self, text):
        self.s = text
        self.i = 0
    
    def increment(self):
        self.i += self.step
    
    def getText(self):
        return self.s[:int(self.i)]
    
    def isTyping(self):
        return self.i < len(self.s)

def random_shuffle(seq):
    l = len(seq)
    for i in range(l):
        j = random.randrange(l)
        seq[i], seq[j] = seq[j], seq[i]
    return seq

def formatTextToFitOnOLED(text):
    lines = []
    line = ""
    l = 0
    
    for c in text:
        if c == "\n":
            lines.append(line)
            line = ""
            l = 0
        else:
            line += c
            l += 1
        
        if l == 15:
            lines.append(line)
            line = ""
            l = 0
    
    if line != "":
        lines.append(line)
        
    return lines

def putTextOnOLED(oled, text):
    oled.fill(0)
    
    lines = formatTextToFitOnOLED(text)
    for i in range(len(lines)):
        line = lines[i]
        oled.text(line, 5, 8 + 8 * i)
    
    oled.show()

class ButtonPressListener:
    def __init__(self, initialValue=None):
        self.value = initialValue
        
    def update(self, value):
        updated = self.value != value
        self.value = value
        return updated
