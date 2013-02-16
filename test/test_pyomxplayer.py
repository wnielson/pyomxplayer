"""
Unit tests for the pyomxplayer module.

Tests can be run with unittest or nosetests,

- `python -m unittest --verbose --failfast pyomxplayer.test.pyomxplayer`
- `nosetests pyomxplayer.test.test_pyomxplayer:Test.test_play_stop_local_video`
"""

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

    stop_treshold = 2 # Maximum time allowed between calling stop and the OMXPlayer process being terminated. 

    # YouTube Video web urls.
    web_urls = [
        util.BBB_YOUTUBE_WEB_URL,
        util.ED_YOUTUBE_WEB_URL,
        util.S_YOUTUBE_WEB_URL,
        util.TOS_YOUTUBE_WEB_URL
    ]

    def test_play_stop_local_video(self):
        log.info("> test_play_stop_local_video")
        p = OMXPlayer(util.BBB_FILE)
        time.sleep(self.short_sleep)
        self.assertTrue(util.is_omxplayer_running(),"OMXPlayer should be running.")
        p.stop()
        time.sleep(self.stop_treshold)
        self.assertFalse(util.is_omxplayer_running(),"OMXPlayer should not be running.")
        log.info("< test_play_stop_local_video")

    def test_play_stop_youtube_video(self):
        """
        Tests playing and stopping YouTube videos.

        Checks that video is stopped within acceptable theshold.
        """

        log.info("> test_play_stop_youtube_video")

        for video_web_url in self.web_urls:
            p = OMXPlayer(util.get_best_youtube_streaming_url(video_web_url))
            time.sleep(5)
            self.assertTrue(util.is_omxplayer_running(),"OMXPlayer should be running.")
            p.stop()
            time.sleep(self.stop_treshold)
            self.assertFalse(util.is_omxplayer_running(),"OMXPlayer should not be running.")

        log.info("< test_play_stop_youtube_video")

    def test_pause_youtube_video(self):
        """
        Testing pausing YouTube videos.
        """

        log.info("> test_pause_youtube_video")

        for video_web_url in self.web_urls:
            p = OMXPlayer(util.get_best_youtube_streaming_url(video_web_url))
            time.sleep(self.short_sleep)
            p.toggle_pause()
            time.sleep(self.very_short_sleep)
            p.toggle_pause()
            time.sleep(self.short_sleep)
            self.assertTrue(util.is_omxplayer_running(),"OMXPlayer should be running.")

        log.info("< test_pause_youtube_video")

    @skip("")
    def test_interleaving_youtube_video(self):
        log.info("> test_interleaving_youtube_video")
        
        for i in range(0,2):
        
            p1 = OMXPlayer(util.get_best_youtube_streaming_url(util.S_YOUTUBE_WER_URL))
            time.sleep(self.short_sleep)
            p1.stop()
            p2 = OMXPlayer(util.get_best_youtube_streaming_url(util.TOS_YOUTUBE_WEB_URL))
            time.sleep(self.short_sleep)
            p2.stop()
        
        time.sleep(self.stop_treshold)
        self.assertFalse(util.is_omxplayer_running(),"OMXPlayer should not be running.")
        
        log.info("< test_interleaving_youtube_video")

    def test_change_volume(self):

        p = OMXPlayer(util.get_best_youtube_streaming_url(util.BBB_YOUTUBE_WEB_URL))

        time.sleep(5)

        for i in range(0,24):
            log.info("increasing volume")
            p.increase_volume()

        time.sleep(5)

        for i in range(0,49):
            log.info("decreasing volume")
            p.decrease_volume()

        time.sleep(5)

        for i in range(0,74):
            log.info("increasing volume")
            p.increase_volume()

        time.sleep(5)

        self.assertTrue(util.is_omxplayer_running(),"OMXPlayer should be running.")

    def test_set_volume(self):

        p = OMXPlayer(util.get_best_youtube_streaming_url(util.BBB_YOUTUBE_WEB_URL))

        time.sleep(5)

        # Test increase
        log.info("20 dB")
        p.set_volume(20)
        time.sleep(5)

        # Test decrease
        log.info("-20 dB")
        p.set_volume(-20)
        time.sleep(5)

        # Test extreme case - setting to 0
        log.info("0 dB")
        p.set_volume(0)
        time.sleep(5)

        # Test extreme case - no change
        log.info("0 dB")
        p.set_volume(0)
        time.sleep(5)

        # Test extreme case - not a multiple of 0.5
        log.info("20.125 dB")
        p.set_volume(20.125)
        time.sleep(5)

        self.assertTrue(util.is_omxplayer_running(),"OMXPlayer should be running.")

    def test_change_speed(self):

        p = OMXPlayer(util.get_best_youtube_streaming_url(util.BBB_YOUTUBE_WEB_URL))

        time.sleep(5)

        # Test increase
        log.info("increase by one")
        p.increase_speed()
        time.sleep(5)

        # Test increase
        log.info("increase by one")
        p.increase_speed()
        time.sleep(5)

        # Test increase
        log.info("increase by one")
        p.increase_speed()
        time.sleep(5)

        # Test increase
        log.info("increase by one")
        p.increase_speed()
        time.sleep(5)

        # Test decrease
        log.info("decrease by one")
        p.decrease_speed()
        time.sleep(5)

        # Test decrease
        log.info("decrease by one")
        p.decrease_speed()
        time.sleep(5)

        # Test decrease
        log.info("decrease by one")
        p.decrease_speed()
        time.sleep(5)

        # Test decrease
        log.info("decrease by one")
        p.decrease_speed()
        time.sleep(5)

        # Test decrease
        log.info("decrease by one")
        p.decrease_speed()
        time.sleep(5)

        # Test decrease
        log.info("decrease by one")
        p.decrease_speed()
        time.sleep(5)

        self.assertTrue(util.is_omxplayer_running(),"OMXPlayer should be running.")

    def test_set_speed(self):

        p = OMXPlayer(util.get_best_youtube_streaming_url(util.BBB_YOUTUBE_WEB_URL))

        time.sleep(10)

        log.info("fast")
        p.set_speed(OMXPlayer.FAST_SPEED)
        time.sleep(5)

        log.info("slow")
        p.set_speed(OMXPlayer.SLOW_SPEED)
        time.sleep(5)

        log.info("normal")
        p.set_speed(OMXPlayer.NORMAL_SPEED)
        time.sleep(5)

        # Extreme - making no change
        log.info("normal")
        p.set_speed(OMXPlayer.NORMAL_SPEED)
        time.sleep(5)

        # Erroneous
        log.info("0.5")
        with self.assertRaises(AssertionError):
            p.set_speed(0.5)

        # Erroneous
        log.info("half")
        with self.assertRaises(AssertionError):
            p.set_speed("half")

        time.sleep(5)

        self.assertTrue(util.is_omxplayer_running(),"OMXPlayer should be running.")
        
    def tearDown(self):
        """
        Terminates any running OMXPlayer processes that are still running.

        This is run after every test function.
        """
        log.info("> tearDown")
        util.killOMXPlayer()
        time.sleep(1)
        log.info("< tearDown")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()