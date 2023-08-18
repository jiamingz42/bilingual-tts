import os
import unittest
import tempfile

from dualang.subtitle_loader import load_subtitle_file, Subtitle


class TestSubtitleLoader(unittest.TestCase):
    def test_load_srt_file(self):
        srt_content = "1\n00:00:01,000 --> 00:00:02,000\nThis is a test."
        with tempfile.NamedTemporaryFile(suffix=".srt", delete=False) as temp:
            temp.write(srt_content.encode())
            temp.close()
            subtitles = load_subtitle_file(temp.name)
            self.assertIsInstance(subtitles, list)
            self.assertEqual(subtitles[0].start, 1000)
            self.assertEqual(subtitles[0].end, 2000)
            self.assertEqual(subtitles[0].text, "This is a test.")
            os.remove(temp.name)

    def test_load_ass_file(self):
        ass_content = "[Events]\nDialogue: 0,0:00:01.00,0:00:02.00,Default,,0,0,0,,This is a test."
        with tempfile.NamedTemporaryFile(suffix=".ass", delete=False) as temp:
            temp.write(ass_content.encode())
            temp.close()
            subtitles = load_subtitle_file(temp.name)
            self.assertIsInstance(subtitles, list)
            self.assertEqual(subtitles[0].start, 1000)
            self.assertEqual(subtitles[0].end, 2000)
            self.assertEqual(subtitles[0].text, "This is a test.")
            os.remove(temp.name)

    def test_load_vtt_file(self):
        vtt_content = "00:00:01.000 --> 00:00:02.000\nThis is a test."
        with tempfile.NamedTemporaryFile(suffix=".vtt", delete=False) as temp:
            temp.write(vtt_content.encode())
            temp.close()
            subtitles = load_subtitle_file(temp.name)
            self.assertIsInstance(subtitles, list)
            self.assertEqual(subtitles[0].start, 1000)
            self.assertEqual(subtitles[0].end, 2000)
            self.assertEqual(subtitles[0].text, "This is a test.")
            os.remove(temp.name)

if __name__ == '__main__':
    unittest.main()
