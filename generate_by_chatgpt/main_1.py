import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QProgressBar
from PyQt5.QtCore import pyqtSlot
from functions import process_files
from progress import ProgressMonitor

class EbookConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.choose_file_button = QPushButton('Choose Source File', self)
        self.choose_file_button.clicked.connect(self.choose_source_file)
        self.layout.addWidget(self.choose_file_button)

        self.choose_output_button = QPushButton('Choose Output Directory', self)
        self.choose_output_button.clicked.connect(self.choose_output_path)
        self.layout.addWidget(self.choose_output_button)

        self.convert_button = QPushButton('Start Conversion', self)
        self.convert_button.clicked.connect(self.convert_files_to_txt)
        self.layout.addWidget(self.convert_button)

        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)

        self.status_label = QLabel('Status: Ready', self)
        self.layout.addWidget(self.status_label)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('eBook Converter')

    @pyqtSlot()
    def choose_source_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Source File", "", "All Files (*);;PDF Files (*.pdf);;EPUB Files (*.epub)", options=options)
        if file_name:
            self.source_file = file_name
            self.status_label.setText(f'Source File: {file_name}')

    @pyqtSlot()
    def choose_output_path(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if folder:
            self.output_directory = folder
            self.status_label.setText(f'Output Directory: {folder}')

    @pyqtSlot()
    def convert_files_to_txt(self):
        if hasattr(self, 'source_file') and hasattr(self, 'output_directory'):
            self.status_label.setText('Converting...')
            self.progress_bar.setValue(0)
            # Placeholder for the conversion process
            # This should be replaced with the actual conversion logic
            process_files(self.source_file, self.output_directory, self.progress_bar, self.status_label)
        else:
            self.status_label.setText('Please select source file and output directory.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EbookConverter()
    ex.show()
    sys.exit(app.exec_())
