# main_1.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QProgressBar, QFileDialog, \
    QCheckBox, QLineEdit
from PyQt5.QtCore import QTimer
import functions  # 您的 functions 模块
from progress import ProgressMonitor
from config import DEBUG_V1_1, MAC_DEBUG, WIN_DEBUG


class EbookConverter(QWidget):
    def __init__(self):
        super().__init__()
        #self.file_type = ""
        self.source_file_path_label = QLabel("源文件")
        self.output_file_path_label = QLabel("目标文件")
        self.file_status_label = QLabel("转换状态: 未开始")  # 添加状态标签
        self.progress_bar = QProgressBar()  # 初始化进度条

        self.file_size_input = QLineEdit(self)
        self.file_size_input.setPlaceholderText("输入文件大小限制（MB）")

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_progress_queue)
        self.timer.setInterval(1000)  # 每隔1000毫秒检查一次

        self.progress_monitor = ProgressMonitor(self.update_ui)

        # debug-win
        if WIN_DEBUG:
            self.source_file_path_label = QLabel("C:\\Users\\bobby\\Downloads\\test")
            self.output_file_path_label = QLabel("C:\\Users\\bobby\\Downloads\\test")

        # debug-mac
        if MAC_DEBUG:
            self.source_file_path_label = QLabel("/Users/bobby/Downloads/test")
            self.output_file_path_label = QLabel("/Users/bobby/Downloads/test")

        self.initUI()

    def initUI(self):
        self.setWindowTitle("电子书转换工具")
        layout = QVBoxLayout()

        choose_source_file_button = QPushButton("源文件路径")
        choose_source_file_button.clicked.connect(self.choose_source_file)

        choose_output_path_button = QPushButton("目标路径")
        choose_output_path_button.clicked.connect(self.choose_output_path)

        convertor_button = QPushButton("FILE到TXT")
        convertor_button.clicked.connect(self.convert_files_to_txt)

        layout.addWidget(QLabel("TXT文件大小限制（MB）："))
        layout.addWidget(self.file_size_input)

        
        layout.addWidget(QLabel("设置源文件路径："))
        layout.addWidget(self.source_file_path_label)
        layout.addWidget(choose_source_file_button)
        layout.addWidget(QLabel("设置目标输出路径："))
        layout.addWidget(self.output_file_path_label)
        layout.addWidget(choose_output_path_button)

        layout.addWidget(QLabel("点击开始转换："))
        layout.addWidget(convertor_button)

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
                #self.file_type = functions.determine_file_type(file_path)
            else:
                folder_path = dialog.directoryUrl().toLocalFile()
                self.source_file_path_label.setText(folder_path)
                #self.file_type = "文件夹"

    def choose_output_path(self):
        directory = QFileDialog.getExistingDirectory(self, "选择输出路径")
        if directory:
            self.output_file_path_label.setText(directory)

    def convert_files_to_txt(self):
        # 在开始新的转换之前重置已完成文件的数量
        self.progress_monitor.completed_files = 0

        self.timer.start()  # 启动定时器
        
        files_path = self.source_file_path_label.text()
        output_file_path = self.output_file_path_label.text()
        sorted_files = functions.sort_files(functions.traverse_directory(files_path))
        
        self.progress_monitor.total_files = len(sorted_files)
        # 从文本框获取文件大小限制
        max_size_mb = self.file_size_input.text()
        try:
            max_size_mb = float(max_size_mb)  # 将输入转换为浮点数
            max_size_bytes = max_size_mb * 1024 * 1024  # 将MB转换为字节
        except ValueError:
            max_size_bytes = 4 * 1024 * 1024  # 输入无效时也默认为 4MB
        if DEBUG_V1_1:
            print("Total_files Value In convert files to txt: ", self.progress_monitor.total_files)

        functions.process_files(files_path, output_file_path, max_size_bytes, self.progress_monitor.progress_queue,
                                self.progress_monitor.completed_files)

    def check_progress_queue(self):
        # 调用 ProgressMonitor 实例的 check_progress 方法
        self.progress_monitor.check_progress()

    def update_ui(self, element, value):
        '''
        根据提供的元素类型和值更新用户界面。
        Args:
            element (str): 要更新的UI元素类型（如 'file_status', 'progress_bar'）。
            value (str or int): 根据元素类型提供的更新值。
        '''
        if element == 'file_status':
            self.file_status_label.setText(value)
        elif element == 'progress_bar':
            self.progress_bar.setValue(value)
        elif element == 'completed':
            self.progress_bar.setValue(self.progress_bar.maximum())
            # 可以在这里添加其他完成时的逻辑


# 创建和运行应用
app = QApplication(sys.argv)
ex = EbookConverter()
ex.show()
sys.exit(app.exec_())
