from machine import Pin
import time

led = Pin(14, Pin.OUT)
led_onboard = Pin(25, Pin.OUT)

button1 = Pin(12, Pin.IN)
button2 = Pin(13, Pin.IN)

lastEnabled = 0
enabled = 1

while True:
    if button1.value():
        enabled = 1
    elif button2.value():
        enabled = 0
    
    if lastEnabled != enabled:
        lastEnabled = enabled
        if enabled:
            led_onboard.value(1)
        else:
            led_onboard.value(0)
            led.value(0)
    
    if enabled:
        led.toggle()
        
    time.sleep(0.1)
