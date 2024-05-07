#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 20:06:10 2023

@author: zhangte01
"""

import json
import re
import enum
#from json import *


class EnhancedJSONEncoder(json.JSONEncoder):
    """
    支持正则表达式、枚举的json编码
    """
    def default(self, obj):
        """
        Serialize objects that are not JSON serializable by default.
        
        Args:
            obj: Any object to be serialized.
        
        Returns:
            A dictionary representing the object.
        
        """
        if isinstance(obj, re.Pattern):
            return {"__regex_pattern__": obj.pattern}
        elif isinstance(obj, enum.Enum):
            return {"__enum__": obj.name}
        return super().default(obj)


def enhanced_decode(dct):
    """
    增强型解码函数，用于将字典类型的数据转换为其他类型的数据。
    
    Args:
        dct (dict): 需要进行解码的字典类型数据。
    
    Returns:
        Union[re.Pattern, Enum, dict]: 解码后的数据，可以是正则表达式对象、枚举类型对象或字典类型数据。
    
    """
    if "__regex_pattern__" in dct:
        return re.compile(dct["__regex_pattern__"])
    elif "__enum__" in dct:
        # TODO: 没有考虑类型还原
        return dct["__enum__"]
    return dct


def dumps(obj, **kwargs):
    """
    将 Python 对象转换为 JSON 字符串格式。
    
    Args:
        obj (Any): 需要转换的 Python 对象。
        kwargs: 可选参数，其他传递给 `json.dumps` 函数的参数。
    
    Returns:
        str: 转换后的 JSON 字符串。
    
    """
    return json.dumps(obj, cls=EnhancedJSONEncoder, **kwargs)


def loads(s, **kwargs):
    """
    将 JSON 格式的字符串 s 转换成 Python 对象，并返回该对象。
    
    Args:
        s (str): 需要转换的 JSON 字符串。
        **kwargs: 其他可选参数，用于控制转换过程。
    
    Returns:
        Any: 转换后的 Python 对象，类型可能因 JSON 字符串的内容而异。
    
    """
    return json.loads(s, object_hook=enhanced_decode, **kwargs)


__all__ = ["dumps", "loads"]
