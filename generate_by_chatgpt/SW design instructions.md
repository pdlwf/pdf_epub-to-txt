# 软件设计文档 - 电子书转换工具

## 1. 总体架构

本软件是一个用于将电子书格式（PDF、EPUB）转换为文本格式（TXT）的桌面应用程序。软件采用模块化设计，主要包括用户界面模块、文件处理模块、进度监控模块和配置管理模块。

### 1.1 模块划分

- **用户界面模块** (`main_1.py`): 负责与用户交互，展示转换进度和状态。
- **文件处理模块** (`functions.py`): 负责文件的读取、转换和写入。
- **进度监控模块** (`progress.py`): 负责跟踪文件转换进度和完成状态。
- **配置管理模块** (`config.py`): 管理软件的配置设置，如调试模式开关。

## 2. 关键类和方法设计

### 2.1 `EbookConverter` 类 (用户界面模块)

#### 功能
- 管理用户界面，包括文件选择、转换进度展示和错误消息提示。
- 与文件处理模块和进度监控模块交互，实现软件的主要功能。

#### 方法
- `__init__`: 初始化界面和变量。
- `initUI`: 设置界面布局和元素。
- `choose_source_file`: 通过对话框选择源文件或文件夹。
- `choose_output_path`: 通过对话框选择输出路径。
- `convert_files_to_txt`: 启动文件转换流程，包括重置进度监控和调用文件处理模块。
- `check_progress_queue`: 定期调用进度监控模块，更新UI。
- `update_ui`: 根据进度监控模块的反馈更新界面元素。


```
def __init__(self):
    初始化界面元素和变量。
    设置文件类型、文件路径标签、进度条等界面元素。
    初始化定时器用于定期检查进度队列。
    创建进度监控实例。
```
```
def choose_source_file(self):
    打开一个文件对话框，允许用户选择单个文件或整个文件夹。
    获取用户选择的文件/文件夹路径，并更新源文件路径标签。
    如果选择了单个文件，则判断文件类型。
```
```
def choose_output_path(self):
    打开一个目录选择对话框，允许用户选择输出路径。
    获取并更新输出路径标签。
```
```
def convert_files_to_txt(self):
    在开始转换前重置已完成的文件数量。
    获取源文件路径和输出文件路径。
    从输入框获取文件大小限制，并转换为字节。
    调用 process_files 函数进行文件转换。
    启动定时器以定期更新进度。
```
```
def check_progress_queue(self):
    调用 ProgressMonitor 实例的 check_progress 方法。
    通过该方法定期从队列中获取进度更新并更新UI。
```
```
def update_ui(self, element, value):
    根据传入的元素类型和值更新界面。
    包括更新进度条值、文件状态标签和转换完成状态。
```

### 2.2 `ProgressMonitor` 类 (进度监控模块)

#### 功能
- 监控文件转换进度和状态，通过队列与文件处理模块通信。

#### 方法
- `__init__`: 初始化进度监控所需的变量。
- `check_progress`: 处理队列中的消息，更新已完成文件数量，调用 `update_ui` 方法更新界面。



### 2.3 文件处理模块 (`functions.py`)

#### 功能
- 实现文件的读取、转换和写入功能。

#### 方法
- `convert_file_to_txt_threaded`: 为每个文件创建新线程进行转换。
- `process_files`: 遍历文件夹，对每个文件调用 `convert_file_to_txt_threaded`。
- `convert_file_to_txt`: 执行文件的读取和转换逻辑，更新进度监控。
- `convert_pdf_to_txt`, `convert_epub_to_txt`: 实现PDF和EPUB格式的转换逻辑。
- 其他辅助函数：包括文件类型判定、文件遍历、文件排序等。



```
def convert_file_to_txt_threaded(file_path, output_file_path, file_type, max_size, progress_queue, completed_files):
    为每个文件创建一个新线程以进行转换。
    调用 convert_file_to_txt 函数，并传入必要参数。
```
```
def process_files(source_path, output_path, max_size, progress_queue, completed_files):
    遍历指定路径下的所有文件。
    对每个文件判断类型，并调用 convert_file_to_txt_threaded 进行转换。
```
```
def convert_file_to_txt(file_path, output_file_path, file_type, max_size, progress_queue, completed_files):
    初始化 output_file_index 和 current_size。
    根据文件类型调用相应的转换函数（PDF或EPUB）。
    转换完成一个文件后，向队列发送 file_status 消息。
```
```
def convert_pdf_to_txt(pdf_file_path, output_file_path, output_file_index, current_size, max_size, progress_queue):
    读取PDF文件，并逐页提取文本。
    检查文件大小并分割文件。
    更新进度并发送至队列。
    处理异常并发送错误信息至队列。
```
```
def convert_epub_to_txt(epub_file_path, output_file_path, output_file_index, current_size, max_size, progress_queue):
    读取EPUB文件，并提取文本内容。
    检查文件大小并分割文件。
    更新进度并发送至队列。
    处理异常并发送错误信息至队列。

```
```
def determine_file_type(file_path):
    判断并返回文件类型（PDF或EPUB）。

def traverse_directory(directory_path):
    遍历指定目录并返回所有文件路径。

def sort_files(file_paths):
    对文件路径列表进行排序。
```

### 2.4 配置管理模块 (`config.py`)

#### 功能
- 提供软件运行时的配置信息。

## 3. 开发说明

- 在实现 `EbookConverter` 类时，重点在于用户交互的流畅性和准确性。所有UI操作应该直观并且响应用户的操作。
- `ProgressMonitor` 类需要高效地处理来自文件处理模块的消息，并准确地反馈到UI模块。
- 文件处理模块的关键在于转换逻辑的正确性和文件操作的安全性。需要确保在多线程环境下的稳定性和数据一致性。
- 所有模块应该通过清晰的接口进行交互，保持低耦合度。

## 4. 其他说明

- 该软件设计文档适用于当前版本的电子书转换工具。对于未来的扩展和维护，应该考虑到模块间的依赖关系和扩展性。
- 软件的测试和调试是重要的开发阶段，需要在真实环境中验证软件的功能和性能。
