#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: liermeng
"""

import os
import sys
import subprocess

class ADBProcessTerminatedError(Exception):
    """ 进程终止异常 """
    pass

def print_error(text):
    """使用红色字体来打印错误信息"""
    print(f'\033[31m{text}\033[0m')

def check_log_path(log_path: str):
    """判断log文件的来源是log文件还是adb"""
    if os.path.exists(log_path):
        return 1
    else:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        devices = result.stdout.split('\n')[1:-2]
        adb_device_flag = False
        for d in devices:
            name, stat = d.split('\t')
            if log_path in name and stat == 'device':
                adb_device_flag = True
                break
        if adb_device_flag:
            return 0
        else:
            raise Exception(f"adb device {log_path} doesn't exist, is offline or is unauthorised")

def get_realtime_log(device_name: str):
    """运行 adb logcat 命令"""
    process = subprocess.Popen(['adb', '-s', device_name, 'logcat'], stdout=subprocess.PIPE)
    try:
        # 逐行读取输出
        for line in iter(process.stdout.readline, b''):
            # 如果进程已经结束，抛出异常
            if process.poll() is not None:
                raise ADBProcessTerminatedError("adb process terminated")
            # 解码为字符串并去除末尾的换行符
            line = line.decode(errors='replace').rstrip()
            yield line
    finally:
        process.wait()
