# -*- coding:utf-8 -*-
"""
utils base
"""
from typing import TypeVar
import re

KT = TypeVar('KT')
VT = TypeVar('VT')


def sanitize_input(input_string: str) -> str:
    """
    Sanitizes an input string by escaping potentially dangerous characters.

    Args:
        input_string (str): The string to be sanitized.

    Returns:
        str: The sanitized string.
    """

    # 移除或转义特殊字符
    sanitized = re.sub(r'[;|&`\'\"*?~<>^()[\]{}$\\]', '', input_string)
    return sanitized


def chinese_double_length(string: str) -> int:
    """
    Get string length, chinese double length
    Args:
        string (str): string for calculate length

    Returns:
        int: string length
    """
    length = 0
    for char in string:
        if ord(char) > 127:  # 如果字符的ASCII码大于127，则认为是中文字符
            length += 2
        else:
            length += 1
    return length
