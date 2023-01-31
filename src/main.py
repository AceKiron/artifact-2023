import machine
import time

led_onboard = machine.Pin(25, machine.Pin.OUT)
led_extern = machine.Pin(1, machine.Pin.OUT)

while True:
    led_onboard.toggle()
    time.sleep(.2)
    
    led_extern.toggle()
    time.sleep(.2)
