"""
Utilities.
"""

import os
import subprocess

BBB_FILE = "/opt/diss/videos/BigBuckBunny_320x180.mp4" # Big Buck Bunny
BBB_YOUTUBE_WEB_URL = "http://www.youtube.com/watch?v=YE7VzlLtp-4" # Big Buck Bunny
ED_YOUTUBE_WEB_URL = "http://www.youtube.com/watch?v=TLkA0RELQ1g" # Elephants Dream - Blender Foundation's first short Open Movie
S_YOUTUBE_WEB_URL = "http://www.youtube.com/watch?v=eRsGyueVLvQ" # Sintel - Third Open Movie by Blender Foundation
TOS_YOUTUBE_WEB_URL = "http://www.youtube.com/watch?v=R6MlUcmOul8" # Tears of Steel - Blender Foundation's fourth short Open Movie
GANGNAM_YOUTUBE_WEB_URL = "http://www.youtube.com/watch?v=9bZkp7q19f0" # PSY - GANGNAM STYLE

YOUTUBE_FORMATS = {
    "5" : "flv [240x400]",
    "17" : "mp4 [144x176]",
    "18" : "mp4 [360x640]",
    "22" : "mp4 [720x1280]",
    "34" : "flv [360x640]",
    "35" : "flv [480x854]",
    "37" : "mp4 [1080x1920]",
    "43" : "webm [360x640]",
    "44" : "webm [480x854]",
    "45" : "webm [720x1280]",
    "46" : "webm [1080x1920]",
    }

def killOMXPlayer():
    """
    Kill all running instances of OMXPlayer.
    """
    for i in range(0,3):
        os.system("kill `ps ax | grep omxplayer.bin | head -n 1 | awk '{print $1}'`")
        
def get_youtube_streaming_url(web_url,fmt):
    """
    Returns the url to stream a YouTube video using specified format.
    """
    output = subprocess.check_output(["youtube-dl","--get-url","--format",fmt,web_url])
    return output[:-1] # Remove new line character.

def get_best_youtube_streaming_url(web_url):
    """
    Returns the url to stream a YouTube video using the best quality streaming format.
    """
    return get_youtube_streaming_url(web_url,"best")

def get_low_q_youtube_streaming_url(web_url):
    """
    Returns the url to stream a YouTube video using a low quality format.
    """
    return get_youtube_streaming_url(web_url,"18") # Use mp4 [360x640]

def is_omxplayer_running():
    """
    Returns whether there is an running instance of OMXPlayer.
    """
    return len(subprocess.check_output("ps ax | grep omxplayer.bin",shell=True).splitlines()) > 2