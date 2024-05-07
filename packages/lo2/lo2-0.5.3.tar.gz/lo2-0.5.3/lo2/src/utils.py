from datetime import datetime, timedelta
import re
import os

import chardet
import tempfile
import shutil


def preprocess_file_in_place(file_path):
    """
    对文件进行预处理，修复log文件编码问题，在原地修改文件。

    Args:
        file_path (str): 需要预处理的文件路径。
    Returns:
        None
    """
    temp_file_path = file_path + ".temp"

    with open(file_path, "rb") as input_file, tempfile.NamedTemporaryFile(
        mode="w", delete=False, encoding="utf-8"
    ) as output_file:
        for line in input_file:
            result = chardet.detect(line)
            encoding = result["encoding"]
            confidence = result["confidence"]

            if confidence < 0.5:
                print(
                    "Low confidence in detected encoding. Manual inspection recommended."
                )

            decoded_line = line.decode(encoding, errors="replace")
            output_file.write(decoded_line)

    # 用临时文件替换原始文件
    shutil.move(output_file.name, temp_file_path)
    os.remove(file_path)
    os.rename(temp_file_path, file_path)

    print(f"File has been preprocessed in place: {file_path}")


def get_kernel_file(folder):
    """
    根据文件夹路径获取kernel日志文件列表

    Args:
        folder (str): 文件夹路径

    Returns:
        List[str]: kernel日志文件列表，按照时间排序

    """
    # 使用正则表达式检查字符串是否以 "Hello" 开始
    pattern = re.compile(r"^kernel_log_[0-9]+_([0-9]{10,})")
    number = re.compile(r"^kernel_log_[0-9]+_[0-9]{10,}\.([0-9]+)$")

    kernel_path = os.path.join(folder, "kernel")
    if not os.path.isdir(kernel_path):
        return None
    log_files = []
    for root, dirs, files in os.walk(kernel_path):
        for file in files:
            match = pattern.match(file)
            if match:
                timestamp = int(match.group(1))
                num_match = number.match(file)
                num = 0
                if num_match:
                    num = int(num_match.group(1))
                log_files.append((timestamp - num, os.path.join(root, file)))
    log_files = sorted(log_files, key=lambda x: x[0])
    return list(map(lambda x: x[1], log_files))


def get_logcat_file(folder):
    """
    获取指定文件夹下所有以"logcat_"开头的日志文件，并按时间降序排序后返回。

    Args:
        folder (str): 目标文件夹路径。

    Returns:
        List[str]: 符合条件的日志文件路径列表。

    """
    logcat_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.startswith("logcat_"):
                logcat_files.append(os.path.join(root, file))
    logcat_files.sort()
    logcat_files.reverse()
    return logcat_files


def concatenate_files(output_file, file_list):
    """
    将多个文件连接成一个文件。

    Args:
        output_file (str): 输出文件的路径。
        file_list (List[str]): 需要连接的文件列表。

    Returns:
        None
    """
    with open(output_file, "wb") as output:
        for file_name in file_list:
            with open(file_name, "rb") as input_file:
                for chunk in iter(lambda: input_file.read(4096), b""):
                    output.write(chunk)
            # 在每个文件之间加一个空行
            output.write(b"\n")


def get_all_files_in_folder(folder):
    """
    获取指定文件夹中所有文件的绝对路径。

    Args:
        folder: 目标文件夹路径。

    Returns:
        包含所有文件绝对路径的列表。

    """
    all_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files
