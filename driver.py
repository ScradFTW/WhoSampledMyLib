import sys
from WhoSampledScraper import WhoSampledScraper

wss = WhoSampledScraper(sys.argv[1])

print wss.artistName + " " + wss.songTitle
print "-------------------------------------------"

sampleList = wss.getSongsSampled()

for song in sampleList:
    print song
