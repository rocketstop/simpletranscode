#!/usr/bin/python

import os
import sys
import uuid
import shutil
import logging
import argparse
import subprocess
import ConfigParser

BASE_PATH = os.path.dirname(os.path.realpath(__file__))


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
        help='Path and filename of file to be transcoded.'
    )

    arguments = parser.parse_args()
    return arguments


def initConfig():
    config_filepath = os.path.join(BASE_PATH, 'simpletranscode.conf')

    if not os.path.exists(config_filepath):
        print 'Config file not found: %s' % config_filepath
        sys.exit(1)
    config = ConfigParser.SafeConfigParser()
    config.read(config_filepath)
    return config


def initLogging(config):

    fmt = '%%(asctime)s [%s] %%(message)s' % str(uuid.uuid4())[:6]
    logfile = os.path.join(BASE_PATH, config.get('Logging', 'log-filename'))

    logging.basicConfig(level=logging.INFO,
                        format=fmt,
                        filename=logfile)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def cleanup_and_exit(dest_video, video_path):
    if (os.path.exists(dest_video)):
        logging.info("Copying new over original: %s" % video_path)
        if (os.path.exists(video_path)):
            os.remove(video_path)
            shutil.copyfile(dest_video,video_path)
    logging.info('Completed processing.')


def main(config):

    if (os.path.exists(args.filename[0])):
        try:
            video_path = args.filename[0]
            original_video_dir = os.path.dirname(video_path)
            video_basename = os.path.basename(video_path)
            video_name, video_ext = os.path.splitext(video_basename)

            output_filename = video_name + ".mkv"
            dest_video = os.path.join(original_video_dir, output_filename)
            logging.info('Starting run on: %s' % video_path)
            logging.info('Source size: %s' % os.path.getsize(video_path))
            logging.info('Writing to: %s' % dest_video)

            FFMPEG_PATH = config.get('Dependencies', 'ffmpeg-path')
            logging.info('Using ffmpeg path: %s' % FFMPEG_PATH)

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
            logging.info('Transcode command: %s' % cmd)
            subprocess.call(cmd)
            logging.info('Transcode size: %s' % os.path.getsize(dest_video))
            cleanup_and_exit(dest_video, video_path)
            sys.exit(0)

        except Exception, e:
            logging.error('Something went wrong: %s' % e)
            sys.exit(1)

    else:
        logging.error('Unable to open filename, verify filename and path.')
        logging.error('Expected filename: %s ' % args.filename[0])
        sys.exit(1)


if __name__ == '__main__':
    config = initConfig()
    args = parse_arguments()
    initLogging(config)

    main(config)
