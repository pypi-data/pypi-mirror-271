#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 18:22:55 2023

@author: zhangte01
"""
import sys

# ANSI terminal codes (if changed, regular expressions in LineMatcher need to be udpated)
ANSI_RED = "\033[1;31m[lo2]"
ANSI_YELLOW = "\033[0;33m[lo2]"
ANSI_GREEN = "\033[0;32m[lo2]"
ANSI_NORMAL = "\033[0m[lo2]"
ANSI_RESET = "\033[0m"


# def color_print(message, color):
#    """ Print a message to stderr with colored highlighting """
#    sys.stderr.write("%s%s%s\n" % (color, message,  ANSI_NORMAL))


def color_print(color, *args, **kwargs):
    """
    以指定颜色打印输出信息，并在信息结束后自动重置颜色。
    
    Args:
        color (str): 打印信息的颜色，可选值为"red"、"green"、"yellow"、"blue"、"magenta"、"cyan"或"white"。
        *args (Any): 要打印的信息内容，可以接收多个参数。
        **kwargs (Any): 可选参数，支持"indent"参数，表示输出信息的缩进量，默认为0。
    
    Returns:
        None
    
    """
    print(color, end="")
    if "indent" in kwargs:
        indent = kwargs.pop("indent")
        print(" " * indent, end="")
    print(*args, **kwargs, end="")
    print(ANSI_RESET)


def prompt_error(*args, **kwargs):
    """print error"""
    color_print(ANSI_RED, *args, **kwargs)


def prompt_warn(*args, **kwargs):
    """print warn"""
    color_print(ANSI_YELLOW, *args, **kwargs)


def prompt_success(*args, **kwargs):
    """print success"""
    color_print(ANSI_GREEN, *args, **kwargs)


def prompt_info(*args, **kwargs):
    """print info"""
    color_print(ANSI_NORMAL, *args, **kwargs)
