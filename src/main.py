import machine
import time

led_onboard = machine.Pin(25, machine.Pin.OUT)
led_extern = machine.Pin(1, machine.Pin.OUT)

while True:
    led_onboard.value(1)
    time.sleep(.2)
    led_extern.value(1)
    time.sleep(.2)
    
    led_onboard.value(0)
    time.sleep(.2)
    led_extern.value(0)
    time.sleep(.2)
