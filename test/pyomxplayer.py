'''
Unit tests for the pyomxplayer module.

Recommend to run with:

python -m unittest --verbose --failfast pyomxplayer.test.pyomxplayer
'''
import unittest
from unittest import skip
import time
import logging

from ..pyomxplayer import OMXPlayer
import util

logging.basicConfig(format="%(asctime)s - %(message)s",datefmt="%H:%M:%S",level=logging.INFO)
log = logging.getLogger(__name__)

class Test(unittest.TestCase):

    # Timings
    
    very_short_sleep = 1
    short_sleep = 5
    long_sleep = 30
    stop_time = 2 # Maximum time allowed between calling stop and the OMXPlayer process being terminated. 

    @unittest.skip("")
    def test_play_stop_local_video(self):
        log.info("> test_play_stop_local_video")
        p = OMXPlayer(util.BBB_FILE)
        time.sleep(self.short_sleep)
        self.assertTrue(util.is_omxplayer_running(),"OMXPlayer should be running.")
        p.stop()
        time.sleep(self.stop_time)
        self.assertFalse(util.is_omxplayer_running(),"OMXPlayer should not be running.")
        log.info("< test_play_stop_local_video")

    @unittest.skip("")
    def test_play_stop_youtube_video(self):
        log.info("> test_play_stop_youtube_video")
        p = OMXPlayer(util.get_best_youtube_streaming_url(util.BBB_YOUTUBE_WEB_URL))
        time.sleep(self.short_sleep)
        self.assertTrue(util.is_omxplayer_running(),"OMXPlayer should be running.")
        p.stop()
        time.sleep(self.stop_time)
        self.assertFalse(util.is_omxplayer_running(),"OMXPlayer should not be running.")
        log.info("< test_play_stop_youtube_video")

    @unittest.skip("")    
    def test_pause_youtube_video(self):
        log.info("> test_pause_youtube_video")
        p = OMXPlayer(util.get_best_youtube_streaming_url(util.BBB_YOUTUBE_WEB_URL))
        time.sleep(self.short_sleep)
        p.toggle_pause()
        time.sleep(self.very_short_sleep)
        p.toggle_pause()
        time.sleep(self.short_sleep)
        self.assertTrue(util.is_omxplayer_running(),"OMXPlayer should be running.")
        log.info("< test_pause_youtube_video")

    def test_interleaving_youtube_video(self):
        log.info("> test_interleaving_youtube_video")
        
        for i in range(0,2):
        
            p1 = OMXPlayer(util.get_best_youtube_streaming_url(util.S_YOUTUBE_WER_URL))
            time.sleep(self.short_sleep)
            p1.stop()
            p2 = OMXPlayer(util.get_best_youtube_streaming_url(util.TOS_YOUTUBE_WEB_URL))
            time.sleep(self.short_sleep)
            p2.stop()
        
        time.sleep(self.stop_time)
        self.assertFalse(util.is_omxplayer_running(),"OMXPlayer should not be running.")
        
        log.info("< test_interleaving_youtube_video")
        
    def tearDown(self):
        """
        Terminates any running OMXPlayer processes that are still running.
        """
        log.info("> tearDown")
        util.killOMXPlayer()
        log.info("< tearDown")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()