# Raspberry PI Test Eingang Taster Ausgang LED
#
# Bibliotheken importieren
import os
import time
import RPi.GPIO as IO
# Layout des GPIO
IO.setmode(IO.BCM)
# Deklarieren der Variabeln GPIO-Ports
ausgang1 = 9
eingang1 = 17
eingang2 = 27
eingang3 = 22
eingang4 = 10
# Deklarieren der Variabeln Sonstige Variablen
abbruch = 0
# Setzen der PINS
IO.setup(ausgang1, IO.OUT)
IO.setup(eingang1, IO.IN)
IO.setup(eingang2, IO.IN)
IO.setup(eingang3, IO.IN)
IO.setup(eingang4, IO.IN)
# Starten des Programms
#
# LED einschalten
IO.output(ausgang1, IO.LOW)
# Taster abfragen
while (abbruch == 0):
	if (IO.input(eingang1)):
		print ("Eingang 1")
	elif (IO.input(eingang2)):
		print ("Eingang 2")
	elif (IO.input(eingang3)):
		print ("Eingang 3")
	elif (IO.input(eingang4)):
		print ("Eingang 4")
		abbruch = 1
# LED ausschalten
IO.output(ausgang1, IO.HIGH)
