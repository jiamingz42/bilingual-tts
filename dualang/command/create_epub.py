import os
import pysrt
from ebooklib import epub

def read_srt_files(directory):
    """Read all SRT files in a directory."""
    srt_files = [directory + '/' + f for f in os.listdir(directory) if f.endswith('.srt')]
    return sorted(srt_files)

def parse_srt_file(file_path):
    """Parse an SRT file and extract the subtitles."""
    subs = pysrt.open(file_path)
    for sub in subs:
        yield sub.text

def add_chapter(book, title, filename, content):
    chapter = epub.EpubHtml(title=title, file_name=filename, content=content)
    book.add_item(chapter)
    return chapter

def create_epub(subtitles, output, epub_title):
    book = epub.EpubBook()

    # set metadata
    book.set_identifier('id123456')
    book.set_title(epub_title)
    book.set_language('ja')

    chapters = []
    for i, subtitle in enumerate(subtitles):
        chapter_name = subtitle.split('.')[0].replace('_', ' ').replace('-', ' ').replace(' ja', '')

        # create chapter
        c1 = epub.EpubHtml(title=chapter_name, file_name=f"chap_{i:0d}.xhtml", lang="ja")
        c1.content = f"<h1>{chapter_name}</h1>"
        for line in  parse_srt_file(subtitle):
            c1.content += f"<p>{line}</p>"

        book.add_item(c1)

        chapters.append(c1)


    book.toc = (
        (epub.Section("Simple book"), chapters),
    )

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    style = "BODY {color: white;}"
    nav_css = epub.EpubItem(
        uid="style_nav",
        file_name="style/nav.css",
        media_type="text/css",
        content=style,
    )

    book.add_item(nav_css)

    book.spine = ["nav"] + chapters

    epub.write_epub(output, book)

import os
import sys

def create_epub_main(args):
    subtitles = sorted(read_srt_files(args.input_folder))

    # Ensure output file ends with .epub
    if not args.output.endswith('.epub'):
        args.output += '.epub'

    # Check if output file already exists
    if os.path.isfile(args.output):
        print(f"File {args.output} already exists. Do you want to overwrite it? [y/N]")
        choice = input().lower()
        if choice not in ['y', 'yes']:
            print("Aborted.")
            sys.exit(0)

    print(args.output)
    create_epub(subtitles, args.output, args.title)
