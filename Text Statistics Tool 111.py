#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文本统计工具 (mywc) - 初学者友好版
功能：统计文件或标准输入的行数、单词数、字符数
用法：python wc.py file.txt
      cat file.txt | python wc.py
"""

import sys
import argparse

# ==================== 统计单个文件 ====================
def count_file(filepath):
    """读取文件内容，返回 (行数, 单词数, 字符数)，失败返回 None"""
    try:
        # 先尝试用 UTF-8 打开
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"错误：文件 '{filepath}' 不存在", file=sys.stderr)
        return None
    except UnicodeDecodeError:
        # 如果 UTF-8 失败，尝试用 GBK（常见于中文 Windows）
        try:
            with open(filepath, 'r', encoding='gbk') as f:
                content = f.read()
        except Exception as e:
            print(f"错误：无法读取文件 '{filepath}' - {e}", file=sys.stderr)
            return None
    
    lines = content.count('\n')          # 行数 = 换行符个数
    words = len(content.split())         # 单词数 = 按空白分割后的段数
    chars = len(content)                 # 字符数 = 字符串长度
    return (lines, words, chars)

# ==================== 统计标准输入 ====================
def count_stdin():
    """从键盘/管道读取内容并统计"""
    content = sys.stdin.read()
    lines = content.count('\n')
    words = len(content.split())
    chars = len(content)
    return (lines, words, chars)

# ==================== 主程序 ====================
def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(description="统计文本文件的行数、单词数、字符数")
    parser.add_argument('files', nargs='*', help='要统计的文件（可多个，不写则从标准输入读取）')
    parser.add_argument('-l', '--lines', action='store_true', help='只显示行数')
    parser.add_argument('-w', '--words', action='store_true', help='只显示单词数')
    parser.add_argument('-c', '--chars', action='store_true', help='只显示字符数')
    args = parser.parse_args()

    # 决定显示哪些内容：如果什么都没选，就全显示
    show_lines = args.lines or not (args.words or args.chars)
    show_words = args.words or not (args.lines or args.chars)
    show_chars = args.chars or not (args.lines or args.words)

    # 情况1：没有提供文件名 → 从标准输入读取
    if not args.files:
        lines, words, chars = count_stdin()
        # 按需打印
        parts = []
        if show_lines:
            parts.append(str(lines).rjust(8))
        if show_words:
            parts.append(str(words).rjust(8))
        if show_chars:
            parts.append(str(chars).rjust(8))
        print(' '.join(parts) + " (标准输入)")
        return

    # 情况2：有一个或多个文件
    total_lines = total_words = total_chars = 0
    for file in args.files:
        result = count_file(file)
        if result is None:
            continue   # 出错就跳过这个文件
        lines, words, chars = result
        total_lines += lines
        total_words += words
        total_chars += chars

        # 打印当前文件的统计结果
        parts = []
        if show_lines:
            parts.append(str(lines).rjust(8))
        if show_words:
            parts.append(str(words).rjust(8))
        if show_chars:
            parts.append(str(chars).rjust(8))
        print(' '.join(parts) + f" {file}")

    # 如果统计了多个文件，再打印一行总计
    if len(args.files) > 1:
        parts = []
        if show_lines:
            parts.append(str(total_lines).rjust(8))
        if show_words:
            parts.append(str(total_words).rjust(8))
        if show_chars:
            parts.append(str(total_chars).rjust(8))
        print(' '.join(parts) + " 总计")

if __name__ == '__main__':
    main()