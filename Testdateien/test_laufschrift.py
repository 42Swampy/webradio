# Test Laufschrift
eingabe = "abcdefghijklmnopqrstuvwxyz"
laenge = len(eingabe)
bereich = laenge - 19
for i in range(0,bereich):
	ausgabe_laufschrift = eingabe[i:(i+20)]
	print ausgabe_laufschrift
