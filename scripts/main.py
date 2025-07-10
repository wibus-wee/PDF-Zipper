#!/usr/bin/env python3
"""
PDF Zipper 可执行文件入口点
"""

import sys
import os

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 导入并运行主程序
if __name__ == "__main__":
    from pdf_zipper.cli import main
    main()
