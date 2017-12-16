#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import subprocess
import time
import RPi.GPIO as IO # RPi.GPIO wird jetzt als IO angesprochen

# GPIO Warnungen ausschalten
IO.setwarnings(False)

# Layout des GPIO
IO.setmode(IO.BCM)

# mpc Playliste laden
subprocess.call(["mpc", "load", "radiosender"])
#subprocess.Popen("mpc load radiosender", shell=True)
subprocess.call(["mpc", "play", "1"])
#subprocess.Popen("mpc play 1", shell=True)
i=subprocess.Popen(["mpc", "current"])
print (i)

while True:
	pass
