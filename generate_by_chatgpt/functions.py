# functions.py
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import os
import PyPDF2
import threading
from config import DEBUG_V1_1, MAC_DEBUG, WIN_DEBUG


# 开启子进程进行文件转换
def convert_file_to_txt_threaded(file_path, output_file_path, file_type, max_size, progress_queue, completed_files):
    threading.Thread(target=convert_file_to_txt, args=(
        file_path, output_file_path, file_type, max_size, progress_queue, completed_files)).start()


def process_files(source_path, output_path, max_size, progress_queue, completed_files):
    file_paths = traverse_directory(source_path) if determine_source_type(source_path) == "folder" else [source_path]

    sorted_files = sort_files(file_paths)

    for index, file_path in enumerate(sorted_files):
        file_type = determine_file_type(file_path)
        if file_type is not None:
            convert_file_to_txt_threaded(file_path, output_path, file_type, max_size, progress_queue, completed_files)


# 文件/文件夹相关操作：排序，遍历，判定类型
def traverse_directory(directory_path):
    file_paths = []
    for root, dirs, files in os.walk(directory_path):
        # 如果根目录是EPUB文件，则将整个EPUB文件作为单个文件添加
        if determine_file_type(root) == 'epub':
            file_paths.append(root)
            dirs[:] = []  # 不进入EPUB文件的内部
            continue
        for file in files:
            file_path = os.path.join(root, file)
            if determine_file_type(file_path):
                file_paths.append(file_path)
    return file_paths


def sort_files(file_paths):
    # 先过滤掉不是 epub 或 pdf 的文件，然后排序
    filtered_paths = filter(lambda x: determine_file_type(x) in ['epub', 'pdf'], file_paths)
    if DEBUG_V1_1:
        print("files:", file_paths)
    return sorted(filtered_paths, key=lambda x: x.lower())


def determine_source_type(source_path):
    if os.path.isdir(source_path):
        return "folder"
    elif os.path.isfile(source_path):
        return "file"
    else:
        return "unknown"


# 单个文件的操作
# 判定需要转换的文件类型
def determine_file_type(file_path):
    # 获取文件的扩展名
    _, ext = os.path.splitext(file_path)

    # 根据扩展名判断文件类型
    if ext.lower() == '.pdf':
        return 'pdf'
    elif ext.lower() == '.epub':
        return 'epub'
    else:
        return None  # 未知或不支持的文件类型


# 监测文件的大小，以免生成过大的文件
def check_file_size_and_split(text, current_size, output_file_index, max_size):
    text_size = len(text.encode('utf-8'))
    if current_size + text_size > max_size:
        output_file_index += 1
        current_size = 0  # 重置文件大小计数器
    current_size += text_size
    return current_size, output_file_index


# 将内容写入指定的文件
def write_text_to_file(text, file_path):
    with open(file_path, "a", encoding="utf-8") as txt_file:
        txt_file.write(text)


# 把不同类型的文件转换为txt
def convert_file_to_txt(file_path, output_file_path, file_type, max_size, progress_queue, completed_files):
    output_file_index = 0
    current_size = 0

    if file_type == "pdf":
        current_size, output_file_index = convert_pdf_to_txt(file_path, output_file_path,
                                                             output_file_index, current_size, max_size, progress_queue)
    elif file_type == "epub":
        current_size, output_file_index = convert_epub_to_txt(file_path, output_file_path,
                                                              output_file_index, current_size, max_size, progress_queue)
    progress_queue.put(('file_status', 1))


# 转换PDF到TXT的函数
def convert_pdf_to_txt(pdf_file_path, output_file_path, output_file_index, current_size, max_size,
                       progress_queue):
    try:
        file_name = os.path.splitext(os.path.basename(pdf_file_path))[0]
        with open(pdf_file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)

            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text = page.extract_text() if page.extract_text() else ''
                current_size, output_file_index = check_file_size_and_split(text, current_size,
                                                                            output_file_index, max_size)
                output_file_name = f"{output_file_path}/{file_name}-output-{output_file_index}.txt"
                write_text_to_file(text, output_file_name)

                progress = (page_num + 1) / num_pages * 100
                progress_queue.put(('progress_bar', progress))

    except Exception as e:
        print(f"转换PDF过程中发生错误: {e}")
        progress_queue.put(('progress_bar', -1))  # 使用特殊值指示错误
    else:
        progress_queue.put(('progress_bar', 100))  # 表示转换完成

    if DEBUG_V1_1:
        print("PDF文件已转换并保存在: ", output_file_name)
    return current_size, output_file_index


def convert_epub_to_txt(epub_file_path, output_file_path, output_file_index, current_size, max_size,
                        progress_queue):
    try:
        book = epub.read_epub(epub_file_path)
        items = [item for item in book.get_items() if item.get_type() == ebooklib.ITEM_DOCUMENT]
        total_items = len(items)
        file_name = os.path.splitext(os.path.basename(epub_file_path))[0]

        for index, item in enumerate(items):
            soup = BeautifulSoup(item.content, 'html.parser')
            text = soup.get_text()
            current_size, output_file_index = check_file_size_and_split(text, current_size,
                                                                        output_file_index, max_size)
            output_file_name = f"{output_file_path}/{file_name}-output-{output_file_index}.txt"
            write_text_to_file(text, output_file_name)

            progress = (index + 1) / total_items * 100
            progress_queue.put(('progress_bar', progress))

    except Exception as e:
        print(f"转换PDF过程中发生错误: {e}")
        progress_queue.put(('progress_bar', -1))  # 使用特殊值指示错误
    else:
        progress_queue.put(('progress_bar', 100))  # 表示转换完成
    if DEBUG_V1_1:
        print("PDF文件已转换并保存在: ", output_file_name)
    return current_size, output_file_index
