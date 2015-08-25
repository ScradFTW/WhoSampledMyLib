"""
File: WhoSampledScraper.py
Author: Brad Jobe
Version: 1.1

Scrapes relevant HTML content from an artist's track page

Current problems:
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
    SONGS_SAMPLED = 0
    WHO_SAMPLED = 2

    whoSampledPath = None
    artistName = None
    songTitle = None
    sampleList = []
    whoSampledHTML = None


    def __init__(self, songLoc):
        songfile = eyed3.load(songLoc)

        try:
            self.artistName = songfile.tag.artist
            self.songTitle = songfile.tag.title

            if self.artistName == None or self.songTitle == None:
                raise MissingTagException()
        except MissingTagException:
            print "audiofile at " + songLoc + " has missing tag information"

        self.whoSampledPath = ("/" + self.artistName + "/" + \
                             self.songTitle + "/").replace(" ", "-")


    def getSongsSampled(self):
        return self.sampleScraper(self.artistName, self.songTitle, \
                                  "songsSampled")


    def getWhoSampled(self):
        return self.sampleScraper(self.artistName, self.songTitle, \
                                  "whoSampled")


    def getHTMLFromPath(self):
        urlCheck = urllib2.urlopen(self.HTTP_PROTO + \
                        self.URL_WHOSAMPLED + \
                        self.whoSampledPath)
        try:
            if urlCheck.geturl().lower() != (self.HTTP_PROTO + \
                            self.URL_WHOSAMPLED + \
                            self.whoSampledPath).lower():
                raise RedirectException()

        except RedirectException:
            print "The URL of " + self.songTitle + " by " + self.artistName + \
                " was redirected."
            return None

        return urlCheck.read()

    def sampleScraper(self, artistName, songTitle, calltype):
        if self.whoSampledHTML == None:
            self.whoSampledHTML = self.getHTMLFromPath()

        if self.whoSampledHTML== None:
            return None

        splitHTML = self.whoSampledHTML.split("<span Was sampled")

        if calltype == "songsSampled":
            whoSampledDoc = html.document_fromstring( \
                    splitHTML[self.SONGS_SAMPLED])

        elif calltype == "whoSampled":
            whoSampledDoc = html.document_fromstring( \
                    splitHTML[self.WHO_SAMPLED])

        artistNamesSamples = whoSampledDoc.find_class("trackArtist")
        songTitlesSamples = whoSampledDoc.find_class("trackName")

        if len(artistNamesSamples) != len(songTitlesSamples) \
                or len(artistNamesSamples) < 1:
                return None

        for i in range(0, len(artistNamesSamples)):
            self.sampleList.append( \
                    songTitlesSamples[i].text_content() + " " + \
                    artistNamesSamples[i].text_content())

        return self.sampleList


    def getStatusCode(self, host, path):
        conn = httplib.HTTPConnection(host)
        conn.request("HEAD", path)
        return str(conn.getresponse().status)


class RedirectException(Exception):
    pass


class MissingTagException(Exception):
    pass
