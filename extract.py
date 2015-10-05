#!/usr/bin/env python
from __future__ import print_function

"""Extract the 'dashmpd' information from a youtube video, download and parse the mpd file and print the
representations that are listed in the mpd file"""

__author__ = "Christian Kreuzberger"
__copyright__ = "Copyright 2015, Christian Kreuzberger"
__licencse__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Christian Kreuzerger"
__email__ = "christian.kreuzberger@itec.aau.at"
__status__ = "Production"

'''This work was partially funded by the Austrian Science Fund (FWF) under the CHIST-ERA project CONCERT
(A Context-Adaptive Content Ecosystem Under Uncertainty), project number I1402.'''

'''
The MIT License
Copyright (c) 2015 Christian Kreuzberger, christian.kreuzberger@itec.aau.at
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''


import urllib2
import libxml2
import sys

def printStdErr(*objs):
    print(*objs, file=sys.stderr)


# parse input parameters
if len(sys.argv) < 2 or len(sys.argv) > 3:
    printStdErr("Usage: " + sys.argv[0] + " YoutubeURL [MPDOutputFilename]")
    printStdErr("\tExample: " + sys.argv[0] + " https://www.youtube.com/watch?v=GTGUa4J8XKw aspen.mpd")
    exit(1)

mpdoutfile = "video.mpd"


if len(sys.argv) == 2:
    yUrl = sys.argv[1]
elif len(sys.argv) == 3:
    yUrl = sys.argv[1]
    mpdoutfile = sys.argv[2]


printStdErr("Downloading HTML of " + yUrl)

f=urllib2.urlopen(yUrl)
html=f.read()

mpdurl = html[html.find("dashmpd"):]
mpdurl = mpdurl[mpdurl.find("\":")+3:]
mpdurl = mpdurl[0:mpdurl.find("\"")]
mpdurl = mpdurl.replace("\\/", "/")

printStdErr("Extracted MPDURL from HTML: ")
printStdErr(mpdurl)

downloadfile = urllib2.urlopen(mpdurl)
mpdstring = downloadfile.read()

# store to file
localmpdfile = open(mpdoutfile, "w")
localmpdfile.write(mpdstring)
localmpdfile.close()


# print adaptation set and representations


print("AdaptationSet,RepresentationID,Bitrate,Codec,ExtraInformation")


# parse MPD using libxml2
doc = libxml2.parseFile(mpdoutfile)

# assuming there is one period, containing multiple adaptation sets
periods = doc.get_children().get_children()
adaptationSet = periods.get_children()

# iterate over adaptation sets
while adaptationSet != None:
    adaptationSetType = None
    # get adaptation set type (based on mimetype)
    for prop in adaptationSet.properties:
        if prop.name == 'mimeType':
            adaptationSetType = prop.content

    # go over all childnodes, containing representation settings
    childNode = adaptationSet.get_children()
    while childNode != None:
        if childNode.get_name() == "Representation":
            # if this is a representation xml tag, check out all the type values
            for prop in childNode.properties:
                if prop.name == "id":
                    repId = prop.content
                elif prop.name == "bandwidth":
                    repBitrate = prop.content
                elif prop.name == "height":
                    repHeight = prop.content
                elif prop.name == "width":
                    repWidth = prop.content
                elif prop.name == "frameRate":
                    repFPS = prop.content
                elif prop.name == "codecs":
                    repCodec = prop.content
            # print representation information
            if "video" in adaptationSetType:
                print(adaptationSetType + "," + repId + "," + repBitrate + "," + repCodec + "," + repWidth + "/" +
                      repHeight + "/" + repFPS)
            elif "audio" in adaptationSetType:
                print(adaptationSetType + "," + repId + "," + repBitrate + "," + repCodec)
        # get next childnode (get next representation)
        childNode = childNode.get_next()

    # get next adaptation set
    adaptationSet = adaptationSet.get_next()

# done