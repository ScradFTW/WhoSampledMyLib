"""
File: WhoSampledScraper
Author: Brad Jobe
Version: 1.0

Scrapes relevant HTML content from an artist's track page
"""

import sys
import eyed3
import urllib2
from lxml import html

SONG_ARG = sys.argv[1];
URL_WHOSAMPLED = "http://www.whosampled.com"

songfile = eyed3.load(SONG_ARG)

artistName = songfile.tag.artist
songTitle = songfile.tag.title

print "\nArtist: " + artistName
print "Track: " + songTitle

artistName = artistName.replace(" ", "-")
songTitle = songTitle.replace(" ", "-")

whoSampledURL = URL_WHOSAMPLED + "/" + artistName + "/" + songTitle

whoSampledHTML = (urllib2.urlopen(whoSampledURL)).read()
whoSampledDoc = html.document_fromstring(whoSampledHTML)

artistNamesFromSamples = whoSampledDoc.find_class("trackArtist")
songNamesFromSamples = whoSampledDoc.find_class("trackName")

print "-----------------------------------------"

if len(songNamesFromSamples) == 0:
    print "No samples were found for the given track"
else:
    print "Samples:"
    for i in range(0, len(songNamesFromSamples)):
        print "\t" + songNamesFromSamples[i].text_content()
        print "\t" + artistNamesFromSamples[i].text_content()
