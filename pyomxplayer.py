import os
import pexpect
import re

from threading import Thread
from time import sleep

def omxplayer_parameter_exists(parameter_string):
    return bool(re.search("\s%s\s" % parameter_string.strip(), os.popen("/usr/bin/omxplayer").read()))

class OMXPlayer(object):

    _VIDEOPROP_REXP = re.compile(r".*Video codec ([\w-]+) width (\d+) height (\d+) profile (\d+) fps ([\d.]+).*", flags=re.MULTILINE)
    _AUDIOPROP_REXP = re.compile(r".*Audio codec (\w+) channels (\d+) samplerate (\d+) bitspersample (\d+).*", flags=re.MULTILINE)
    _STATUS_REXP = re.compile(r"(M:|V :)\s*([\d.]+).*")
    _DONE_REXP = re.compile(r"have a nice day.*")

    _LAUNCH_CMD = '/usr/bin/omxplayer -s %s %s'
    _PAUSE_CMD = 'p'
    _TOGGLE_SUB_CMD = 's'
    _QUIT_CMD = 'q'

    paused = False
    subtitles_visible = True
    position = 0

    def __init__(self, mediafile, args=None, fullscreen=True):
        if not args:
            args = ""
        
        if fullscreen:
            args += " -r"
            
        cmd = self._LAUNCH_CMD % (args, mediafile)
        
        self._process = pexpect.spawn(cmd)

        self.video = dict()
        self.audio = dict()

        headers = ""
        while "Video" not in headers or "Audio" not in headers:
            headers += self._process.readline()

        # Get video properties
        video_props = self._VIDEOPROP_REXP.search(headers).groups()
        self.video['decoder'] = video_props[0]
        self.video['dimensions'] = tuple(int(x) for x in video_props[1:3])
        self.video['profile'] = int(video_props[3])
        self.video['fps'] = float(video_props[4])

        # Get audio properties
        audio_props = self._AUDIOPROP_REXP.search(headers).groups()
        self.audio['decoder'] = audio_props[0]
        (self.audio['channels'], self.audio['rate'],
         self.audio['bps']) = [int(x) for x in audio_props[1:]]

        self._position_thread = Thread(target=self._get_position)
        self._position_thread.start()

        self.toggle_subtitles()

    def _get_position(self):
        
        while True:
            
            index = self._process.expect([
                self._STATUS_REXP,
                pexpect.TIMEOUT,
                pexpect.EOF,
                self._DONE_REXP
            ])
            
            if index == 1: # on timeout, keep going
                continue
            elif index in (2, 3): # EOF or finished
                break
            elif index == 0:
                self.position = float(self._process.match.group(2).strip()) / 1000000
        
            sleep(0.1)
            
            # print "POS: %0.2f" % self.position

    def pause(self):
        if not self.paused:
            self.toggle_pause()

    def play(self):
        if self.paused:
            self.toggle_pause()

    def toggle_pause(self):
        if self._process.send(self._PAUSE_CMD):
            self.paused = not self.paused

    def toggle_subtitles(self):
        if self._process.send(self._TOGGLE_SUB_CMD):
            self.subtitles_visible = not self.subtitles_visible

    def stop(self):
        self._process.send(self._QUIT_CMD)
        self._process.terminate(force=True)

    def set_subtitles(self, sub_idx):
        raise NotImplementedError

    def set_volume(self, volume):
        raise NotImplementedError

    def seek(self, minutes):
        raise NotImplementedError


