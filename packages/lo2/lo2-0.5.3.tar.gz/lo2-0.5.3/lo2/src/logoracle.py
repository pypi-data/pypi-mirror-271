#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 17:39:20 2023

@author: zhangte01
"""

from . import lo2json as json
from .lo2log import *
from . import parser
from . import lo2html
import os
import sys


if __name__ == "__main__":
    log_fn = sys.argv[1]
    lo2_lang_fn = sys.argv[2]

    def get_file_or_dir_contents(path: str):
        """ 获取文件或目录下的所有内容"""
        if os.path.isfile(path):
            # 如果路径是文件，则返回文件名
            return [path]
        elif os.path.isdir(path):
            # 获取目录下所有内容
            contents = os.listdir(path)

            # 分为目录和文件
            dirs = [d for d in contents if os.path.isdir(os.path.join(path, d))]
            files = [f for f in contents if os.path.isfile(os.path.join(path, f))]

            # 按 ls -l 的方式排序目录和文件
            dirs.sort(key=lambda x: x.lower())
            files.sort(key=lambda x: x.lower())

            # 合并目录和文件列表，并保持目录在前
            all_contents = dirs + files

            # 返回完整的文件路径列表
            fs = [os.path.join(path, content) for content in all_contents]
            fs.reverse()
            return fs
        else:
            print("{path} is not a file or dir")
            return None

    result = get_file_or_dir_contents(log_fn)

    if not result:
        sys.exit(0)

    text = []
    for e_f in result:
        with open(e_f, "r", errors="replace") as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]
            text += lines

    with open(lo2_lang_fn, "r") as f:
        lo2_code = json.load(f)

    lo2lang = parser.Lo2IRExecutor(lo2_code)

    lo2lang.parser()
    state_list = lo2lang.run_text(text)

    """
    with open('debug-ast.json', 'w') as f:
        f.write(json.dumps(lo2lang.operable_ast))
    """

    for e in state_list:
        e["state"] = e["state"].name

    render_data = {
        "state_list": state_list,
        "textlog": text,
        "coverage": lo2lang.coverage,
        "lo2_fn": lo2lang.lo2_src_name,
    }

    out_dir = os.getcwd()
    html_mvc = lo2html.MVC()
    html_mvc.model(render_data).to_controller("timeline").to_html(outdir=out_dir)

    for e in result:
        print(e)
