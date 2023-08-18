import os
import unittest
from dualang.subtitle_loader import load_subtitle_file, Subtitle

class TestSubtitleLoader(unittest.TestCase):
    def setUp(self):
        self.srt_file = 'tests/mock_files/mock.srt'
        self.ass_file = 'tests/mock_files/existing_mock.ass'
        self.vtt_file = 'tests/mock_files/mock.vtt'

    def test_load_srt_file(self):
        subtitles = load_subtitle_file(self.srt_file)
        self.assertIsInstance(subtitles, list)
        self.assertIsInstance(subtitles[0], Subtitle)

    def test_load_ass_file(self):
        subtitles = load_subtitle_file(self.ass_file)
        self.assertIsInstance(subtitles, list)
        self.assertIsInstance(subtitles[0], Subtitle)

    def test_load_vtt_file(self):
        subtitles = load_subtitle_file(self.vtt_file)
        self.assertIsInstance(subtitles, list)
        self.assertIsInstance(subtitles[0], Subtitle)

if __name__ == '__main__':
    unittest.main()
