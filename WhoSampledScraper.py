"""
File: WhoSampledScraper.py
Author: Brad Jobe
Version: 1.0

Scrapes relevant HTML content from an artist's track page

Current problems:
    Doesn't handle redirects properly
    Doesn't find other sample info about a track
    need to cache already found track titles
    Code needs to be better formatted
"""
import sys
import eyed3
import urllib2
from lxml import html

class WhoSampledScraper:

    URL_WHOSAMPLED = "http://www.whosampled.com"

    artistName = None
    songTitle = None
    whoSampledURL = None
    sampleList = []

    def __init__(self, songLoc):
        songfile = eyed3.load(songLoc)
        self.artistName = songfile.tag.artist
        self.songTitle = songfile.tag.title
        self.whoSampledURL = self.URL_WHOSAMPLED + \
                             ("/" + self.artistName + "/" + \
                             self.songTitle).replace(" ", "-")

    def getSongsSampled(self):
        return self.sampleScraper(self.artistName, self.songTitle, \
                                  "songsSampled")

    def getWhoSampled(self):
        return self.sampleScraper(self.artistName, self.songTitle, \
                                  "whoSampled")

    def sampleScraper(self, artistName, songTitle, calltype):
        whoSampledHTML = (urllib2.urlopen(self.whoSampledURL)).read()
        whoSampledDoc = html.document_fromstring(whoSampledHTML)

        if calltype == "songsSampled":
            artistNamesFromSamples = whoSampledDoc.find_class("trackArtist")
            songTitlesFromSamples = whoSampledDoc.find_class("trackName")
            if len(artistNamesFromSamples) != len(songTitlesFromSamples) \
                or len(artistNamesFromSamples) < 1:
                return None

            for i in range(0, len(artistNamesFromSamples)):
                self.sampleList.append( \
                        songTitlesFromSamples[i].text_content() + " " + \
                        artistNamesFromSamples[i].text_content())

            return self.sampleList
