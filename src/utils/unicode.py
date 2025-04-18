"""Unicode 字元處理工具模組

此模組提供 Unicode 字元與轉義序列之間的轉換功能。
"""

import re


def unescape_unicode(text: str) -> str:
    """將 Unicode 轉義序列轉回 UTF-8 字元

    Args:
        text: 包含 Unicode 轉義序列的字串

    Returns:
        轉換後的 UTF-8 字串
    """
    return re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), text)


def escape_non_ascii(text: str) -> str:
    """將非 ASCII 字元轉換為 Unicode 轉義序列

    Args:
        text: 包含非 ASCII 字元的字串

    Returns:
        轉換後的字串，非 ASCII 字元會被轉換為 Unicode 轉義序列
    """
    escaped_text = []
    for char in text:
        if ord(char) > 127:
            escaped_text.append(f"\\u{ord(char):04x}")
        else:
            escaped_text.append(char)
    return "".join(escaped_text)
