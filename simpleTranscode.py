#!/usr/bin/python

import os
import sys
import uuid
import logging
import argparse
import subprocess

FFMPEG_PATH = '/usr/bin/ffmpeg'
LOG_PATH = os.path.dirname(os.path.realpath(__file__))
LOG_FILENAME = "transcode.log"


def parse_arguments():

    parser = argparse.ArgumentParser(
        description='''
            Utility to transcode a given video file using a configured group of
            settings. Meant to be used with Plex DVR in post-processing.
            '''
    )

    parser.add_argument(
        nargs=1,
        dest='filename',
        default=None,
        help='Path and filename of file containing matrix to be printed.'
    )

    arguments = parser.parse_args()
    return arguments


def initLogging():
    session_uuid = str(uuid.uuid4())
    fmt = '%%(asctime)-15s [%s] %%(message)s' % session_uuid[:6]
    logging.basicConfig(level=logging.INFO, format=fmt,
                        filename=os.path.join(LOG_PATH, LOG_FILENAME))
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def cleanup_and_exit(dest_video, video_path):
    if (os.path.exists(dest_video)):
        logging.info("Removing original: %s" % video_path)
        if (os.path.exists(video_path)):
            os.remove(video_path)
    logging.info('Completed processing.')


def main():
    initLogging()

    if (os.path.exists(args.filename[0])):
        try:
            video_path = args.filename[0]
            original_video_dir = os.path.dirname(video_path)
            video_basename = os.path.basename(video_path)
            video_name, video_ext = os.path.splitext(video_basename)

            output_filename = video_name + ".mkv"
            dest_video = os.path.join(original_video_dir, output_filename)
            logging.info('Starting run on: %s' % video_path)
            logging.info('Writing to: %s' % dest_video)

        except Exception, e:
            logging.error('Problem getting working paths: %s' % e)
            sys.exit(1)

        try:
            cmd = [FFMPEG_PATH, '-i', video_path,
                                '-c:v', 'libx264',
                                '-preset', 'medium',
                                '-b:v', '3000k',
                                '-c:a', 'ac3',
                                '-b:a', '384k',
                                dest_video]
            logging.info('[ffmpeg] Command: %s' % cmd)
            subprocess.call(cmd)
            cleanup_and_exit(dest_video, video_path)
            sys.exit(0)

        except Exception, e:
            logging.error('Something went wrong: %s' % e)
            sys.exit(1)

    else:
        logging.error('Unable to open filename, verify filename and path.')
        sys.exit(1)


if __name__ == '__main__':
    args = parse_arguments()
    main()
