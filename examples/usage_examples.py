#!/usr/bin/env python3
"""
PDF Zipper 使用示例

这个文件展示了如何在 Python 代码中使用 PDF Zipper 的各种功能。
"""

import os
import sys
from pathlib import Path

# 添加 pdf_zipper 到路径（如果没有安装的话）
try:
    from pdf_zipper import autocompress_pdf, compress_pdf, convert_to_ppt
except ImportError:
    # 如果没有安装，尝试从源码导入
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from pdf_zipper import autocompress_pdf, compress_pdf, convert_to_ppt


def simple_logger(message: str):
    """简单的日志函数"""
    print(f"[LOG] {message}")


def example_auto_compress():
    """示例：自动压缩 PDF 到指定大小"""
    print("🎯 示例：自动压缩 PDF")
    print("-" * 40)
    
    input_file = "sample.pdf"
    output_file = "auto_compressed.pdf"
    target_size = 2.0  # 2MB
    
    if not os.path.exists(input_file):
        print(f"❌ 输入文件不存在: {input_file}")
        return
    
    print(f"输入文件: {input_file}")
    print(f"输出文件: {output_file}")
    print(f"目标大小: {target_size} MB")
    print()
    
    autocompress_pdf(input_file, output_file, target_size, simple_logger)
    print()


def example_manual_compress():
    """示例：手动压缩 PDF"""
    print("🔧 示例：手动压缩 PDF")
    print("-" * 40)
    
    input_file = "sample.pdf"
    output_file = "manual_compressed.pdf"
    dpi = 120
    
    if not os.path.exists(input_file):
        print(f"❌ 输入文件不存在: {input_file}")
        return
    
    print(f"输入文件: {input_file}")
    print(f"输出文件: {output_file}")
    print(f"DPI: {dpi}")
    print()
    
    compress_pdf(input_file, output_file, dpi, simple_logger)
    print()


def example_convert_to_ppt():
    """示例：转换 PDF 为 PowerPoint"""
    print("📊 示例：转换 PDF 为 PowerPoint")
    print("-" * 40)
    
    input_file = "sample.pdf"
    output_file = "converted.pptx"
    dpi = 150
    
    if not os.path.exists(input_file):
        print(f"❌ 输入文件不存在: {input_file}")
        return
    
    print(f"输入文件: {input_file}")
    print(f"输出文件: {output_file}")
    print(f"DPI: {dpi}")
    print()
    
    convert_to_ppt(input_file, output_file, dpi, simple_logger)
    print()


def create_sample_pdf():
    """创建示例 PDF 文件"""
    try:
        import fitz  # PyMuPDF
        
        print("📄 创建示例 PDF 文件...")
        
        doc = fitz.open()
        
        # 添加多个页面以便测试
        for i in range(3):
            page = doc.new_page()
            text = f"""
PDF Zipper 测试文档 - 第 {i+1} 页

这是一个用于测试 PDF Zipper 功能的示例文档。

功能特性：
• 自动压缩到指定大小
• 手动压缩（自定义 DPI）
• 转换为 PowerPoint 演示文稿
• 美观的终端界面
• 完整的命令行支持

页面 {i+1} / 3
            """
            page.insert_text((50, 50), text.strip())
        
        doc.save("sample.pdf")
        doc.close()
        
        file_size = os.path.getsize("sample.pdf") / (1024 * 1024)
        print(f"✅ 示例 PDF 创建成功: sample.pdf ({file_size:.2f} MB)")
        return True
        
    except ImportError:
        print("❌ 需要安装 PyMuPDF 来创建示例 PDF")
        return False
    except Exception as e:
        print(f"❌ 创建示例 PDF 失败: {e}")
        return False


def batch_processing_example():
    """示例：批量处理多个 PDF 文件"""
    print("📁 示例：批量处理")
    print("-" * 40)
    
    # 查找当前目录下的所有 PDF 文件
    pdf_files = list(Path(".").glob("*.pdf"))
    
    if not pdf_files:
        print("❌ 当前目录没有找到 PDF 文件")
        return
    
    print(f"找到 {len(pdf_files)} 个 PDF 文件:")
    for pdf_file in pdf_files:
        print(f"  - {pdf_file}")
    
    print("\n开始批量压缩...")
    
    for pdf_file in pdf_files:
        if pdf_file.name.startswith("sample"):  # 只处理示例文件
            output_file = pdf_file.with_stem(f"{pdf_file.stem}_batch_compressed")
            print(f"\n处理: {pdf_file} -> {output_file}")
            
            try:
                compress_pdf(str(pdf_file), str(output_file), 100, simple_logger)
            except Exception as e:
                print(f"❌ 处理失败: {e}")


def main():
    """主函数"""
    print("🗜️ PDF Zipper 使用示例")
    print("=" * 50)
    print()
    
    # 创建示例 PDF
    if not create_sample_pdf():
        print("无法创建示例 PDF，跳过演示")
        return
    
    print()
    
    # 运行各种示例
    try:
        example_auto_compress()
        example_manual_compress()
        example_convert_to_ppt()
        batch_processing_example()
        
        print("🎉 所有示例运行完成！")
        print("\n生成的文件:")
        for file in Path(".").glob("*compressed*"):
            print(f"  - {file}")
        for file in Path(".").glob("*.pptx"):
            print(f"  - {file}")
            
    except KeyboardInterrupt:
        print("\n👋 用户中断了演示")
    except Exception as e:
        print(f"\n❌ 演示过程中出错: {e}")


if __name__ == "__main__":
    main()
