"""Tests for quilt-tts."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import unittest

from quilt_tts.core import speak_lore, list_voices


class TestSpeak(unittest.TestCase):

    def test_works_without_api_key(self):
        """Without ELEVENLABS_TOKEN, returns error."""
        os.environ.pop("ELEVENLABS_TOKEN", None)
        r = speak_lore("test")
        self.assertIn("_error", r)


class TestLive(unittest.TestCase):

    @unittest.skipUnless(os.environ.get("ELEVENLABS_TOKEN"), "ELEVENLABS_TOKEN not set")
    def test_real_speak(self):
        """Live API test."""
        import tempfile
        tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        tmp.close()
        r = speak_lore("Hello, world. The substrate walks.", output_path=tmp.name)
        self.assertNotIn("_error", r)
        self.assertGreater(r["size_bytes"], 1000)
        os.unlink(tmp.name)


if __name__ == "__main__":
    unittest.main()
