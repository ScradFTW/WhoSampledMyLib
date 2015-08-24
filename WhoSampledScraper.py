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
import httplib

class WhoSampledScraper:

    URL_WHOSAMPLED = "www.whosampled.com"
    HTTP_PROTO = "http://"
    HTTP_REDIRECT = "3"

    whoSampledPath = None
    artistName = None
    songTitle = None
    sampleList = []

    def __init__(self, songLoc):
        songfile = eyed3.load(songLoc)
        self.artistName = songfile.tag.artist
        self.songTitle = songfile.tag.title
        self.whoSampledPath = ("/" + self.artistName + "/" + \
                             self.songTitle).replace(" ", "-")
    def getSongsSampled(self):
        return self.sampleScraper(self.artistName, self.songTitle, \
                                  "songsSampled")

    def getWhoSampled(self):
        return self.sampleScraper(self.artistName, self.songTitle, \
                                  "whoSampled")


    def sampleScraper(self, artistName, songTitle, calltype):
        try:
            if self.getStatusCode(self.URL_WHOSAMPLED, self.whoSampledPath)[0] \
                == self.HTTP_REDIRECT:
                    raise RedirectException()
        except RedirectException:
            print "The URL to " + self.songTitle + " by " + \
                    artistName + " was redirected."

        whoSampledHTML = (urllib2.urlopen(self.HTTP_PROTO + \
                          self.URL_WHOSAMPLED + \
                          self.whoSampledPath)).read()

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

    def getStatusCode(self, host, path):
        conn = httplib.HTTPConnection(host)
        conn.request("HEAD", path)
        return str(conn.getresponse().status)

class RedirectException(Exception):
    pass
