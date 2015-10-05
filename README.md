# Extract YouTube MPD Information
A Python script to extract youtubes MPD file and print the information to the console

## Requirements
 * (Linux)
 * Python 2.7 or better
 * libxml2 (e.g., sudo apt-get install python-libxml2)
 * urllib2

## Usage
Example Call (will download the MPD file to aspen.mpd)

	python extract.py https://www.youtube.com/watch?v=GTGUa4J8XKw aspen.mpd

Output (of the above Example, URLs shortened/anonymized):

> Downloading HTML of https://www.youtube.com/watch?v=GTGUa4J8XKw
Extracted MPDURL from HTML: 
https://manifest.googlevideo.com/api/manifest/dash/sparams/.....
AdaptationSet,RepresentationID,Bitrate,Codec,ExtraInformation
audio/mp4,140,127570,mp4a.40.2
video/mp4,133,247800,avc1.4d4015,426/240/24
video/mp4,134,601944,avc1.4d401e,640/360/24
video/mp4,135,1103336,avc1.4d401e,854/480/24
video/mp4,160,109967,avc1.42c00c,256/144/12
video/mp4,136,2206969,avc1.4d401f,1280/720/24
video/mp4,137,4144774,avc1.640028,1920/1080/24


## Output Information
MPDs usually contain multiple ```AdaptationSet``` XML tags. Those contain a ```MimeType``` of either:

 * audio/mp4
 * audio/webm
 * video/mp4
 * video/webm

Within one ```AdaptationSet``` there are multiple ```Representation``` tags, which then contain information for each representation:

 * Bitrate (in Kilobit per second)
 * Codec
 * Information for Video Only (in ExtraInformation column of generated output):
 --* Video Width
 --* Video Height
 --* Video Frame Rate



## Acknowledgements
This work was partly funded by the **Austrian Science Fund (FWF)** under the CHIST-ERA project **CONCERT** (A Context-Adaptive Content Ecosystem Under Uncertainty), project number _I1402_ (see [http://www.concert-project]() for more details).
