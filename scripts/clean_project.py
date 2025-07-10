#!/usr/bin/env python3
"""
PDF Zipper 项目清理脚本
清理所有构建产物、缓存文件和临时文件
"""

import os
import shutil
import glob
from pathlib import Path


def clean_directory(path, description):
    """清理指定目录"""
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"✅ 清理 {description}: {path}")
    else:
        print(f"⏭️  跳过 {description}: {path} (不存在)")


def clean_files(pattern, description):
    """清理匹配模式的文件"""
    files = glob.glob(pattern, recursive=True)
    if files:
        for file in files:
            try:
                if os.path.isfile(file):
                    os.remove(file)
                elif os.path.isdir(file):
                    shutil.rmtree(file)
                print(f"✅ 删除 {description}: {file}")
            except Exception as e:
                print(f"❌ 删除失败 {file}: {e}")
    else:
        print(f"⏭️  跳过 {description}: 没有找到匹配文件")


def main():
    """主清理函数"""
    print("🧹 PDF Zipper 项目清理工具")
    print("=" * 50)
    
    # 切换到项目根目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    print(f"📁 项目根目录: {project_root}")
    print()
    
    # 清理构建目录
    print("🔨 清理构建产物...")
    clean_directory("build", "PyInstaller 构建目录")
    clean_directory("dist", "PyInstaller 输出目录")
    clean_directory("release", "发布目录")
    clean_directory("hooks", "PyInstaller hooks 目录")
    
    # 清理 Python 缓存
    print("\n🐍 清理 Python 缓存...")
    clean_files("**/__pycache__", "Python 缓存目录")
    clean_files("**/*.pyc", "Python 字节码文件")
    clean_files("**/*.pyo", "Python 优化字节码文件")
    clean_files("**/*.pyd", "Python 扩展模块")
    
    # 清理包构建产物
    print("\n📦 清理包构建产物...")
    clean_files("*.egg-info", "Egg 信息目录")
    clean_files(".eggs", "Eggs 目录")
    clean_directory(".pytest_cache", "Pytest 缓存")
    clean_directory(".mypy_cache", "MyPy 缓存")
    clean_directory(".coverage", "Coverage 缓存")
    clean_directory("htmlcov", "Coverage HTML 报告")
    
    # 清理 PyInstaller 文件
    print("\n🔧 清理 PyInstaller 文件...")
    clean_files("*.spec", "PyInstaller spec 文件")
    
    # 清理测试文件
    print("\n🧪 清理测试文件...")
    clean_files("test*.pdf", "测试 PDF 文件")
    clean_files("test*.pptx", "测试 PowerPoint 文件")
    clean_files("demo*.pdf", "演示 PDF 文件")
    clean_files("demo*.pptx", "演示 PowerPoint 文件")
    clean_files("sample.*", "示例文件")
    clean_files("*_compressed.*", "压缩输出文件")
    clean_files("*_converted.*", "转换输出文件")
    
    # 清理系统文件
    print("\n💻 清理系统文件...")
    clean_files("**/.DS_Store", "macOS 系统文件")
    clean_files("**/Thumbs.db", "Windows 缩略图文件")
    clean_files("**/*.tmp", "临时文件")
    clean_files("**/*.temp", "临时文件")
    
    # 清理编辑器文件
    print("\n📝 清理编辑器文件...")
    clean_files("**/*.swp", "Vim 交换文件")
    clean_files("**/*.swo", "Vim 交换文件")
    clean_files("**/*~", "备份文件")
    clean_files("**/.vscode", "VS Code 配置")
    clean_files("**/.idea", "PyCharm 配置")
    
    print("\n🎉 清理完成!")
    print("📋 建议运行以下命令验证项目状态:")
    print("   make test          # 运行测试")
    print("   make lint          # 检查代码质量")
    print("   make build-cli     # 测试构建")


if __name__ == "__main__":
    main()
