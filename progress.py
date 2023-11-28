# progress.py
from queue import Queue
from config import DEBUG_V1_1, MAC_DEBUG, WIN_DEBUG

class ProgressMonitor:
    def __init__(self, update_ui_callback, total_files=0, completed_files=0):
        self.update_ui_callback = update_ui_callback
        self.total_files = total_files
        self.completed_files = completed_files
        self.progress_queue = Queue()

    def check_progress(self):
        # 处理队列中当前可用的消息
        while not self.progress_queue.empty():
            msg = self.progress_queue.get()
            if isinstance(msg, tuple) and len(msg) == 2:
                message_type, data = msg
                if message_type == 'progress_bar':
                    self.update_ui_callback('progress_bar', int(data))
                elif message_type == 'file_status':
                    self.completed_files += 1
                    if DEBUG_V1_1:
                        print('self.completed_files', self.completed_files)
                    self.update_ui_callback('file_status', f"转换文件: {self.completed_files}/{self.total_files}")

        # 检查是否所有文件都已处理完毕
        if self.completed_files == self.total_files:
            self.update_ui_callback('completed', None)
        return self.completed_files, self.total_files
