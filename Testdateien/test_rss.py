#! /usr/bin/python
# -*- coding: utf-8 -*-
#

# Test von feedparser
import os
import feedparser
import time


# Deklarieren der Variabeln
ganzer_feed = ""

# Feed herunterladen
print ("Lade RSS-Feed")
d=feedparser.parse("http://rss.kicker.de/news/2bundesliga")
print ("RSS-Feed geladen")

# Titel als erstes
ganzer_feed = ganzer_feed+(d.feed.title)+" --- "

# Die Feeds danach
for i in range(len(d['entries'])):   # Anzahl der Eintraege: len(d['entries'])
	ganzer_feed = ganzer_feed+(d.entries[i].title)+" --- "
	
print (ganzer_feed)
