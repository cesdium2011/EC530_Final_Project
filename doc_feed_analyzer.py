import os
import PyPDF2
import feedparser

def analyze_document(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError("The specified file path does not exist.")

    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        num_pages = pdf_reader.numPages
        text = ""

        for page_num in range(num_pages):
            page = pdf_reader.getPage(page_num)
            text += page.extractText()

    analysis_result = {
        'num_pages': num_pages,
        'text': text,
    }

    return analysis_result

def analyze_feed(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError("The specified file path does not exist.")

    with open(file_path, 'r') as feed_file:
        content = feed_file.read()
    
    feed = feedparser.parse(content)
    num_entries = len(feed.entries)

    titles = [entry.title for entry in feed.entries]
    links = [entry.link for entry in feed.entries]

    analysis_result = {
        'num_entries': num_entries,
        'titles': titles,
        'links': links,
    }

    return analysis_result
