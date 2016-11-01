# simpletranscode

A simple tool to post-process transcode recorded video in Plex DVR.

## Requires:
ffmpeg

## Tested with:
python 2.7

ubuntu 14.04

## To use:
Keep `simpleTranscode` and `simpleTranscode.py` in the same directory. Ensure that the
**plex** user (the user that Plex is running as) has access to that directory and those files.
Copy the example configuration file to `simpletranscode.conf`, modify the configuration file
if the path to ffmpeg is not correct.

In the Plex DVR setup for post-processing, supply the full path to the simpleTranscode script.
Find that setting in Settings > DVR (Beta) > DVR Settings > POSTPROCESSING SCRIPT

## What it does:
Using some basic settings, uses ffmpeg in post-processing to transcode the file produced
by OTA recording devices (.ts in my case, I use a HDHomerun Connect) to moderately-sized
.mkv with ac3 audio. Records the 'run' by appending to run.txt and records log results to
transcode.log. It then removes the original video file, so Plex will copy the new file
into the media library.

## Caveats:
Lightly tested

Currently, the two log files that this script produces will always be written.

## TODO:
Edit to produce a 'verbose' option for log output, with default set as no logging.

Add a few different options for transcode quality.

Better logging and error messages.

Workflow/Queue/Throttle? (If multiple recordings finish simultaneously).