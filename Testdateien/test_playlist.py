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

# Datei zum Lesen oeffnen
d = open("/var/lib/mpd/playlists/radiosender.m3u","r")

# Einlesen der Zeilen in der Datei
allezeilen = d.readlines()

# Schließen der Datei
d.close()

# Ausgeben der Playlist
print (allezeilen)
print (len(allezeilen))

# Anzahl der Stationen (Ueberfluessige Zeilen abgezogen)
anzahl_stationen = ((len(allezeilen)-1)/2)
print anzahl_stationen
# Neue Liste (stationsliste) erstellen
stationsliste = []
# Stationsnamen herausfiltern und in stationsliste uebergeben
for zeile in range(1,(anzahl_stationen+1)):
	laenge_zeile = len (allezeilen[((zeile*2)-1)])
	print laenge_zeile
	print (allezeilen[((zeile*2)-1)])[11:(laenge_zeile-1)]
	stationsliste.append((allezeilen[((zeile*2)-1)])[11:(laenge_zeile-1)])
print stationsliste
