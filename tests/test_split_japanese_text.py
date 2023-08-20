import unittest

from dualang.split_japanese_text import split_japanese_text


class TestSplitJapaneseText(unittest.TestCase):
    def test_split_japanese_text(self):
        text = "今日はいい天気ですね！散歩に行きませんか？いいえ、忙しいです。"
        expected_output = ["今日はいい天気ですね！", "散歩に行きませんか？", "いいえ、忙しいです。"]
        self.assertEqual(split_japanese_text(text), expected_output)

        text_with_empty_line = "\n今日はいい天気ですね！\n"
        self.assertEqual(split_japanese_text(text_with_empty_line), ["今日はいい天気ですね！"])

        text_with_only_punctuation = "。"
        self.assertEqual(split_japanese_text(text_with_only_punctuation), [])

        # FAILURE: This test fails because the regex is not greedy enough
        text_with_no_punctuation = "今日はいい天気ですね散歩に行きませんかいいえ忙しいです"
        self.assertEqual(
            split_japanese_text(text_with_no_punctuation),
            ["今日はいい天気ですね散歩に行きませんかいいえ忙しいです"],
        )


if __name__ == "__main__":
    unittest.main()
