import queue

def check_conversion_progress(self, progress_queue):
        try:
            progress = progress_queue.get_nowait()  # 尝试从队列获取进度
            '''
            if isinstance(progress, str) and progress == "COMPLETED":
                self.progress_bar.setValue(self.progress_bar.maximum())  # 完成时设置进度条为最大值
                print("转换成功！")
                return  # 停止进度条更新
            '''
            if isinstance(progress, Exception):
                print(f"转换失败: {progress}")
            else:
                self.progress_bar.setValue(int(progress))  # Update progress bar
                if progress < 100:
                    QTimer.singleShot(1, lambda: self.check_conversion_progress(progress_queue))
                '''
                elif isinstance(progress, str) and progress == "COMPLETED":
                    self.progress_bar.setValue(self.progress_bar.maximum())  # 完成时设置进度条为最大值
                    print("转换成功！")
                    return  # 停止进度条更新
                '''
        except queue.Empty:
            # 如果队列为空，稍后再次检查
            QTimer.singleShot(1, lambda: self.check_conversion_progress(progress_queue))