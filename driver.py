import sys
from WhoSampledScraper import WhoSampledScraper

print sys.argv[1]

wss = WhoSampledScraper(sys.argv[1])

print wss.artistName + " " + wss.songTitle
print "-------------------------------------------"

sampleList = wss.getSongsSampled()

print "-> Songs sampled in the track --"
if sampleList == None:
    print "The sample list could not be found"
else:
    for song in sampleList:
        print song

print "------------------------------------------\n"

print "->Songs that sample the track --"

sampleList = wss.getWhoSampled()

if sampleList == None:
    print "The sample list could not be found"
else:
    for song in sampleList:
        print song

print "------------------------------------------"
