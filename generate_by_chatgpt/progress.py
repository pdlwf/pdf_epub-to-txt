from PyQt5.QtCore import QObject, pyqtSignal

class ProgressMonitor(QObject):
    # Signal to indicate progress update
    progress_updated = pyqtSignal(int)
    # Signal to indicate completion or error
    status_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.total_files = 0
        self.completed_files = 0

    def set_total_files(self, total):
        self.total_files = total

    def update_progress(self):
        """
        Update the progress of the file conversion process.
        """
        self.completed_files += 1
        progress = int((self.completed_files / self.total_files) * 100)
        self.progress_updated.emit(progress)
        if self.completed_files == self.total_files:
            self.status_changed.emit('Conversion Completed')

    def reset_progress(self):
        """
        Reset the progress monitor to its initial state.
        """
        self.total_files = 0
        self.completed_files = 0
        self.progress_updated.emit(0)
        self.status_changed.emit('Ready')

    def report_error(self, message):
        """
        Report an error in the conversion process.
        """
        self.status_changed.emit(f'Error: {message}')
