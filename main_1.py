import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QProgressBar, QFileDialog, QCheckBox
from PyQt5.QtCore import QTimer, pyqtSignal
import functions  # 您的 functions 模块
import queue


class EbookConverter(QWidget):
    update_progress_signal = pyqtSignal(int, int)  # 定义一个信号
    def __init__(self):
        super().__init__()
        self.progress_bar = QProgressBar()
        #self.file_type = QLabel()
        self.file_type = ""
        self.source_file_path_label = QLabel("源文件")
        self.output_file_path_label = QLabel("目标文件")
        self.file_status_label = QLabel("转换状态: 未开始")  # 添加状态标签
        self.update_progress_signal.connect(self.update_file_status)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("电子书转换工具")
        layout = QVBoxLayout()

        choose_source_file_button = QPushButton("选择源文件")
        choose_source_file_button.clicked.connect(self.choose_source_file)

        choose_output_path_button = QPushButton("选择输出路径")
        choose_output_path_button.clicked.connect(self.choose_output_path)

        '''
        epub_button = QPushButton("EPUB到TXT")
        epub_button.clicked.connect(self.convert_epub_to_txt)
        '''
        convertor_button = QPushButton("FILE到TXT")
        convertor_button.clicked.connect(self.convert_files_to_txt)

        layout.addWidget(QLabel("点击开始转换："))
        # layout.addWidget(epub_button)
        layout.addWidget(convertor_button)
        layout.addWidget(QLabel("请选择源文件："))
        layout.addWidget(self.source_file_path_label)
        layout.addWidget(choose_source_file_button)
        layout.addWidget(QLabel("设置目标输出路径："))
        layout.addWidget(self.output_file_path_label)
        layout.addWidget(choose_output_path_button)
        layout.addWidget(self.progress_bar)

        layout.addWidget(QLabel("转换状态："))
        layout.addWidget(self.file_status_label)  # 将状态标签添加到布局中
        
        self.setLayout(layout)

    
    def choose_source_file(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setOption(QFileDialog.ReadOnly, True)
        dialog.setOption(QFileDialog.ShowDirsOnly, False)
        dialog.setOption(QFileDialog.DontResolveSymlinks, True)

        single_file_checkbox = QCheckBox("选择单个文件")
        dialog.layout().addWidget(single_file_checkbox)

        if dialog.exec_():
            file_paths = dialog.selectedFiles()
            if single_file_checkbox.isChecked():
                file_path = file_paths[0]
                self.source_file_path_label.setText(file_path)
                self.file_type = functions.determine_file_type(file_path)
            else:
                folder_path = dialog.directoryUrl().toLocalFile()
                self.source_file_path_label.setText(folder_path)
                self.file_type = "文件夹"

    def choose_output_path(self):
        directory = QFileDialog.getExistingDirectory(self, "选择输出路径")
        if directory:
            self.output_file_path_label.setText(directory)


    def convert_files_to_txt(self):
        files_path = self.source_file_path_label.text()
        output_file_path = self.output_file_path_label.text()
        progress_queue = queue.Queue()
        functions.process_files(files_path, output_file_path, self.update_progress_signal.emit)
        

    def update_file_status(self, current_index, total_files):
        # 更新状态标签的文本以显示当前转换文件的进度
        self.file_status_label.setText(f"转换文件: {current_index}/{total_files}")


# 创建和运行应用
app = QApplication(sys.argv)
ex = EbookConverter()
ex.show()
sys.exit(app.exec_())

