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
        ass_content = """
        [Script Info]
        Title: Default Aegisub file
        ScriptType: v4.00+
        WrapStyle: 0
        ScaledBorderAndShadow: yes
        YCbCr Matrix: None

        [Aegisub Project Garbage]

        [V4+ Styles]
        Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
        Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1

        [Events]
        Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
        Dialogue: 0,0:00:01.00,0:00:02.00,Default,,0,0,0,,This is a test.
        """
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
        vtt_content = "WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nThis is a test."
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
