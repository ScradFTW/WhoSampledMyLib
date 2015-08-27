import sys
from WhoSampledScraper import WhoSampledScraper

print sys.argv[1]

wss = WhoSampledScraper(sys.argv[1])

print wss.artistName + " " + wss.songTitle
print "-------------------------------------------"

sampleList = wss.getSongsSampled()

if sampleList == None:
    print "The sample list could not be found"
    sys.exit()

for song in sampleList:
    print song

sampleList = wss.getWhoSampled()

if sampleList == None:
    print "The sample list could not be found"
    sys.exit()

for song in sampleList:
    print song
