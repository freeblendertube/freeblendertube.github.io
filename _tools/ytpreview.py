#!/usr/bin/python3

# sudo pip3 install...
# from __future__ import unicode_literals
# import youtube_dl

import sys
import os
import subprocess
import argparse
import glob
import math
import re

import json
from collections import OrderedDict
import io

home = os.path.dirname(os.path.realpath(__file__))

height = 120
columns = 10
rows = 10

def get_url_and_title():
    with open("2011-05-26-60 Snap and AlignTools.md") as search:
        url = ''
        for line in search:
            if re.search('video_link:', line):
                url = line.rstrip()
        url = url.split('video_link:')[1].lstrip()
        print(url)

    cmd = ['youtube-dl', '--skip-download', '--get-title', str(url)]
    text = subprocess.check_output(cmd).decode('utf-8').strip()
    text = text.replace(' - ', '-')
    text = text.replace(' ', '-')
    text = ''.join(c for c in text if c.isalnum() or c =='-' or c =='_')
    video_title = text.lower()
    if not os.path.exists(video_title):
        os.makedirs(video_title)


def download_video(download_url):
    video_out = 'video.mp4'
    cmd = ['youtube-dl', '-e', '-f', '134', '-o', 'video.mp4', 'https://www.youtube.com/watch?v=VmRqlsuSvsw']

    # download the video
    subprocess.call(cmd)

    '''
    # Get video meta info and then download using youtube-dl

    ydl_opts = {}

    # get meta info from the video
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(download_url, download=False)

    # renaming the file
    # remove special characters from the file name
    print('meta[title]=%s' %meta['title'])
    out = ''.join(c for c in meta['title'] if c.isalnum() or c =='-' or c =='_' )
    print('out=%s' %out)
    extension = meta['ext']
    video_out = out + '.' + extension
    print('video_out=%s' %video_out)
    videoSize = 'bestvideo[height<=540]+bestaudio/best[height<=540]'
    cmd = ['youtube-dl', '-f', videoSize, '-k', '-o', video_out, download_url]
    print('cmd=%s' %cmd)

    # Sometimes output file has format code in name such as 'out.webm'
    # So, when the best output format happens to be mp4, for example, 'out.webm.mp4'
    # which is the input file for iframe_extract(). But there is no 'out.webm.mp4' any more.
    # The following will reset the input as the newly merged video output, 'out.webm.mp4'
    found = False
    extension_list = ['mkv', 'mp4', 'webm']
    for e in extension_list:
       glob_str = '*.' + e
       for f in glob.glob(glob_str):
          if out in f:
             if os.path.isfile(f):
                video_out = f
                found = True
                break
       if found:
          break

    # call iframe-extraction : ffmpeg
    print('before iframe_extract() video_out=%s' %video_out)
    iframe_extract(video_out)
    return meta
    '''
    extract_preview(video_out)

def extract_preview(videoFile):
    count_frames_cmd = """ffmpeg -nostats -i video.mp4 -vcodec copy -f rawvideo -y /dev/null 2>&1 | grep frame | awk '{split($0,a,"fps")}END{print a[1]}' | sed 's/.*= *//'"""
    ps = subprocess.Popen(count_frames_cmd, shell=True, stdout=subprocess.PIPE)
    frames = ps.communicate()[0].decode('utf-8').strip()
    nth_frame = math.floor(int(frames) / 100)
    print('extract every ' + str(nth_frame) + ' frames')

    extract_frames_cmd = ['ffmpeg', '-loglevel', 'panic', '-y', '-i', 'video.mp4', '-frames', '1', '-q:v', '1', '-vf', 'select=not(mod(n\,'+str(nth_frame)+')),scale=-1:'+str(height)+',tile='+str(columns)+'x'+str(rows), 'video_preview.jpg']
    subprocess.call(extract_frames_cmd)

    '''
    # Move the extracted iframes to a subfolder
    # imgPrefix is used as a subfolder name that stores iframe images
    cmd = MKDIR + '-p ' + imgPrefix
    os.system(cmd)
    print("make subdirectoy=%s" %cmd)
    mvcmd = MOVE + imgPrefix + '*.png ' + imgPrefix
    print("moving images to subdirectoy %s" %mvcmd)
    os.system(mvcmd)
    '''

def check_arg(args=None):

# Command line options
# Currently, only the url option is used

    parser = argparse.ArgumentParser(description='download video')
    parser.add_argument('-u', '--url',
                        help='video url',
                        required='True')

    results = parser.parse_args(args)
    return (results.url)


# Usage sample:
#    syntax: python iframe_extract.py -u url
#    (ex) python iframe_extract.py -u https://www.youtube.com/watch?v=dP15zlyra3c

if __name__ == '__main__':
    u = check_arg(sys.argv[1:])
    get_url_and_title()
    # meta = download_video(u)
    # extract_preview('video.mp4')
