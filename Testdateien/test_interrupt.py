#!/usr/bin/python
import time
import RPi.GPIO as IO
# GPIO Warnungen ausschalten
IO.setwarnings(False)
# Layout des GPIO
IO.setmode(IO.BCM)

# Deklarieren der Variabeln GPIO-Ports
ausgang1 = 9
eingang1 = 10
eingang2 = 22
eingang3 = 27
eingang4 = 17

# Setzen der PINS
IO.setup(ausgang1, IO.OUT)
IO.setup(eingang1, IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(eingang2, IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(eingang3, IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(eingang4, IO.IN, pull_up_down=IO.PUD_UP)

# Interrupt Funktionen
def Taster1(callback):  
    print ("Taster 1 wurde gedrueckt")
def Taster2(callback):
    print ("Taster 2 wurde gedrueckt")
def Taster3(callback):
    print ("Taster 3 wurde gedrueckt")
def Taster4(callback):
    print ("Taster 4 wurde gedrueckt")

IO.add_event_detect(eingang1, IO.FALLING, callback=Taster1, bouncetime=20)
IO.add_event_detect(eingang2, IO.FALLING, callback=Taster2, bouncetime=20)
IO.add_event_detect(eingang3, IO.FALLING, callback=Taster3, bouncetime=20)
IO.add_event_detect(eingang4, IO.FALLING, callback=Taster4, bouncetime=20)
while True:
    time.sleep(1)
IO.cleanup()
