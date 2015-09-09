"""
File: WhoSampledScraper.py
Author: Brad Jobe
Version: 0.0.1

Scrapes relevant HTML content from an artist's track page
"""
import sys
import eyed3
import urllib2
from lxml import html
import httplib
import json

class WhoSampledScraper:

    URL_WHOSAMPLED = "www.whosampled.com"
    HTTP_PROTO = "http://"
    HTTP_REDIRECT = "3"
    SONGS_SAMPLED = 0
    WHO_SAMPLED = 2
    SONGS_SAMPLED_CALL = "songsSampled"
    WHO_SAMPLED_CALL = "whoSampled"

    def __init__(self, songLoc):
        """
        Parses a songfile for the artist and title ID3 tags and creates the
        theoretical path for the songfile's samplepage.

        Param: The directory path to a song file, as a string.
        Throws: MissingTagException if tag(s) could not be found.
        """
        songfile = eyed3.load(songLoc)

        try:
            self.whoSampledHTML = None
            self.artistName = songfile.tag.artist
            self.songTitle = songfile.tag.title
            self.sampleJSON = {}

            if self.artistName == None or self.songTitle == None:
                raise MissingTagException()
        except MissingTagException:
            print "audiofile at " + songLoc + " has missing tag information"

        self.whoSampledPath = ("/" + self.artistName + "/" + \
                             self.songTitle + "/").replace(" ", "-")
        self.sampleJSON[self.whoSampledPath] = { self.SONGS_SAMPLED_CALL:{}, \
                                                 self.WHO_SAMPLED_CALL: {} }

    def getSongsSampled(self):
        """
        Returns a list of songs that were sampled in the given track.
        """
        jsonSamples = self.sampleScraper(self.SONGS_SAMPLED_CALL)
        return self.convertJsontoList(jsonSamples)

    def getWhoSampled(self):
        """
        Returns a list of songs that have used the given track as a sample.
        """
        jsonSamples = self.sampleScraper(self.WHO_SAMPLED_CALL)
        return self.convertJsontoList(jsonSamples)

    def getHTMLFromPath(self):
        """
        Returns the html content from the song's sample page.

        Throws: RedirectException if the url is redirected away from the
                predicted path of the songs's sample page.
        """
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

    def sampleScraper(self, calltype):
        """
        Scrapes sample data from the song's sample page.

        Params: a string of specifying what type of sample data is to be
                scraped from the sample page.
        Returns: a list of song samples, as strings, or an empty list.
        """

        self.cachedSamples = self.loadCachedSampleData()

        try:
            self.cachedSamples[self.whoSampledPath] == None
        except KeyError:
            self.sampleJson = self.searchForSampleData(calltype)
        else:
            self.sampleJson = self.cachedSamples[self.whoSampledPath][calltype]

        return self.sampleJson

    def searchForSampleData(self, calltype):
        """
        loads html of artist's track page on WhoSampled.com and parses it for
        the relevant sample data.

        args: specific type of sample data to parse for
        returns: None if sample data could not be found, returns sample data
                 in json format if successful page parse
        """
        if self.whoSampledHTML == None:
            self.whoSampledHTML = self.getHTMLFromPath()

        if self.whoSampledHTML == None:
            return None

        splitHTML = self.whoSampledHTML.split("<span Was sampled")

        if calltype == self.SONGS_SAMPLED_CALL:
            whoSampledDoc = html.document_fromstring( \
                        splitHTML[self.SONGS_SAMPLED])

        elif calltype == self.WHO_SAMPLED_CALL and len(splitHTML) > 1:
            whoSampledDoc = html.document_fromstring( \
                                splitHTML[self.WHO_SAMPLED])
        elif len(splitHTML) <= 1:
            return None

        artistNamesSamples = whoSampledDoc.find_class("trackArtist")
        songTitlesSamples = whoSampledDoc.find_class("trackName")

        if len(artistNamesSamples) != len(songTitlesSamples) \
                    or len(artistNamesSamples) < 1:
            return None

        for i in range(0, len(artistNamesSamples)):
            a = artistNamesSamples[i].text_content()
            s = songTitlesSamples[i].text_content()
            self.sampleJSON[self.whoSampledPath][calltype][a] = s

        self.cacheSampleData()
        return self.sampleJSON


    def loadCachedSampleData(self):
        """
        loads stored sample data from previous lookups

        returns: json sample data
        """

        with open("samples.json", "r") as inSampleFile:
             jsonData = json.load(inSampleFile)

        inSampleFile.close()

        return jsonData

    def cacheSampleData(self):
        """
        stores sample data that has not been previously cached
        """

        self.cachedSamples[self.whoSampledPath] \
                        = self.sampleJSON[self.whoSampledPath]

        with open('samples.json', 'w') as outSampleFile:
                json.dump(self.cachedSamples, outSampleFile)

        outSampleFile.close()

    def convertJsontoList(self, jsonSampleData):
        """
        converts JSON sampled data to a python list

        args: json to be converted
        returns: python list of converted data
        """
        sampleList = []
        sampleDict = jsonSampleData

        if bool(sampleDict) == False:
            return None

        for key in sampleDict:
            sampleList.append(str(sampleDict[key]) + " " + str(key))

        return sampleList

class RedirectException(Exception):
    pass


class MissingTagException(Exception):
    pass
