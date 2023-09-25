import os
import pysrt
from ebooklib import epub

def read_srt_files(directory):
    """Read all SRT files in a directory."""
    srt_files = [f for f in os.listdir(directory) if f.endswith('.srt')]
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

def create_epub(srt_files, directory, epub_title):
    """Create an EPUB file with a table of contents, where each chapter corresponds to a subtitle file."""
    book = epub.EpubBook()
    book.set_identifier('id123456')
    book.set_title(epub_title)
    book.set_language('ja')
    book.add_author("Author Authorowski")

    chapters = []
    for i, srt_file in enumerate(srt_files):
        chapter = epub.EpubHtml(title="intro", file_name=f'chap_{i}.xhtml', lang='en')
        chapter.content = "<h1>hi world</h1>"
        book.add_item(chapter)

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    epub.write_epub(epub_title + '.epub', book)

def create_epub_main(args):
    subtitles = sorted(read_srt_files(args.input_folder))
    create_epub(subtitles, args.input_folder, args.title)
