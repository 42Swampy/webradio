#! /usr/bin/python3
# -*- coding: utf-8 -*-
#  
# Raspberry PI Webradio Projekt
#
# Bibliotheken importieren
import os
import subprocess
import time
import feedparser
import RPi.GPIO as IO # RPi.GPIO wird jetzt als IO angesprochen

# GPIO Warnungen ausschalten
IO.setwarnings(False)

# Layout des GPIO
IO.setmode(IO.BCM)

# Deklarieren der Variabeln GPIO-Ports
ausgang1 = 15
ausgang2 = 11
ausgang3 = 3
ausgang4 = 9
eingang1 = 10
eingang2 = 22
eingang3 = 27
eingang4 = 17

# Deklarieren der Variabeln GPIO-Ports Display
DISPLAY_RS = 7
DISPLAY_E  = 8
DISPLAY_DATA4 = 25 
DISPLAY_DATA5 = 24
DISPLAY_DATA6 = 23
DISPLAY_DATA7 = 18

# Deklarieren der Variabeln Sonstige Variablen
led1 = 0 # Gruen
led2 = 0 # Blau
led3 = 0 # Rot
taste1 = 0
taste2 = 0
taste3 = 0
taste4 = 0
auswahl = 1
auswahl2 = 1
auswahl3 = 1
auswahl_menu = 1
abbruch = 0
abbruch2 = 0
abbruch3 = 0
abbruch4 = 0
abbruch5 = 0
anzahl_stationen = 0
anzahl_mp3 = 0
anzahl_feeds = 0
radiomodus = 1
usbmodus = 0
laufzeit = 0
ganzer_feed = " "
feedliste = []
stationsliste = []
usbliste = []
menuliste = ["USB-Stick","Selbsttest","Debug-Modus","Herunterfahren","Wiedegabe anhalten","Nachtmodus","RSS-Feeds","Uhr/Timer"]
uhrzeit = time.localtime() # Uhrzeit/Datum holen
zeiteinstellung = 0
timer = 0

# CGRAM Benutzerdefinierte Zeichen festlegen
play = [16,24,28,30,30,28,24,16] # Abspielen-Zeichen
bw = [17,19,23,31,31,23,19,17] # Rueckwaerts-Zeichen
up = [0,0,4,14,31,0,0,0] # Hoch-Zeichen
down = [0,0,31,14,4,0,0,0] # Runter-Zeichen
fw = [17,25,29,31,31,29,25,17] # Vorwaerts-Zeichen
menu = [31,0,31,0,31,0,31,0] # Menue-Zeichen
zurueck = [0,1,1,5,13,31,12,4] # Zurueck-Zeichen
enter = [27,10,4,10,27,0,0,0] # Enter -Zeichen

# Display initialisieren
DISPLAY_WIDTH = 20 	# Zeichen je Zeile
DISPLAY_LINE_1 = 0x80 	# Adresse der ersten Display Zeile
DISPLAY_LINE_2 = 0xC0 	# Adresse der zweiten Display Zeile
DISPLAY_LINE_3 = 0x94 	# Adresse der ersten Display Zeile
DISPLAY_LINE_4 = 0xD4 	# Adresse der zweiten Display Zeile
DISPLAY_CHR = True
DISPLAY_CMD = False
E_PULSE = 0.0005
E_DELAY = 0.0005

# Setzen der PINS (Eingaenge für Interruptfunktionen)
IO.setup(ausgang1, IO.OUT)
IO.setup(ausgang2, IO.OUT)
IO.setup(ausgang3, IO.OUT)
IO.setup(ausgang4, IO.OUT)
IO.setup(eingang1, IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(eingang2, IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(eingang3, IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(eingang4, IO.IN, pull_up_down=IO.PUD_UP)

# Setzen der PINS Display
IO.setup(DISPLAY_E, IO.OUT)
IO.setup(DISPLAY_RS, IO.OUT)
IO.setup(DISPLAY_DATA4, IO.OUT)
IO.setup(DISPLAY_DATA5, IO.OUT)
IO.setup(DISPLAY_DATA6, IO.OUT)
IO.setup(DISPLAY_DATA7, IO.OUT)

# Interrupt Funktionen
def Taster1(callback):
	global taste1
	print ("Taster 1 wurde gedrueckt")
	taste1 = 1
def Taster2(callback):
	global taste2
	print ("Taster 2 wurde gedrueckt")
	taste2 = 1
def Taster3(callback):
	global taste3
	print ("Taster 3 wurde gedrueckt")
	taste3 = 1
def Taster4(callback):
	global taste4
	print ("Taster 4 wurde gedrueckt")
	taste4 = 1

# Displayfunktionen (von http://www.schnatterente.net)
def display_init():
	lcd_byte(0x33,DISPLAY_CMD)
	lcd_byte(0x32,DISPLAY_CMD)
	lcd_byte(0x28,DISPLAY_CMD)
	lcd_byte(0x0C,DISPLAY_CMD)  
	lcd_byte(0x06,DISPLAY_CMD)
	lcd_byte(0x01,DISPLAY_CMD)
	
def kill_umlauts(message):
	try:
		message = message.replace('ä', chr(225))
		message = message.replace('ö', chr(239))
		message = message.replace('ü', chr(245))
		message = message.replace('Ä', chr(225))
		message = message.replace('Ö', chr(239))
		message = message.replace('Ü', chr(245))
		message = message.replace('ß', chr(226))
		message = message.replace('°', chr(223))
		message = message.replace('µ', chr(228))
		message = message.replace('´', chr(96))
		message = message.replace('€', chr(227))
		message = message.replace('–', '-')
		message = message.replace('“', '"')
		message = message.replace('”', '"')
		message = message.replace('„', '"')
		message = message.replace('’', '\'')
		message = message.replace('‘', '\'')
		message = message.replace('è', 'e')
		message = message.replace('é', 'e')
		message = message.replace('ê', 'e')
		message = message.replace('á', 'a')
		message = message.replace('à', 'a')
		message = message.replace('â', 'a')
		message = message.replace('©', '(c)')
	except:
		return message;
	return message

def lcd_string(message):
	message = kill_umlauts(message)
	message = message.ljust(DISPLAY_WIDTH," ")  
	for i in range(DISPLAY_WIDTH):
	  lcd_byte(ord(message[i]),DISPLAY_CHR)

def lcd_byte(bits, mode):
	IO.output(DISPLAY_RS, mode)
	IO.output(DISPLAY_DATA4, False)
	IO.output(DISPLAY_DATA5, False)
	IO.output(DISPLAY_DATA6, False)
	IO.output(DISPLAY_DATA7, False)
	if bits&0x10==0x10:
	  IO.output(DISPLAY_DATA4, True)
	if bits&0x20==0x20:
	  IO.output(DISPLAY_DATA5, True)
	if bits&0x40==0x40:
	  IO.output(DISPLAY_DATA6, True)
	if bits&0x80==0x80:
	  IO.output(DISPLAY_DATA7, True)
	time.sleep(E_DELAY)    
	IO.output(DISPLAY_E, True)  
	time.sleep(E_PULSE)
	IO.output(DISPLAY_E, False)  
	time.sleep(E_DELAY)      
	IO.output(DISPLAY_DATA4, False)
	IO.output(DISPLAY_DATA5, False)
	IO.output(DISPLAY_DATA6, False)
	IO.output(DISPLAY_DATA7, False)
	if bits&0x01==0x01:
	  IO.output(DISPLAY_DATA4, True)
	if bits&0x02==0x02:
	  IO.output(DISPLAY_DATA5, True)
	if bits&0x04==0x04:
	  IO.output(DISPLAY_DATA6, True)
	if bits&0x08==0x08:
	  IO.output(DISPLAY_DATA7, True)
	time.sleep(E_DELAY)    
	IO.output(DISPLAY_E, True)  
	time.sleep(E_PULSE)
	IO.output(DISPLAY_E, False)  
	time.sleep(E_DELAY)

# Funktion von http://www.raspberrypi-spy.co.uk/ uebernommen
def cgchar(CGCHR, bytes):
  lcd_byte(CGCHR, DISPLAY_CMD)
  for value in (bytes[0],bytes[1],bytes[2],bytes[3],bytes[4],bytes[5],bytes[6],bytes[7]):
    lcd_byte(value, DISPLAY_CHR)

# Funktion um alle Zeilen zu loeschen
def display_erase():
	lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
	lcd_string("                    ")
	lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
	lcd_string("                    ")
	lcd_byte(DISPLAY_LINE_3, DISPLAY_CMD)
	lcd_string("                    ")
	lcd_byte(DISPLAY_LINE_4, DISPLAY_CMD)
	lcd_string("                    ")

# Laufschrift Funktion
def laufschrift(bereich):
	for i in range(0,bereich):
		# Zeile ausgeben
		ausgabe_laufschrift = station[i:(i+20)]
		lcd_byte(DISPLAY_LINE_4, DISPLAY_CMD)
		lcd_string(ausgabe_laufschrift)
		time.sleep(0.5)
		# Zeile loeschen
		lcd_byte(DISPLAY_LINE_4, DISPLAY_CMD)
		lcd_string("                    ")
		# Bei Tastendruck Schleife beenden
		if (taste1 == 1) or (taste2 == 1) or (taste3 == 1) or (taste4 == 1):
			break

# Stationsnamen - Datei einlesen
def Stationsnamen(stationsliste):
	# Datei zum Lesen oeffnen
	d = open("/home/pi/playlists/radiosender.m3u","r")
	# Einlesen der Zeilen in der Datei
	allezeilen = d.readlines()
	# Schließen der Datei
	d.close()
	# Anzahl der Stationen (Ueberfluessige Zeilen abgezogen)
	global anzahl_stationen
	anzahl_stationen = (int((len(allezeilen)-1)/2))
	for zeile in range(1,(anzahl_stationen+1)):
		laenge_zeile = len (allezeilen[((zeile*2)-1)])
		stationsliste.append((allezeilen[((zeile*2)-1)])[11:(laenge_zeile-1)])
	return stationsliste

# USB - Datei einlesen
def Usbnamen(usbliste):
	# Datei zum Lesen oeffnen
	d = open("/home/pi/playlists/usbliste.m3u","r")
	# Einlesen der Zeilen in der Datei
	allezeilen = d.readlines()
	# Schließen der Datei
	d.close()
	# Anzahl der Dateien (Ueberfluessige Zeilen abgezogen)
	global anzahl_mp3
	anzahl_mp3 = (int(len(allezeilen)))
	for zeile in range(0,(anzahl_mp3)):
		laenge_zeile = len (allezeilen[zeile])
		usbliste.append((allezeilen[zeile])[0:(laenge_zeile-1)])
	return usbliste
	
# RSS-Feed - Datei einlesen
def rssnamen(feedliste):
	# Datei zum Lesen oeffnen
	d = open("/home/pi/playlists/rssfeeds.m3u","r")
	# Einlesen der Zeilen in der Datei
	allezeilen = d.readlines()
	# Schließen der Datei
	d.close()
	# Anzahl der RSS-Feeds (Ueberfluessige Zeilen abgezogen)
	global anzahl_feeds
	anzahl_feeds = (int(len(allezeilen)))
	for zeile in range(0,(anzahl_feeds)):
		laenge_zeile = len (allezeilen[zeile])
		feedliste.append((allezeilen[zeile])[0:(laenge_zeile-1)])
	return feedliste

# Optionsmenue anzeigen
def Optionsmenue():
	global auswahl_menu
	global menuliste
	global laenge_menu
	# 1. Zeile
	if (auswahl_menu < 1):
		lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
		lcd_string("  "+menuliste[(laenge_menu + auswahl_menu)])
	else:
		lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
		lcd_string("  "+menuliste[(auswahl_menu-1)])
	# 2. Zeile
	lcd_byte(DISPLAY_LINE_3, DISPLAY_CMD)
	lcd_string(chr(0)+" "+menuliste[auswahl_menu])
	# 3. Zeile
	if (auswahl_menu > (laenge_menu-1)):
		lcd_byte(DISPLAY_LINE_4, DISPLAY_CMD)
		lcd_string("  "+menuliste[(laenge_menu - auswahl_menu)])
	else:
		lcd_byte(DISPLAY_LINE_4, DISPLAY_CMD)
		lcd_string("  "+menuliste[(auswahl_menu+1)])

# Herunterfahren
def Herunterfahren():
	print ("Eingang 1")
	taste1 = 0   #Taste zuruecksetzen
	display_erase()
	lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
	lcd_string("********************")
	lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
	lcd_string("* Webradio wird    *")
	lcd_byte(DISPLAY_LINE_3, DISPLAY_CMD)
	lcd_string("* heruntergefahren *")
	lcd_byte(DISPLAY_LINE_4, DISPLAY_CMD)
	lcd_string("********************")
	time.sleep(1)
	display_erase()
	# mpd beenden
	subprocess.call(["mpc", "stop"])
	# LED ausschalten
	IO.output(ausgang1, IO.LOW)
	IO.output(ausgang2, IO.LOW)
	IO.output(ausgang3, IO.LOW)
	# LCD-Anzeige loeschen
	display_erase()
	# Display Beleuchtung ausschalten
	IO.output(ausgang4, IO.LOW)
	# Herunterfahren
	print ("Fahre System herunter")
	subprocess.call(["sudo", "halt"])
	time.sleep(10)

#
# Starten
#
	   
# mpc Playliste laden
subprocess.call(["mpc", "clear"])
subprocess.call(["mpc", "load", "radiosender"])

# Display initialisieren
display_init()

# Benutzerdefinierte Zeichen setzen
cgchar(0x40, play) # Play auf chr(0) setzen
cgchar(0x48, bw) # Zurueck auf chr(1) setzen
cgchar(0x50, fw) # Vorwaerts auf chr(2) setzen
cgchar(0x58, menu) # Menue auf chr(3) setzen
cgchar(0x60, up) # Hoch auf chr(4) setzen
cgchar(0x68, down) # Runter auf chr(5) setzen
cgchar(0x70, zurueck) # Zurueck auf chr(6) setzen
cgchar(0x78, enter) # Enter auf chr(7) setzen

# Display Beleuchtung einschalten
IO.output(ausgang4, IO.HIGH)

# Anzeige der Bereitschaft des Webradios
lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
lcd_string("********************")
lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
lcd_string("* Webradio bereit  *")
lcd_byte(DISPLAY_LINE_3, DISPLAY_CMD)
lcd_string("*                  *")
lcd_byte(DISPLAY_LINE_4, DISPLAY_CMD)
lcd_string("********************")
time.sleep(1)
print ("Webradio bereit")

# LED einschalten
IO.output(ausgang1, IO.HIGH)
IO.output(ausgang2, IO.LOW)
IO.output(ausgang3, IO.LOW)

# Stationen aus Playlist uebergeben
Stationsnamen(stationsliste)

# Menue auf LCD anzeigen
display_erase()
lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
lcd_string("  "+chr(0)+"    "+chr(1)+"    "+chr(2)+"    "+chr(3))

# Interrupts definieren
IO.add_event_detect(eingang1, IO.FALLING, callback=Taster1, bouncetime=500)
IO.add_event_detect(eingang2, IO.FALLING, callback=Taster2, bouncetime=500)
IO.add_event_detect(eingang3, IO.FALLING, callback=Taster3, bouncetime=500)
IO.add_event_detect(eingang4, IO.FALLING, callback=Taster4, bouncetime=500)

#
# Hauptprogramm
#

# Eingabe machen
# Taster abfragen
while (abbruch == 0):
	if ((timer == 1) and (laufzeit <= (int(time.time())))):
		Herunterfahren()
	# Auswahl anzeigen
	lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
	lcd_string("Radiomodus ("+str(auswahl)+")")
	lcd_byte(DISPLAY_LINE_3, DISPLAY_CMD)
	lcd_string(stationsliste[(auswahl-1)])
	# Sender ausgeben
	f = subprocess.Popen(["mpc", "current"], stdout=subprocess.PIPE)
	station = ""
	station += str((f.stdout.read()).decode(encoding='UTF-8'))
	# Ursprüngliche Laenge station
	laenge_ursprung = len(station)
	# Letztes Zeichen loeschen
	station = station[:-1]
	# 20 Leerzeichen an station anhaengen
	station = station + "                    "
	laenge = len(station)
	bereich = laenge - 19
	# Laufschrift
	if (laenge_ursprung >= 21):
		laufschrift(bereich)
	# Wenn die urspruengliche Laenge 20 Zeichen oder weniger entspricht, station nur statisch ausgeben
	else:
		lcd_byte(DISPLAY_LINE_4, DISPLAY_CMD)
		lcd_string(station)
	# Taster auswerten
	if (taste1 == 1):
		# Radiomodus anschalten
		radiomodus = 1
		print ("Eingang 1")
		# Webradio spielen
		subprocess.call(["mpc", "play", str(auswahl)])
		# mpc play auswahl
		print (auswahl)
		taste1 = 0   #Taste zuruecksetzen
		time.sleep(0.01)
	elif (taste2 == 1):
		print ("Eingang 2")
		auswahl=auswahl-1
		# Wenn Stationsanfang erreicht ist, wieder auf Stationsende springen
		if (auswahl == 0):
			auswahl = anzahl_stationen
		print (auswahl)
		taste2 = 0   #Taste zuruecksetzen
		time.sleep(0.01)
	elif (taste3 == 1):
		print ("Eingang 3")
		auswahl=auswahl+1
		# Wenn Stationsende erreicht ist, wieder auf Stationsanfang springen
		if (auswahl == (anzahl_stationen+1)):
			auswahl = 1
		print (auswahl)
		taste3 = 0   # Taste zuruecksetzen
		time.sleep(0.01)
	elif (taste4 == 1):
		#
		# Optionsmenue
		#
		print ("Eingang 4")
		print (auswahl)
		taste4 = 0   # Taste zuruecksetzen
		abbruch2 = 0
		# Laenge der Menue-Einträge ermitteln
		laenge_menu = (len(menuliste)-1)
		print (laenge_menu)
		# Optionsmenue anzeigen
		display_erase()
		lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
		lcd_string("  "+chr(5)+"    "+chr(7)+"    "+chr(4)+"    "+chr(6))
		Optionsmenue()
		# Optionsmenue auswerten
		while (abbruch2 == 0):
			if ((timer == 1) and (laufzeit <= (int(time.time())))):
				Herunterfahren()
			# Taster auswerten
			# Im Optionsmenue eins runter gehen
			if (taste1 == 1):
				print ("Eingang 1")
				print (auswahl)
				auswahl_menu = auswahl_menu + 1
				if (auswahl_menu > laenge_menu):
					auswahl_menu = 0
				print (auswahl_menu)
				# Neues Menue anzeigen
				Optionsmenue()
				taste1 = 0   #Taste zuruecksetzen
				time.sleep(0.01)
			# Optionen abfragen
			elif (taste2 == 1):
				print ("Eingang 2")
				print (auswahl)
				taste2 = 0   #Taste zuruecksetzen
				#
				# Debug-Modus
				#
				if (auswahl_menu == 2):
					abbruch = 1
					abbruch2 = 1
				#
				# Selbsttest
				#
				if (auswahl_menu == 1):
					# Alles ausschalten
					display_erase()
					IO.output(ausgang1, IO.LOW)
					IO.output(ausgang2, IO.LOW)
					IO.output(ausgang3, IO.LOW)
					subprocess.call(["mpc", "stop"])
					# Display testen
					display_erase()
					lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
					lcd_string("Displaytest:")
					lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
					lcd_string("--------------------")
					lcd_byte(DISPLAY_LINE_3, DISPLAY_CMD)
					lcd_string("ABCDEFGHIJKLMNOPQRST")
					lcd_byte(DISPLAY_LINE_4, DISPLAY_CMD)
					lcd_string("abcdefghijklmnopqrst")
					time.sleep(1.50)
					display_erase()
					# Audioausgabe testen
					display_erase()
					lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
					lcd_string("Test Audio links:")
					lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
					lcd_string("--------------------")
					subprocess.call("speaker-test -t wav -w Front_Left.wav -c 2 -s 1", shell=True)
					time.sleep(1.50)
					display_erase()
					lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
					lcd_string("Test Audio rechts:")
					lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
					lcd_string("--------------------")
					subprocess.call("speaker-test -t wav -w Front_Right.wav -c 2 -s 2", shell=True)
					time.sleep(1.50)
					# LEDs testen
					display_erase()
					lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
					lcd_string("LED Test 1 (Grün):")
					lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
					lcd_string("--------------------")
					IO.output(ausgang1, IO.HIGH)
					IO.output(ausgang2, IO.LOW)
					IO.output(ausgang3, IO.LOW)
					time.sleep(1.50)
					display_erase()
					lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
					lcd_string("LED Test 2 (Blau):")
					lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
					lcd_string("--------------------")
					IO.output(ausgang1, IO.LOW)
					IO.output(ausgang2, IO.HIGH)
					IO.output(ausgang3, IO.LOW)
					time.sleep(1.50)
					display_erase()
					lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
					lcd_string("LED Test 3 (Rot):")
					lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
					lcd_string("--------------------")
					IO.output(ausgang1, IO.LOW)
					IO.output(ausgang2, IO.LOW)
					IO.output(ausgang3, IO.HIGH)
					time.sleep(1.50)
					# Optionsmenue wieder herstellen
					display_erase()
					lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
					lcd_string("  "+chr(5)+"    "+chr(7)+"    "+chr(4)+"    "+chr(6))
					# Altes Menue anzeigen
					Optionsmenue()
					IO.output(ausgang1, IO.HIGH)
					IO.output(ausgang2, IO.LOW)
					IO.output(ausgang3, IO.LOW)
				#
				# Nachtmodus
				#
				if (auswahl_menu == 5):
					# Display Beleuchtung ausschalten
					IO.output(ausgang4, IO.LOW)
					# LED ausschalten
					IO.output(ausgang1, IO.LOW)
					IO.output(ausgang2, IO.LOW)
					IO.output(ausgang3, IO.LOW)
					while (taste1 == 0 and taste2 == 0 and taste3 == 0 and taste4 == 0):
						if ((timer == 1) and (laufzeit <= (int(time.time())))):
							Herunterfahren()
						time.sleep(0.1)
					# Alles wieder zuruecksetzen
					IO.output(ausgang4, IO.HIGH)
					IO.output(ausgang1, IO.HIGH)
					taste1=0
					taste2=0
					taste3=0
					taste4=0
					IO.output(ausgang3, IO.LOW)
				#
				# Uhr/Timer
				#
				if (auswahl_menu == 7):
					# Menue auf LCD anzeigen
					display_erase()
					lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
					lcd_string("  "+chr(5)+"    "+chr(7)+"    "+chr(4)+"    "+chr(6))
					if ((timer == 0) or (zeiteinstellung == 0)):
						lcd_byte(DISPLAY_LINE_3, DISPLAY_CMD)
						lcd_string("Timer: (aus)")
					else:
						lcd_byte(DISPLAY_LINE_3, DISPLAY_CMD)
						lcd_string("Timer: "+str(zeiteinstellung)+" (min)")
					while (abbruch5 == 0):
						if ((timer == 1) and (laufzeit <= (int(time.time())))):
							Herunterfahren()
						# Laufzeit nicht negativ werden lassen
						if (laufzeit <= 0):
							laufzeit = int(time.time())
						# Datum und Uhrzeit ausgeben
						lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
						lcd_string(time.strftime("%d.%m.%Y %H:%M:%S"))
						# Countdown ausgeben
						if (timer == 1):
							lcd_byte(DISPLAY_LINE_4, DISPLAY_CMD)
							lcd_string("Noch "+str(int(((laufzeit/60)-(time.time()/60)))+1)+" Minuten")
						else:
							lcd_byte(DISPLAY_LINE_4, DISPLAY_CMD)
							lcd_string("Timer ausgeschaltet ")
						# Um 10 min erhoehen
						if (taste1 == 1):
							# Zeit nicht negativ werden lassen
							if (zeiteinstellung < 10):
								zeiteinstellung = 0
							else:
								zeiteinstellung = zeiteinstellung-10
							if (zeiteinstellung == 0):
								lcd_byte(DISPLAY_LINE_3, DISPLAY_CMD)
								lcd_string("Timer: (aus)")
							else:
								lcd_byte(DISPLAY_LINE_3, DISPLAY_CMD)
								lcd_string("Timer: "+str(zeiteinstellung)+" (min)")
							taste1 = 0   #Taste zuruecksetzen
							time.sleep(0.01)
						if (taste2 == 1):
							# Betriebszeit setzen
							laufzeit = (int(time.time())+(zeiteinstellung*60))
							# Timer an- oder ausschalten
							if (laufzeit > time.time()):
								timer = 1
							else:
								timer = 0	
							taste2 = 0   #Taste zuruecksetzen
							time.sleep(0.01)
						# Um 10 min verringern
						if (taste3 == 1):
							zeiteinstellung = zeiteinstellung+10
							# Zeitrahmen 24 Stunden
							if (zeiteinstellung > 1450):
								zeiteinstellung = 1450
							lcd_byte(DISPLAY_LINE_3, DISPLAY_CMD)
							lcd_string("Timer: "+str(zeiteinstellung)+" (min)")
							taste3 = 0   #Taste zuruecksetzen
							time.sleep(0.01)
						elif (taste4 == 1):
							# RSS - Menue beenden
							print ("Eingang 4")
							taste4 = 0   #Taste zuruecksetzen
							abbruch5 = 1
							time.sleep(0.01)
					abbruch5 = 0
					# Optionsmenue anzeigen
					display_erase()
					lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
					lcd_string("  "+chr(5)+"    "+chr(7)+"    "+chr(4)+"    "+chr(6))
					Optionsmenue()
				#
				# RSS - Feed
				#
				if (auswahl_menu == 6):
					# Menue auf LCD anzeigen
					display_erase()
					lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
					lcd_string("  "+chr(0)+"    "+chr(1)+"    "+chr(2)+"    "+chr(6))
					# Die RSS - Feed URLs aus Datei einlesen
					rssnamen(feedliste)
					print (anzahl_feeds)
					print (feedliste)
					while (abbruch5 == 0):
						if ((timer == 1) and (laufzeit <= (int(time.time())))):
							Herunterfahren()
						# Auswahl anzeigen
						lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
						lcd_string("RSS-Feed ("+str(auswahl3)+")")
						lcd_byte(DISPLAY_LINE_3, DISPLAY_CMD)
						lcd_string(feedliste[(auswahl3-1)])
						# Taster auswerten						
						if (taste1 == 1):
							print ("Eingang 1")
							taste1 = 0   #Taste zuruecksetzen						
							# Feed herunterladen anzeigen
							print ("Lade RSS-Feed")
							lcd_byte(DISPLAY_LINE_4, DISPLAY_CMD)
							lcd_string("                    ")
							lcd_byte(DISPLAY_LINE_4, DISPLAY_CMD)
							lcd_string("Lade RSS-Feed")
							# Feed herunterladen
							d=feedparser.parse(feedliste[(auswahl3-1)])
							print ("RSS-Feed geladen")
							lcd_byte(DISPLAY_LINE_4, DISPLAY_CMD)
							lcd_string("                    ")
							time.sleep(0.01)
							# Titel als erstes lesen
							ganzer_feed = " "
							ganzer_feed = ganzer_feed+(d.feed.title)+" --- "
							# Die Feeds danach lesen
							for i in range(len(d['entries'])):   # Anzahl der Eintraege: len(d['entries'])
								ganzer_feed = ganzer_feed+(d.entries[i].title)+" --- "
							station = ganzer_feed # Variable fuer Laufschriftfunktion 
							# 20 Leerzeichen an station anhaengen
							station = station + "                    "
							laenge = len(station)
							bereich = laenge - 19
							print (bereich)
							print (station)
							laufschrift(bereich)
						elif (taste2 == 1):
							# RSS - Feed erhoehen
							print ("Eingang 2")
							auswahl3=auswahl3-1
							# Wenn Feedanfang erreicht ist, wieder auf Feedende springen
							if (auswahl3 == 0):
								auswahl3 = anzahl_feeds
								print (auswahl3)
							taste2 = 0   # Taste zuruecksetzen
							time.sleep(0.01)
						elif (taste3 == 1):
							# RSS - Feed erniedrigen
							print ("Eingang 3")
							auswahl3=auswahl3+1
							# Wenn Feedende erreicht ist, wieder auf Feedanfang springen
							if (auswahl3 == (anzahl_feeds+1)):
								auswahl3 = 1
								print (auswahl3)
							taste3 = 0   #Taste zuruecksetzen
							time.sleep(0.01)
						elif (taste4 == 1):
							# RSS - Menue beenden
							print ("Eingang 4")
							taste4 = 0   #Taste zuruecksetzen
							abbruch5 = 1
							time.sleep(0.01)
					abbruch5 = 0
					# Optionsmenue anzeigen
					display_erase()
					lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
					lcd_string("  "+chr(5)+"    "+chr(7)+"    "+chr(4)+"    "+chr(6))
					Optionsmenue()
				#
				# Herunterfahren
				#
				if (auswahl_menu == 3):
					display_erase()
					while  (abbruch4 == 0):
						if ((timer == 1) and (laufzeit <= (int(time.time())))):
							Herunterfahren()
						lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
						lcd_string("  "+chr(7)+"              "+chr(6)+"  ")
						lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
						lcd_string("--------------------")
						lcd_byte(DISPLAY_LINE_3, DISPLAY_CMD)
						lcd_string("  Herunterfahren    ")
						lcd_byte(DISPLAY_LINE_4, DISPLAY_CMD)
						lcd_string(" Sind Sie sicher ?  ")
						# Taster auswerten
						if (taste1 == 1):
							Herunterfahren()
						elif (taste2 == 1):
							# Keine Funktion
							print ("Eingang 2")
							taste2 = 0   #Taste zuruecksetzen
							time.sleep(0.01)
						elif (taste3 == 1):
							# Keine Funktion
							print ("Eingang 3")
							taste3 = 0   # Taste zuruecksetzen
							time.sleep(0.01)
						elif (taste4 == 1):
							# Abbruch Herunterfahren
							print ("Eingang 4")
							taste4 = 0   #Taste zuruecksetzen
							abbruch4 = 1
							time.sleep(0.01)
					abbruch4 = 0
					# Optionsmenue anzeigen
					display_erase()
					lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
					lcd_string("  "+chr(5)+"    "+chr(7)+"    "+chr(4)+"    "+chr(6))
					Optionsmenue()
				#
				# Wiedergabe anhalten
				#
				if (auswahl_menu == 4):
					subprocess.call(["mpc", "stop"])
					
				#
				# USB Modus
				#
				if (auswahl_menu == 0):
					if (usbmodus == 0):
						# MPC vorbereiten
						subprocess.call(["mpc", "stop"])
						subprocess.call(["mpc", "clear"])
						subprocess.call("mpc update --wait", shell=True)
						subprocess.call("mpc ls | mpc add usb0", shell=True)
						subprocess.call("mpc listall > /home/pi/playlists/usbliste.m3u", shell=True)
						# Eintraege aud Datei holen
						# Variable - USB - Liste leeren
						usbliste = []
						Usbnamen(usbliste)
						print (anzahl_mp3)
						print (usbliste)
						# Wenn keine Dateien auf USB-Stick gefunden wurden
						if (anzahl_mp3 == 0):
							display_erase()
							lcd_byte(DISPLAY_LINE_3, DISPLAY_CMD)
							lcd_string("Kein USB-Stick, oder")
							lcd_byte(DISPLAY_LINE_4, DISPLAY_CMD)
							lcd_string("   keine Dateien !  ")
							time.sleep(1)
					# Auswahl USB Modus
					display_erase()
					lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
					lcd_string("  "+chr(0)+"    "+chr(1)+"    "+chr(2)+"    "+chr(6))
					while ((abbruch3 == 0) and (anzahl_mp3 > 0)):
						if ((timer == 1) and (laufzeit <= (int(time.time())))):
							Herunterfahren()
						# Auswahl anzeigen
						lcd_byte(DISPLAY_LINE_2, DISPLAY_CMD)
						lcd_string("USB - Stick ("+str(auswahl2)+")")
						lcd_byte(DISPLAY_LINE_3, DISPLAY_CMD)
						lcd_string((usbliste[((auswahl2)-1)])[5:])
						# Sender ausgeben
						f = subprocess.Popen(["mpc", "current"], stdout=subprocess.PIPE)
						station = ""
						station += str((f.stdout.read()).decode(encoding='UTF-8'))
						# Ursprüngliche Laenge station
						laenge_ursprung = len(station)
						# Letztes Zeichen loeschen
						station = station[:-1]
						# 20 Leerzeichen an station anhaengen
						station = station + "                    "
						laenge = len(station)
						bereich = laenge - 19
						# Laufschrift
						if (laenge_ursprung >= 21):
							laufschrift(bereich)
						# Wenn die urspruengliche Laenge 20 Zeichen oder weniger entspricht, station nur statisch ausgeben
						else:
							lcd_byte(DISPLAY_LINE_4, DISPLAY_CMD)
							lcd_string(station)
						# Taster auswerten
						if (taste1 == 1):
							# USB Modus einschalten
							usbmodus = 1
							print ("Eingang 1")
							subprocess.call(["mpc", "play", str(auswahl2)])
							taste1 = 0   #Taste zuruecksetzen
							time.sleep(0.01)
						elif (taste2 == 1):
							print ("Eingang 2")
							auswahl2=auswahl2-1
							# Wenn MP3-Anfang erreicht ist, wieder auf MP3-Ende springen
							if (auswahl2 == 0):
								auswahl2 = anzahl_mp3
							taste2 = 0   #Taste zuruecksetzen
							time.sleep(0.01)
						elif (taste3 == 1):
							print ("Eingang 3")
							auswahl2=auswahl2+1
							# Wenn MP3-Ende erreicht ist, wieder auf MP3-Anfang springen
							if (auswahl2 == (anzahl_mp3+1)):
								auswahl2 = 1
							taste3 = 0   # Taste zuruecksetzen
							time.sleep(0.01)
						elif (taste4 == 1):
							print ("Eingang 4")
							taste4 = 0   #Taste zuruecksetzen
							time.sleep(0.01)
							abbruch3 = 1
					abbruch3 = 0
					time.sleep(0.01)
					# Optionsmenue wieder herstellen
					display_erase()
					lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
					lcd_string("  "+chr(5)+"    "+chr(7)+"    "+chr(4)+"    "+chr(6))
					# Altes Menue anzeigen
					Optionsmenue()
			# Im Optionsmenue eins rauf gehen
			elif (taste3 == 1):
				print ("Eingang 3")
				print (auswahl)
				auswahl_menu = auswahl_menu - 1
				if (auswahl_menu < 0):
					auswahl_menu = laenge_menu
				print (auswahl_menu)
				# Neues Menue anzeigen
				Optionsmenue()
				taste3 = 0   # Taste zuruecksetzen
				time.sleep(0.01)
			# Aus dem Optionsmenue wieder in den Radiomodus wechseln
			elif (taste4 == 1):
				print ("Eingang 4")
				print (auswahl)
				taste4 = 0   # Taste zuruecksetzen
				abbruch2 = 1
				# Falls USB-Modus noch gewaehlt ist
				if (usbmodus == 1):
					subprocess.call(["mpc", "stop"])
					subprocess.call(["mpc", "clear"])
					subprocess.call(["mpc", "load", "radiosender"])
					usbmodus = 0				
				# Menue zuruecksetzen
				display_erase()
				lcd_byte(DISPLAY_LINE_1, DISPLAY_CMD)
				lcd_string("  "+chr(0)+"    "+chr(1)+"    "+chr(2)+"    "+chr(3))
				time.sleep(0.01)
# mpd beenden
subprocess.call(["mpc", "stop"])

# Display Beleuchtung ausschalten
IO.output(ausgang4, IO.LOW)

# LED ausschalten
IO.output(ausgang1, IO.LOW)
IO.output(ausgang2, IO.LOW)
IO.output(ausgang3, IO.LOW)

# LCD-Anzeige loeschen
display_erase()

# Debug-Modus
print ("Debug-Modus")
