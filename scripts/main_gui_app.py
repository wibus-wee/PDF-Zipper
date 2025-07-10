#!/usr/bin/env python3
"""
PDF Zipper GUI App Bundle 专用入口点
双击 App Bundle 时直接启动 GUI 界面
"""

import sys
import os

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def main():
    """智能启动：App Bundle 双击时启动 GUI，命令行时支持参数"""
    try:
        # 检查是否有命令行参数
        if len(sys.argv) > 1:
            # 有参数时，使用完整的 CLI 功能
            from pdf_zipper.cli import main as cli_main
            cli_main()
        else:
            # 无参数时（App Bundle 双击），直接启动 GUI
            from pdf_zipper.gui import launch_gui
            launch_gui()
        
    except KeyboardInterrupt:
        # 用户按 Ctrl+C 退出
        print("\n👋 用户取消操作")
        sys.exit(0)
    except Exception as e:
        # 显示错误信息
        print(f"❌ 启动 GUI 时出错: {e}")
        
        # 尝试显示图形化错误对话框（如果可能）
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.withdraw()  # 隐藏主窗口
            
            messagebox.showerror(
                "PDF Zipper 启动错误",
                f"启动 GUI 时出现错误:\n\n{e}\n\n请检查系统要求或联系开发者。"
            )
            
        except ImportError:
            # 如果没有 tkinter，就在终端显示错误
            print("💡 提示: 如果问题持续，请尝试从终端运行:")
            print("   pdf-zipper gui")
        
        sys.exit(1)

if __name__ == "__main__":
    main()
