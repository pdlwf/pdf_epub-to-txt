import os
import threading
from PyPDF2 import PdfReader
from ebooklib import epub
from progress import ProgressMonitor

def convert_pdf_to_txt(pdf_file_path, output_file_path):
    """
    Converts a PDF file to a TXT file.
    """
    reader = PdfReader(pdf_file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(text)

def convert_epub_to_txt(epub_file_path, output_file_path):
    """
    Converts an EPUB file to a TXT file.
    """
    book = epub.read_epub(epub_file_path)
    text = ""
    for doc in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        text += doc.get_body_content().decode("utf-8") + "\n"
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(text)

def process_file(file_path, output_dir, progress_monitor):
    """
    Processes a single file for conversion.
    """
    if file_path.lower().endswith('.pdf'):
        output_file_path = os.path.join(output_dir, os.path.basename(file_path) + '.txt')
        convert_pdf_to_txt(file_path, output_file_path)
    elif file_path.lower().endswith('.epub'):
        output_file_path = os.path.join(output_dir, os.path.basename(file_path) + '.txt')
        convert_epub_to_txt(file_path, output_file_path)
    # Update progress
    progress_monitor.update_progress()

def process_files(source_file, output_directory, progress_monitor):
    """
    Processes files in a given directory for conversion.
    """
    # Set total files count for progress monitoring
    progress_monitor.set_total_files(1)  # Assuming one file for simplicity

    # Start conversion in a new thread
    threading.Thread(target=process_file, args=(source_file, output_directory, progress_monitor)).start()
