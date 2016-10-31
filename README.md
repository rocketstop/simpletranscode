# simpletranscode

A simple tool for post-process transcoding recorded video in Plex DVR.

## Requires:
ffmpeg

## Tested with:
python 2.7

ubuntu 14.04

## To use:
Keep simpleTranscode and simpleTranscode.py in the same directory. Ensure that the
plex user (the user that Plex is running as) has access to that directory. If the
current path to ffmpeg (/usr/bin/ffmpeg) is not correct, edit the line that sets
FFMPEG_PATH in simpleTranscode.py.

In the Plex DVR setup for post-processing, supply the full path to the simpleTranscode script.

## What it does:
Using some basic settings, uses ffmpeg in post-processing to transcode the file produced
by OTA cards (.ts in my case, I use a HDHomerun Connect) to moderately-sized .mkvs with ac3
audio. Records the 'run' by appending to run.txt and records log results to transcode.log.
It then removes the original video file, so Plex will copy the new file into the media
library.

## Caveats:
Lightly tested

The two log files that this script produces will currently always be written.

## TODO:
Edit to produce a 'quiet' option with no log output.

Configuration file.

Add a few different options for transcode quality.
