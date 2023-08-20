import re


def split_japanese_text(text):
    # Check if there are any Japanese punctuation marks in the text
    if not re.search(r'。|！|？', text):
        return [text.strip()] if text.strip() else []


    # Split the text based on common Japanese punctuation marks, but preserve the delimiters
    sentences = re.split(r"(。|！|？)", text)

    # Combine each sentence with its trailing punctuation mark, and filter out empty strings
    sentences = [
        sentences[i].strip() + sentences[i + 1].strip()
        for i in range(0, len(sentences) - 1, 2)
        if sentences[i].strip()
    ]

    return sentences
